from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.api.deps import get_current_admin
from app.schemas.lead import LeadResponse
from app.services.lead import LeadService
from app.utils.pagination import PaginationParams

router = APIRouter()

@router.get("", response_model=List[LeadResponse])
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    params = PaginationParams(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, search=search)
    return await LeadService.get_leads(db=db, params=params)

@router.get("/{id}", response_model=LeadResponse)
async def get_lead(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await LeadService.get_lead(db=db, id=id)
