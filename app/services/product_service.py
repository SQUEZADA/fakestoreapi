from typing import List, Union, Optional
from app.models.product import Product, ProductCreate, ProductUpdate
from app.config.supabase_config import supabase_client

class ProductService:
    def __init__(self):
        self.db = supabase_client

    def get_products(
        self,
        name: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 10
    ) -> List[Product]:
        query = self.db.table('products').select("*, categories(*)").limit(limit)
        
        if name:
            query = query.ilike("name", f"%{name}%")
        if category_id:
            query = query.eq("category_id", category_id)
        if min_price:
            query = query.gte("price", min_price)
        if max_price:
            query = query.lte("price", max_price)
            
        response = query.execute()
        return response.data

    def get_product_by_id(self, product_id: int) -> Product:
        response = self.db.table('products').select("*, categories(*)").eq('id', product_id).execute()
        
        if not response.data:
            raise ValueError(f"Product with ID {product_id} not found")
            
        return response.data[0]

    def create_product(self, product: ProductCreate) -> Product:
        response = self.db.table('products').insert(product.model_dump()).execute()
        
        if not response.data:
            raise ValueError("Failed to create product")
            
        return self.get_product_by_id(response.data[0]['id'])

    def update_product(self, product_id: int, product: ProductUpdate) -> Product:
        # Filter out None values
        update_data = {k: v for k, v in product.model_dump().items() if v is not None}
        
        response = self.db.table('products').update(update_data).eq('id', product_id).execute()
        
        if not response.data:
            raise ValueError(f"Product with ID {product_id} not found")
            
        return self.get_product_by_id(product_id)

    def delete_product(self, product_id: int) -> bool:
        response = self.db.table('products').delete().eq('id', product_id).execute()
        return len(response.data) > 0

    def get_products_by_category(self, category_id: int, limit: int = 10) -> List[Product]:
        response = self.db.table('products')\
            .select("*, categories(*)")\
            .eq('category_id', category_id)\
            .limit(limit)\
            .execute()
        return response.data 