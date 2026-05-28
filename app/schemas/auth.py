# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from uuid import UUID
from enum import Enum


class Language(str, Enum):
    """Danh sách ngôn ngữ hỗ trợ"""
    ENGLISH = "en"
    VIETNAMESE = "vi"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    FRENCH = "fr"
    SPANISH = "es"
    PORTUGUESE = "pt"
    GERMAN = "de"
    RUSSIAN = "ru"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool = False  
    auth_provider: str = "local" 

class LoginResponse(BaseModel):
    """Response khi login thành công - rõ ràng và chuyên nghiệp"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    user_id: UUID


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRegister(BaseModel):
    """Schema đăng ký user"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    
    native_language: Language = Language.VIETNAMESE
    target_language: Language

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Chuyển email về chữ thường và loại bỏ khoảng trắng"""
        return v.lower().strip()

    @field_validator("target_language")
    @classmethod
    def validate_different_languages(cls, v: Language, info):
        """target_language phải khác native_language"""
        native = info.data.get("native_language")
        if native and v == native:
            raise ValueError("Target language must be different from native language")
        return v


class GoogleLogin(BaseModel):
    id_token: str

    class Config:
        from_attributes = True