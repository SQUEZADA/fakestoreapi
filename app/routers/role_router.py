from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.role import Role, RoleType
from app.models.user import User
from app.services.role_service import RoleService
from app.dependencies.auth import get_current_user
from app.dependencies.rbac import require_roles

router = APIRouter(prefix="/roles", tags=["roles"])

def get_role_service():
    return RoleService()

@router.get("/user/{user_id}", response_model=List[Role])
@require_roles([RoleType.ADMIN, RoleType.MANAGER])
async def get_user_roles(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service)
):
    return service.get_user_roles(user_id)

@router.post("/user/{user_id}/role/{role_id}")
@require_roles([RoleType.ADMIN])
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service)
):
    try:
        service.assign_role(user_id, role_id)
        return {"message": "Role assigned successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 