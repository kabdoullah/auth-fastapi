import uuid
from sqlalchemy import Column, String, DateTime, func, Boolean, Date, ForeignKey
from app.configurations.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    fixed_phone = Column(String, nullable=True)
    birth_day = Column(Date, nullable=True)
    role_id = Column(UUID, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    company = Column(String, nullable=True)
    country = Column(String, nullable=True)
    company_type = Column(String, nullable=True)
    professional_category = Column(String, nullable=True)
    sub_category = Column(String, nullable=True)
    website = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="users")
    tokens = relationship("Token", back_populates="users")
    otps = relationship("OTP", back_populates="users")








