from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.configurations.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    token = Column(String, index=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False) 
    expires_at = Column(DateTime, default=None, nullable=True)
    
    users = relationship("User", back_populates="tokens")


    def is_valid(self):
        return self.expires_at is None or self.expires_at > datetime.now(timezone.utc).replace(tzinfo=None)

    