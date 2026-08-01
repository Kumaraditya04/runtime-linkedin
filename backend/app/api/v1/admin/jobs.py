from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database import get_db
from app.api.deps import get_current_admin
from app.models.job_execution import JobExecution

from app.models.keyword import Keyword

router = APIRouter()

@router.get("")
async def get_jobs(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # Fetch latest 30 jobs with Keyword name
    query = select(JobExecution, Keyword.keyword).outerjoin(Keyword, JobExecution.keyword_id == Keyword.id).order_by(JobExecution.started_at.desc()).limit(30)
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {
            "id": j.id,
            "job_type": j.job_type,
            "keyword_id": j.keyword_id,
            "keyword_name": kw_name or f"Keyword #{j.keyword_id}",
            "status": j.status,
            "started_at": j.started_at,
            "finished_at": j.finished_at,
            "duration_ms": j.duration_ms,
            "records_found": j.records_found,
            "records_saved": j.records_saved,
            "records_skipped": j.records_skipped,
            "error_message": j.error_message
        } for j, kw_name in rows
    ]
