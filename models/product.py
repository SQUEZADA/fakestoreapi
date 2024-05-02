from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: int | None = None
    userid: str | None = None