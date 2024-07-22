from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenCreate(BaseModel):
    token: str
    user_id: UUID
    expires_at: datetime

class TokenData(BaseModel):
    user_id: UUID