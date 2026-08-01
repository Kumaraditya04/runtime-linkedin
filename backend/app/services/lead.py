from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate
from app.repositories.lead import lead_repo
from app.utils.pagination import PaginationParams

class LeadService:
    @staticmethod
    async def get_leads(
        db: AsyncSession, params: Optional[PaginationParams] = None
    ) -> List[Lead]:
        if params is None:
            return await lead_repo.get_multi(db)
        return await lead_repo.get_multi_paginated(db, params)

    @staticmethod
    async def get_lead(db: AsyncSession, id: int) -> Lead:
        lead = await lead_repo.get(db, id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        return lead

    @staticmethod
    async def create_lead(db: AsyncSession, obj_in: LeadCreate) -> Lead:
        return await lead_repo.create(db, obj_in=obj_in)
