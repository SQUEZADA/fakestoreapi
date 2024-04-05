from typing import Union

from fastapi import FastAPI

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase_client: Client = create_client(url, key)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/products")
def read_products():
    response = supabase_client.table('products').select("*, categories(name,slug)").execute()
    return response.data

@app.get("/products/{item_id}")
def read_product(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('products').select("*, categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.get("/categories/{item_id}")
def read_categories(item_id: int, q: Union[str, None] = None):
    response = supabase_client.table('categories').select("*,categories(name,slug)").eq('id', item_id).execute()
    return response.data

@app.get("/categories")
def read_categories():
    response = supabase_client.table('categories').select("*,categories(name,slug)").execute()
    return response.data