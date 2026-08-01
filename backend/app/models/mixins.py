from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    """Mixin to add created_at and updated_at columns."""
    
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AuditMixin:
    """Mixin to add created_by and updated_by columns."""
    
    @declared_attr
    def created_by(cls):
        return Column(Integer, nullable=True) # ID of the admin/user

    @declared_attr
    def updated_by(cls):
        return Column(Integer, nullable=True)


class ActiveMixin:
    """Mixin to add is_active column."""
    
    @declared_attr
    def is_active(cls):
        return Column(Boolean, default=True, nullable=False)
