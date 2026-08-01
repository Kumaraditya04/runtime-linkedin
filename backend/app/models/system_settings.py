from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base
from app.models.mixins import TimestampMixin, AuditMixin

class SystemSettings(Base, TimestampMixin, AuditMixin):
    """
    Stores global application settings. 
    Only one row (id=1) should ideally exist, or key-value pairs if preferred.
    We will use a Key-Value pair pattern for flexibility.
    """
    __tablename__ = "system_settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)
    description = Column(String, nullable=True)
