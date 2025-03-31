from typing import List
from functools import wraps
from fastapi import HTTPException, status
from app.models.role import RoleType
from app.models.user import User

def require_roles(allowed_roles: List[RoleType]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            user_roles = [role.name for role in current_user.roles]
            if not any(role in allowed_roles for role in user_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator 