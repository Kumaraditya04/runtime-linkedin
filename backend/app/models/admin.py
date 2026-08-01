from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="admin", nullable=False) # RBAC ready: admin, manager, sales, viewer
    is_active = Column(Boolean, default=True)
