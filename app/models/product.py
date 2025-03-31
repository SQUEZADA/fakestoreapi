from pydantic import BaseModel
from typing import Optional, List
from .category import Category

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    stock: int = 0
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int
    category: Optional[Category] = None

    class Config:
        from_attributes = True

__all__ = ['Product', 'ProductCreate', 'ProductUpdate', 'ProductBase']