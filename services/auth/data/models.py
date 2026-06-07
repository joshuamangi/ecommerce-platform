from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB

from data.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    permissions = Column(JSONB, nullable=False, default=list)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
