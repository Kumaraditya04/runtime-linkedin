import enum
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.mixins import TimestampMixin, AuditMixin
from app.models.keyword import Keyword

class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    REVIEWED = "REVIEWED"
    CONTACTED = "CONTACTED"

class Lead(Base, TimestampMixin, AuditMixin):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True, nullable=False, default="linkedin")
    keyword_id = Column(Integer, ForeignKey("keywords.id"), nullable=True)
    author_name = Column(String, nullable=True)
    author_url = Column(String, nullable=True)
    post_url = Column(String, index=True, nullable=False) # Removed unique=True to allow deduplication via fingerprint instead
    fingerprint = Column(String(64), unique=True, index=True, nullable=True) # SHA-256 Hash
    post_text = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    intent_score = Column(Integer, nullable=True)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    
    normalized_data = Column(JSON, nullable=True)
    raw_payload = Column(JSON, nullable=True)
    crawler_version = Column(String, nullable=True)
    parser_version = Column(String, nullable=True)

    keyword = relationship("Keyword")
