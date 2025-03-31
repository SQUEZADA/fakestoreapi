from typing import List, Optional
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.config.supabase_config import supabase_client

class CategoryService:
    def __init__(self):
        self.db = supabase_client

    def get_categories(self, name: Optional[str] = None, limit: int = 10) -> List[Category]:
        query = self.db.table('categories').select("*").limit(limit)
        
        if name:
            query = query.ilike("name", f"%{name}%")
            
        response = query.execute()
        return response.data

    def get_category_by_id(self, category_id: int) -> Category:
        response = self.db.table('categories').select("*").eq('id', category_id).execute()
        
        if not response.data:
            raise ValueError(f"Category with ID {category_id} not found")
            
        return response.data[0]

    def get_category_by_slug(self, slug: str) -> Category:
        response = self.db.table('categories').select("*").eq('slug', slug).execute()
        
        if not response.data:
            raise ValueError(f"Category with slug {slug} not found")
            
        return response.data[0]

    def create_category(self, category: CategoryCreate) -> Category:
        response = self.db.table('categories').insert(category.model_dump()).execute()
        
        if not response.data:
            raise ValueError("Failed to create category")
            
        return self.get_category_by_id(response.data[0]['id'])

    def update_category(self, category_id: int, category: CategoryUpdate) -> Category:
        # Filter out None values
        update_data = {k: v for k, v in category.model_dump().items() if v is not None}
        
        response = self.db.table('categories').update(update_data).eq('id', category_id).execute()
        
        if not response.data:
            raise ValueError(f"Category with ID {category_id} not found")
            
        return self.get_category_by_id(category_id)

    def delete_category(self, category_id: int) -> bool:
        # Check if category has products
        products = self.db.table('products').select("id").eq('category_id', category_id).execute()
        if products.data:
            raise ValueError("Cannot delete category with existing products")
            
        response = self.db.table('categories').delete().eq('id', category_id).execute()
        return len(response.data) > 0

    def get_category_products(self, category_id: int, limit: int = 10) -> List[dict]:
        response = self.db.table('products')\
            .select("*")\
            .eq('category_id', category_id)\
            .limit(limit)\
            .execute()
        return response.data 