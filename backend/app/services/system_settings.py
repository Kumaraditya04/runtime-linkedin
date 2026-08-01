from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.services.base import BaseService
from app.models.system_settings import SystemSettings
from app.schemas.system_settings import SystemSettingsCreate, SystemSettingsUpdate
from app.repositories.system_settings import system_settings_repo

class SystemSettingsService(BaseService[SystemSettings, SystemSettingsCreate, SystemSettingsUpdate]):
    async def get_by_key(self, db: AsyncSession, key: str) -> SystemSettings:
        obj = await self.repository.get_by_key(db, key)
        if not obj:
            raise HTTPException(status_code=404, detail="Setting not found")
        return obj
        
    async def get_by_key_or_none(self, db: AsyncSession, key: str) -> SystemSettings | None:
        return await self.repository.get_by_key(db, key)

system_settings_service = SystemSettingsService(system_settings_repo)
