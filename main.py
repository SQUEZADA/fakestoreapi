from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import supabase_client

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
def read_products():
    response = supabase_client.table('products').select("*, categories(name,slug)").execute()
    return response.data

@app.get("/products/{item_id}")
def read_product(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('products').select("*, categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.get("/categories")
def read_categories():
    response = supabase_client.table('categories').select("*,categories(name,slug)").execute()
    return response.data

@app.get("/categories/{item_id}")
def read_categories(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('categories').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.get("/users")
def read_categories():
    response = supabase_client.table('categories').select("*,categories(name,slug)").execute()
    return response.data

@app.get("/users/{item_id}")
def read_categories(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('categories').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data
