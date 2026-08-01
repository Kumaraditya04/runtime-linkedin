import enum
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from app.database.database import Base
from app.models.mixins import TimestampMixin, AuditMixin

class KeywordStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"

class Keyword(Base, TimestampMixin, AuditMixin):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)
    source = Column(String, nullable=True, default="LinkedIn")
    priority = Column(Integer, default=1)
    status = Column(Enum(KeywordStatus), default=KeywordStatus.ACTIVE, nullable=False)
    search_type = Column(String, default="exact", nullable=False)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    last_result_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
