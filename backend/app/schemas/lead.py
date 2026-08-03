from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from app.models.lead import LeadStatus

class LeadBase(BaseModel):
    source: str
    keyword_id: Optional[int] = None
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    post_url: str
    post_text: Optional[str] = None
    published_at: Optional[datetime] = None
    intent_score: Optional[int] = None
    status: Optional[LeadStatus] = LeadStatus.NEW
    normalized_data: Optional[Any] = None
    raw_payload: Optional[Any] = None
    crawler_version: Optional[str] = None
    parser_version: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    post_url: Optional[str] = None
    source: Optional[str] = None

class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]

    class Config:
        from_attributes = True
