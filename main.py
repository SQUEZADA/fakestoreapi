from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

# from json import dumps,loads

from supabase_config import supabase_client

app = FastAPI()

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: int | None = None
    userid: str | None = None

class Category(BaseModel):
    name: str
    slug: str
    parent_category:  int | None = None

@app.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """

@app.get("/products")
def read_products():
    response = supabase_client.table('products').select("*,categories(name,slug)").execute()
    return response.data

@app.get("/products/{item_id}")
def read_product(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('products').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.post("/products")
def create_product(product: Product):
    response = supabase_client.table('products').insert(product).execute()
    return response.data

@app.put("/products/{item_id}")
def update_product(item_id: int, product: Product):
    response = supabase_client.table('products').update(dict(product)).eq("id",item_id).execute()
    return response.data

@app.get("/categories")
def read_categories():
    response = supabase_client.table('categories').select("*,categories(name,slug)").execute()
    return response.data

@app.get("/categories/{item_id}")
def read_categories(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('categories').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.post("/categories")
def create_categories(category: Category):
    response = supabase_client.table('categories').insert(category).execute()
    return response.data

@app.put("/categories/{item_id}")
def update_categories(item_id: int, category: Category):
    response = supabase_client.table('categories').update(category).eq("id",item_id).execute()
    return response.data

@app.get("/users")
def read_categories():
    response = supabase_client.table('categories').select("*,categories(name,slug)").execute()
    return response.data

@app.get("/users/{item_id}")
def read_categories(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('categories').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data
