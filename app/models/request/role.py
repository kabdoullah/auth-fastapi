from uuid import UUID
from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    id: UUID
    name: str


class RoleCreate(BaseModel):
    name: str  = Field(..., min_length=3, max_length=30)

    class Config:
        from_attributes = True
