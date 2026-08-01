from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.keyword import KeywordStatus

class KeywordBase(BaseModel):
    keyword: str
    category: Optional[str] = None
    source: Optional[str] = "LinkedIn"
    priority: Optional[int] = 1
    status: Optional[KeywordStatus] = KeywordStatus.ACTIVE
    search_type: Optional[str] = "exact"
    notes: Optional[str] = None

class KeywordCreate(KeywordBase):
    pass

class KeywordUpdate(KeywordBase):
    keyword: Optional[str] = None

class KeywordResponse(KeywordBase):
    id: int
    last_run_at: Optional[datetime]
    last_result_count: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]

    class Config:
        from_attributes = True
