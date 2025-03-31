from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .role import Role

class UserBase(BaseModel):
    email: EmailStr
    name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    roles: List[int] = []  # Role IDs

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    roles: Optional[List[int]] = None

class User(UserBase):
    id: int
    roles: List[Role] = []
    
    class Config:
        from_attributes = True

__all__ = ['User', 'UserCreate', 'UserUpdate', 'UserBase']