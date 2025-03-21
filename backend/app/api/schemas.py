from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_superuser: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginData(BaseModel):
    username: str
    password: str

class SongBase(BaseModel):
    title: str
    artist: str
    duration: int
    is_active: Optional[bool] = True

class SongCreate(SongBase):
    file_path: str

class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None

class Song(SongBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SongUpload(BaseModel):
    title: str
    artist: str
    duration: Optional[int] = None  # Será calculado automaticamente
    is_active: Optional[bool] = True

class SongUploadResponse(SongBase):
    id: int
    file_path: str
    duration: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True