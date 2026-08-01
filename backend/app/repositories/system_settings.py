from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.system_settings import SystemSettings
from app.schemas.system_settings import SystemSettingsCreate, SystemSettingsUpdate

class SystemSettingsRepository(BaseRepository[SystemSettings, SystemSettingsCreate, SystemSettingsUpdate]):
    async def get_by_key(self, db: AsyncSession, key: str) -> SystemSettings | None:
        result = await db.execute(select(SystemSettings).filter(SystemSettings.key == key))
        return result.scalar_one_or_none()

system_settings_repo = SystemSettingsRepository(SystemSettings)
