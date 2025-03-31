from typing import List
from app.models.role import Role, RoleType
from app.config.supabase_config import supabase_client

class RoleService:
    def __init__(self):
        self.db = supabase_client

    def get_user_roles(self, user_id: int) -> List[Role]:
        response = self.db.table('user_roles')\
            .select("roles(*)")\
            .eq('user_id', user_id)\
            .execute()
        return [Role(**role['roles']) for role in response.data]

    def assign_role(self, user_id: int, role_id: int) -> bool:
        self.db.table('user_roles').insert({
            "user_id": user_id,
            "role_id": role_id
        }).execute()
        return True

    def remove_role(self, user_id: int, role_id: int) -> bool:
        self.db.table('user_roles')\
            .delete()\
            .eq('user_id', user_id)\
            .eq('role_id', role_id)\
            .execute()
        return True 