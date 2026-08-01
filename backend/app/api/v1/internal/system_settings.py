from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_admin, require_role
from app.schemas.system_settings import SystemSettingsCreate, SystemSettingsUpdate, SystemSettingsResponse
from app.services.system_settings import system_settings_service
from app.core.responses import StandardResponse, success_response

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[SystemSettingsResponse]])
async def get_all_settings(
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_role("admin"))
) -> Any:
    settings = await system_settings_service.get_multi(db)
    return success_response(data=settings)

@router.get("/{key}", response_model=StandardResponse[SystemSettingsResponse])
async def get_setting(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_role("admin"))
) -> Any:
    setting = await system_settings_service.get_by_key(db, key)
    return success_response(data=setting)

@router.post("/", response_model=StandardResponse[SystemSettingsResponse])
async def create_setting(
    setting_in: SystemSettingsCreate,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_role("admin"))
) -> Any:
    setting = await system_settings_service.create(db, obj_in=setting_in)
    return success_response(data=setting, message="Setting created")

@router.put("/{key}", response_model=StandardResponse[SystemSettingsResponse])
async def update_setting(
    key: str,
    setting_in: SystemSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(require_role("admin"))
) -> Any:
    db_obj = await system_settings_service.get_by_key(db, key)
    setting = await system_settings_service.update(db, id=db_obj.key, obj_in=setting_in)
    return success_response(data=setting, message="Setting updated")
