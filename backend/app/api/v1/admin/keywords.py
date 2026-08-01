from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.api.deps import get_current_admin
from app.models.keyword import KeywordStatus
from app.schemas.keyword import KeywordCreate, KeywordUpdate, KeywordResponse
from app.services.keyword import KeywordService
from app.utils.pagination import PaginationParams

router = APIRouter()

@router.get("", response_model=List[KeywordResponse])
async def get_keywords(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    search: Optional[str] = Query(None),
    status: Optional[KeywordStatus] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    params = PaginationParams(skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order, search=search)
    return await KeywordService.get_keywords(db=db, params=params, status=status)

@router.get("/{id}", response_model=KeywordResponse)
async def get_keyword(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    return await KeywordService.get_keyword(db=db, id=id)

@router.post("", response_model=KeywordResponse, status_code=201)
async def create_keyword(
    keyword_in: KeywordCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await KeywordService.create_keyword(db=db, obj_in=keyword_in)

@router.put("/{id}", response_model=KeywordResponse)
async def update_keyword(
    keyword_in: KeywordUpdate,
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await KeywordService.update_keyword(db=db, id=id, obj_in=keyword_in)

@router.delete("/{id}", response_model=KeywordResponse)
async def delete_keyword(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await KeywordService.delete_keyword(db=db, id=id)

@router.post("/{id}/pause", response_model=KeywordResponse)
async def pause_keyword(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await KeywordService.change_status(db=db, id=id, status=KeywordStatus.PAUSED)

@router.post("/{id}/resume", response_model=KeywordResponse)
async def resume_keyword(
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await KeywordService.change_status(db=db, id=id, status=KeywordStatus.ACTIVE)

@router.post("/test", status_code=200)
async def test_keyword(
    keyword_in: KeywordCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # Future integration with crawler module to test the search live
    return {"message": f"Test successful for keyword: {keyword_in.keyword}", "estimated_results": 42}
