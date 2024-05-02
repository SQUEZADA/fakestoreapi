from pydantic import BaseModel

class Category(BaseModel):
    name: str
    slug: str
    parent_category:  int | None = None

class CategoryFilters(BaseModel):
    name: str | None = None
    slug: str | None = None
    parent_category:  int | None = None