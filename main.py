from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import Any, Union

# Models
from models.product import Product
from models.category import Category

# Supabase Connector
from supabase_config import supabase_client

app = FastAPI()

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
def read_products(name: Union[str, None] = None,category: Union[int, None] = None,price: int = 1, limit: int = 10):
    response = supabase_client.table('products').select("*,categories(name,slug)")
    
    if name != None:
        response = response.ilike("name",f'%25{name}%25')
    if category != None:
        response = response.eq("category",category)
    if price != None:
        response = response.gte("price",price)

    return response.limit(limit).execute().data

@app.get("/products/{item_id}")
def read_product(item_id: int, ):
    response = supabase_client.table('products').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.post("/products")
def create_product(product: Product):
    response = supabase_client.table('products').insert(product).execute()
    return response.data

@app.put("/products/{item_id}")
def update_product(item_id: int, product: Product):
    response = supabase_client.table('products').update(dict(product)).eq("id",item_id)
    return response.execute().data

@app.get("/categories")
def read_categories(name: Union[str, None] = None, limit: int = 10):
    response = supabase_client.table('categories').select("*,categories(name,slug)").limit(limit)
    if name != None:
        response = response.ilike("name",f'%25{name}%25')
    return response.execute().data

@app.get("/categories/{item_id}")
def read_categories(item_id: int):
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
