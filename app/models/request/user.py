import re
from datetime import datetime, date
from typing import Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utils.password import validate_password_complexity



class UserBase(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    fixed_phone: Union[str, None] = Field(None, min_length=10, max_length=15)
    birth_day: Union[date, None] = None
    role_id: UUID
    company: Union[str, None] = None
    country: Union[str, None] = None
    company_type: Union[str, None] = None
    professional_category: Union[str, None] = None
    sub_category: Union[str, None] = None
    website: Union[str, None] = None
    password: str = Field(..., min_length=8, max_length=50)

    @field_validator('password')
    def password_password(cls, value: str) -> str:
        if not validate_password_complexity(value):
            raise ValueError(
                'Password must be at least 8 characters long, include an uppercase letter, '
                'a lowercase letter, a digit, and a special character.'
            )
        return value

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_day: Union[date, None] = None
    role_id: UUID
    fixed_phone: Union[str, None] = None
    company: Union[str, None] = None
    country: Union[str, None] = None
    company_type: Union[str, None] = None
    professional_category: Union[str, None] = None
    sub_category: Union[str, None] = None
    website: Union[str, None] = None
    created_at: datetime
    is_active: bool

    
    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    email: EmailStr
    new_password: str
    otp: str

    @field_validator('new_password')
    def password_new_password(cls, value: str) -> str:
        if not validate_password_complexity(value):
            raise ValueError(
                'Password must be at least 8 characters long, include an uppercase letter, '
                'a lowercase letter, a digit, and a special character.'
            )
        return value

class PasswordChangeRequest(BaseModel):
    email: EmailStr
    current_password: str
    new_password: str

    @field_validator('new_password')
    def password_complexity(cls, value: str) -> str:
        if not validate_password_complexity(value):
            raise ValueError(
                'Password must be at least 8 characters long, include an uppercase letter, '
                'a lowercase letter, a digit, and a special character.'
            )
        return value



