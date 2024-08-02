from typing import Any, Union
from pydantic import BaseModel

class Category(BaseModel):
    name: str
    slug: str
    parent_category:  Union[int, None] = None

class Category_Fields(Category):
    name: Union[str, None] = None
    slug: Union[str, None] = None