from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SystemSettingsBase(BaseModel):
    value: str
    description: Optional[str] = None

class SystemSettingsCreate(SystemSettingsBase):
    key: str

class SystemSettingsUpdate(SystemSettingsBase):
    pass

class SystemSettingsResponse(SystemSettingsBase):
    key: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]

    class Config:
        from_attributes = True
