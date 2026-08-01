from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.keyword import Keyword, KeywordStatus
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from app.repositories.keyword import keyword_repo
from app.utils.pagination import PaginationParams

class KeywordService:
    @staticmethod
    async def get_keywords(
        db: AsyncSession, params: PaginationParams, status: Optional[KeywordStatus] = None
    ) -> List[Keyword]:
        return await keyword_repo.get_multi_paginated(db, params, status)

    @staticmethod
    async def get_keyword(db: AsyncSession, id: int) -> Keyword:
        keyword = await keyword_repo.get(db, id)
        if not keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        return keyword

    @staticmethod
    async def create_keyword(db: AsyncSession, obj_in: KeywordCreate) -> Keyword:
        return await keyword_repo.create(db, obj_in=obj_in)

    @staticmethod
    async def update_keyword(db: AsyncSession, id: int, obj_in: KeywordUpdate) -> Keyword:
        keyword = await keyword_repo.get(db, id)
        if not keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        return await keyword_repo.update(db, db_obj=keyword, obj_in=obj_in)

    @staticmethod
    async def delete_keyword(db: AsyncSession, id: int) -> Keyword:
        keyword = await keyword_repo.get(db, id)
        if not keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        return await keyword_repo.remove(db, id=id)
        
    @staticmethod
    async def change_status(db: AsyncSession, id: int, status: KeywordStatus) -> Keyword:
        keyword = await keyword_repo.get(db, id)
        if not keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        update_data = KeywordUpdate(status=status)
        return await keyword_repo.update(db, db_obj=keyword, obj_in=update_data)
