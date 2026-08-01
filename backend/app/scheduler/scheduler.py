import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

async def run_scheduled_keyword_crawls():
    """
    Background job that runs periodically:
    1. Fetches all ACTIVE keywords from the database.
    2. Executes crawl jobs sequentially with human-like delays to prevent rate limits.
    """
    from app.database.database import AsyncSessionLocal
    from app.models.keyword import Keyword, KeywordStatus
    from app.api.v1.admin.crawler import execute_crawl_job

    logger.info("⏰ Starting scheduled keyword crawl task...")
    
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Keyword).where(Keyword.status == KeywordStatus.ACTIVE))
        active_keywords = res.scalars().all()
        
    if not active_keywords:
        logger.info("No active keywords found for auto-crawling.")
        return

    logger.info(f"Found {len(active_keywords)} active keywords for auto-crawling.")
    
    for kw in active_keywords:
        logger.info(f"Auto-crawling keyword ID {kw.id}: '{kw.keyword}'")
        try:
            await execute_crawl_job(kw.id)
            # Safe 15-30 second human-like pause between keyword searches to protect LinkedIn account
            await asyncio.sleep(20)
        except Exception as err:
            logger.error(f"Error auto-crawling keyword ID {kw.id}: {err}")

class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started.")
            
            # Register recurring keyword crawler every 30 minutes
            self.scheduler.add_job(
                run_scheduled_keyword_crawls,
                trigger=IntervalTrigger(minutes=30),
                id="auto_keyword_crawler",
                replace_existing=True
            )
            logger.info("Scheduled 'auto_keyword_crawler' job every 30 minutes.")

    def stop(self):
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped.")

scheduler_service = SchedulerService()
