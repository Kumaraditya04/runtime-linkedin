from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.keyword import Keyword, KeywordStatus
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from app.utils.query_builder import apply_pagination_and_sort
from app.utils.pagination import PaginationParams

class KeywordRepository(BaseRepository[Keyword, KeywordCreate, KeywordUpdate]):
    async def get_multi_paginated(
        self, db: AsyncSession, params: PaginationParams, status_filter: KeywordStatus | None = None
    ) -> list[Keyword]:
        query = select(self.model)
        
        if status_filter:
            query = query.filter(self.model.status == status_filter)
            
        query = apply_pagination_and_sort(
            query=query, 
            params=params, 
            model=self.model, 
            search_fields=["keyword", "category"]
        )
        
        result = await db.execute(query)
        return result.scalars().all()

keyword_repo = KeywordRepository(Keyword)
