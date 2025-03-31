from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService
from app.dependencies.auth import get_current_user
from app.dependencies.rbac import require_roles
from app.models.role import RoleType
from app.models.user import User
from app.models.product import Product

router = APIRouter(prefix="/categories", tags=["categories"])

def get_category_service():
    return CategoryService()

@router.get("/", response_model=List[Category])
async def read_categories(
    name: Union[str, None] = None,
    limit: int = 10,
    service: CategoryService = Depends(get_category_service)
):
    try:
        return service.get_categories(name, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{category_id}", response_model=Category)
async def read_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service)
):
    try:
        return service.get_category_by_id(category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{category_id}/products", response_model=List[Product])
async def read_category_products(
    category_id: int,
    limit: int = 10,
    service: CategoryService = Depends(get_category_service)
):
    try:
        return service.get_category_products(category_id, limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Category)
@require_roles([RoleType.ADMIN, RoleType.MANAGER])
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service)
):
    try:
        return service.create_category(category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{category_id}", response_model=Category)
@require_roles([RoleType.ADMIN, RoleType.MANAGER])
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service)
):
    try:
        return service.update_category(category_id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{category_id}")
@require_roles([RoleType.ADMIN])
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service)
):
    try:
        success = service.delete_category(category_id)
        if success:
            return {"message": f"Category {category_id} successfully deleted"}
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 