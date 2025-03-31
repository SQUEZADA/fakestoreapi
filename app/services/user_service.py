from typing import List, Union
from app.models import User
from app.config.supabase_config import supabase_client
from app.services.role_service import RoleService
from app.models.role import RoleType

class UserService:
    def __init__(self):
        self.db = supabase_client
        self.role_service = RoleService()

    def get_users(self, name: Union[str, None], limit: int = 10) -> List[User]:
        query = self.db.table('users').select("*")
        if name:
            query = query.ilike("name", f'%25{name}%25')
        return query.limit(limit).execute().data

    def get_user_by_id(self, user_id: int) -> User:
        response = self.db.table('users').select("*").eq('id', user_id).execute()
        if not response.data:
            raise ValueError(f"User with ID {user_id} not found")
        
        user_data = response.data[0]
        user_data['roles'] = self.role_service.get_user_roles(user_id)
        return User(**user_data)

    def create_user(self, user: User) -> User:
        # Create user
        created_user = self.db.table('users').insert(dict(user)).execute().data[0]

        # Assign default role if no roles specified
        if not user.roles:
            default_role = self.db.table('roles').select("*").eq('name', RoleType.USER).execute().data[0]
            self.role_service.assign_role(created_user['id'], default_role['id'])
        else:
            # Assign specified roles
            for role_id in user.roles:
                self.role_service.assign_role(created_user['id'], role_id)

        return self.get_user_by_id(created_user['id'])

    def update_user(self, user_id: int, user: User) -> User:
        return self.db.table('users').update(dict(user)).eq("id", user_id).execute().data[0]

    def delete_user(self, user_id: int) -> bool:
        response = self.db.table('users').delete().eq("id", user_id).execute()
        return len(response.data) > 0

    def get_user_by_email(self, email: str) -> User:
        response = self.db.table('users').select("*").eq('email', email).execute()
        if not response.data:
            raise ValueError(f"User with email {email} not found")
        return response.data[0] 