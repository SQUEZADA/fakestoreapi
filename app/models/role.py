from enum import Enum
from pydantic import BaseModel
from typing import List

class RoleType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class Role(BaseModel):
    id: int
    name: RoleType
    description: str

class UserRole(BaseModel):
    user_id: int
    role_id: int 


__all__ = ['Role', 'RoleType', 'UserRole']