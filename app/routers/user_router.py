from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union
from app.models.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user
from app.dependencies.rbac import require_roles
from app.models.role import RoleType

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service():
    return UserService()

@router.get("/", response_model=List[User])
@require_roles([RoleType.ADMIN, RoleType.MANAGER])
async def read_users(
    name: Union[str, None] = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    try:
        return service.get_users(name, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        return service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=User)
@require_roles([RoleType.ADMIN])
async def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    try:
        return service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        return service.update_user(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
@require_roles([RoleType.ADMIN])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service)
):
    try:
        success = service.delete_user(user_id)
        if success:
            return {"message": f"User {user_id} successfully deleted"}
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 