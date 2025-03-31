from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union
from app.models.product import Product, ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.dependencies.auth import get_current_user
from app.dependencies.rbac import require_roles
from app.models.role import RoleType
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])

def get_product_service():
    return ProductService()

@router.get("/", response_model=List[Product])
async def read_products(
    name: Union[str, None] = None,
    category_id: Union[int, None] = None,
    min_price: Union[float, None] = None,
    max_price: Union[float, None] = None,
    limit: int = 10,
    service: ProductService = Depends(get_product_service)
):
    try:
        return service.get_products(name, category_id, min_price, max_price, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=Product)
async def read_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    try:
        return service.get_product_by_id(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Product)
@require_roles([RoleType.ADMIN, RoleType.MANAGER])
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    try:
        return service.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", response_model=Product)
@require_roles([RoleType.ADMIN, RoleType.MANAGER])
async def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    try:
        return service.update_product(product_id, product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}")
@require_roles([RoleType.ADMIN])
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service)
):
    try:
        success = service.delete_product(product_id)
        if success:
            return {"message": f"Product {product_id} successfully deleted"}
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 