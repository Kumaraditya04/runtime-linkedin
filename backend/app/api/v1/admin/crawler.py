from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.database.database import get_db
from app.api.deps import get_current_admin
from app.crawler.linkedin import LinkedInCrawler
from app.services.keyword import KeywordService
from app.models.job_execution import JobExecution, JobStatus, JobErrorCategory
from app.models.lead import Lead, LeadStatus
from pydantic import BaseModel
import asyncio
import logging
import json
import hashlib
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

router = APIRouter()

class CrawlRequest(BaseModel):
    keyword_id: int

async def execute_crawl_job(keyword_id: int):
    crawler = LinkedInCrawler()
    from app.database.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            keyword = await KeywordService.get_keyword(db, keyword_id)
            if not keyword:
                return
            
            # Create a JobExecution
            job = JobExecution(
                job_type="linkedin_crawl",
                keyword_id=keyword.id,
                status=JobStatus.STARTING,
                started_at=datetime.now(timezone.utc),
                records_found=0,
                records_saved=0,
                records_skipped=0
            )
            db.add(job)
            job.status = JobStatus.RUNNING
            await db.commit()
            await db.refresh(job)

            logger.info(f"Starting crawl for keyword {keyword.keyword}")
            leads_extracted = []
            try:
                from app.crawler.voyager import LinkedInVoyagerCrawler
                voyager = LinkedInVoyagerCrawler()
                leads_extracted = await voyager.crawl(keyword, db=db)
            except Exception as voyager_err:
                logger.warning(f"Voyager REST API crawl failed for '{keyword.keyword}' ({voyager_err}). Falling back to Playwright crawler.")
                leads_extracted = await crawler.crawl(keyword, db=db)
            
            job.records_found = len(leads_extracted)
            
            job.status = JobStatus.SAVING
            await db.commit()
            
            # Process leads with bulk fingerprint deduplication
            leads_to_add = []
            for l in leads_extracted:
                post_url = l.get("post_url", "unknown_id")
                author_name = l.get("author_name", "Unknown Name")
                post_text = l.get("post_text", "")
                
                fingerprint_str = f"{post_url}|{author_name}|{post_text}"
                fingerprint_hash = hashlib.sha256(fingerprint_str.encode('utf-8')).hexdigest()
                
                # Check if fingerprint exists in DB
                existing = await db.execute(select(Lead.id).where(Lead.fingerprint == fingerprint_hash))
                if existing.scalar_one_or_none():
                    job.records_skipped += 1
                    continue
                
                lead = Lead(
                    keyword_id=keyword.id,
                    source="LinkedIn",
                    author_name=author_name,
                    author_url=l.get("author_url", "https://linkedin.com"),
                    post_url=post_url,
                    post_text=post_text,
                    fingerprint=fingerprint_hash,
                    raw_payload=l.get("raw_payload", {}),
                    normalized_data=l.get("normalized_data", {}),
                    status=LeadStatus.NEW
                )
                leads_to_add.append(lead)

            if leads_to_add:
                db.add_all(leads_to_add)
                job.records_saved = len(leads_to_add)
                await db.commit()
            
            job.status = JobStatus.COMPLETED
            job.finished_at = datetime.now(timezone.utc)
            
            keyword.last_run_at = datetime.now(timezone.utc)
            keyword.last_result_count = job.records_found
            
            await db.commit()
            logger.info(f"Crawl finished. Saved {len(leads_extracted)} leads.")
        except Exception as e:
            logger.error(f"Crawl failed for keyword {keyword_id}: {e}")
            err_msg = str(e)
            category = JobErrorCategory.UNKNOWN
            if "login wall" in err_msg.lower() or "auth" in err_msg.lower():
                category = JobErrorCategory.AUTH_FAILED
            elif "timeout" in err_msg.lower():
                category = JobErrorCategory.TIMEOUT
            elif "rate limit" in err_msg.lower():
                category = JobErrorCategory.RATE_LIMITED
            elif "selector" in err_msg.lower():
                category = JobErrorCategory.SELECTOR_CHANGED
            elif "chromium" in err_msg.lower() or "executable" in err_msg.lower():
                category = JobErrorCategory.ENVIRONMENT

            if 'job' in locals():
                job.status = JobStatus.FAILED
                job.finished_at = datetime.now(timezone.utc)
                job.error_message = err_msg
                job.error_category = category
                await db.commit()

@router.post("/run")
async def manual_crawl_run(
    payload: CrawlRequest,
    background_tasks: BackgroundTasks,
    admin=Depends(get_current_admin)
):
    background_tasks.add_task(execute_crawl_job, payload.keyword_id)
    return {"message": "Crawl job started in background.", "keyword_id": payload.keyword_id}

@router.post("/run-all")
async def manual_crawl_all_run(
    background_tasks: BackgroundTasks,
    admin=Depends(get_current_admin)
):
    from app.scheduler.scheduler import run_scheduled_keyword_crawls
    background_tasks.add_task(run_scheduled_keyword_crawls)
    return {"message": "Batch crawl task started for all active keywords in background."}
