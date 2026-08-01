from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.database.database import Base
from app.models.mixins import TimestampMixin
from app.models.keyword import Keyword

class JobStatus(str, enum.Enum):
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    PARSING = "PARSING"
    SAVING = "SAVING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class JobErrorCategory(str, enum.Enum):
    AUTH_FAILED = "AUTH_FAILED"
    TIMEOUT = "TIMEOUT"
    RATE_LIMITED = "RATE_LIMITED"
    SELECTOR_CHANGED = "SELECTOR_CHANGED"
    NETWORK_ERROR = "NETWORK_ERROR"
    UNKNOWN = "UNKNOWN"

class JobExecution(Base, TimestampMixin):
    __tablename__ = "job_executions"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String, index=True, nullable=False)
    keyword_id = Column(Integer, ForeignKey("keywords.id"), nullable=True)
    status = Column(SQLEnum(JobStatus), index=True, nullable=False, default=JobStatus.STARTING)
    started_at = Column(DateTime(timezone=True), nullable=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    records_found = Column(Integer, default=0)
    records_saved = Column(Integer, default=0)
    records_skipped = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    error_category = Column(SQLEnum(JobErrorCategory), nullable=True)
    retry_count = Column(Integer, default=0)

    keyword = relationship("Keyword")
