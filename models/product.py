from typing import Any, Union
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    category: Union[int, None] = None
    userid: Union[str, None] = None