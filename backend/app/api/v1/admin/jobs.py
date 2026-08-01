from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database import get_db
from app.api.deps import get_current_admin
from app.models.job_execution import JobExecution

router = APIRouter()

@router.get("")
async def get_jobs(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # MVP: return latest 20 jobs
    query = select(JobExecution).order_by(JobExecution.started_at.desc()).limit(20)
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    # We will just return dicts for MVP instead of setting up full schemas
    return [
        {
            "id": j.id,
            "job_type": j.job_type,
            "keyword_id": j.keyword_id,
            "status": j.status,
            "started_at": j.started_at,
            "finished_at": j.finished_at,
            "duration_ms": j.duration_ms,
            "records_found": j.records_found,
            "error_message": j.error_message
        } for j in jobs
    ]
