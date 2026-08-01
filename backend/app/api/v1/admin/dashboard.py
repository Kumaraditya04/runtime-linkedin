from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.database import get_db
from app.api.deps import get_current_admin
from app.models.keyword import Keyword, KeywordStatus

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # Total Keywords
    total_query = select(func.count(Keyword.id))
    total_result = await db.execute(total_query)
    total_keywords = total_result.scalar() or 0

    # Active Keywords
    active_query = select(func.count(Keyword.id)).where(Keyword.status == KeywordStatus.ACTIVE)
    active_result = await db.execute(active_query)
    active_keywords = active_result.scalar() or 0

    # Paused Keywords
    paused_query = select(func.count(Keyword.id)).where(Keyword.status == KeywordStatus.PAUSED)
    paused_result = await db.execute(paused_query)
    paused_keywords = paused_result.scalar() or 0

    # Future: Job execution metrics
    
    return {
        "total_keywords": total_keywords,
        "active_keywords": active_keywords,
        "paused_keywords": paused_keywords,
        "crawler_status": "Idle", # Placeholder
    }
