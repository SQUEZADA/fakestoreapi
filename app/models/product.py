from typing import Any, Union
from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    name: str
    description: Union[str, None] = None
    price: int
    category: Union[int, None] = None
    userid: Union[str, None] = None

class Product_Fields(Product):
    id: Union[int, None] = None
    name: Union[str, None] = None
    price: Union[int, None] = None
    created_at: Union[str, None] = None
    categories: Union[dict, None] = None

try:
    Product.model_validate('not an object', from_attributes=True)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))