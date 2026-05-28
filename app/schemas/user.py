from pydantic import BaseModel, EmailStr, Fieldfrom, ConfigDict
from typing import Optional
from uuid import UUID



class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: UUID
    is_active: boolS
    model_config = ConfigDict(from_attributes=True)