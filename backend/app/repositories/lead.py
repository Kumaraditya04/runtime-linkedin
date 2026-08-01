from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate
from app.utils.query_builder import apply_pagination_and_sort
from app.utils.pagination import PaginationParams

class LeadRepository(BaseRepository[Lead, LeadCreate, LeadUpdate]):
    async def get_multi_paginated(
        self, db: AsyncSession, params: PaginationParams
    ) -> list[Lead]:
        query = select(self.model)
        
        query = apply_pagination_and_sort(
            query=query, 
            params=params, 
            model=self.model, 
            search_fields=["author_name", "post_text"]
        )
        
        result = await db.execute(query)
        return result.scalars().all()

lead_repo = LeadRepository(Lead)
