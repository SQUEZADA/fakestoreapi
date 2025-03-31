from typing import Any, Union, Optional, List
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str
    slug: str
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

__all__ = ['Category', 'CategoryCreate', 'CategoryUpdate', 'CategoryBase']

class Category_Fields(Category):
    name: Union[str, None] = None
    slug: Union[str, None] = None