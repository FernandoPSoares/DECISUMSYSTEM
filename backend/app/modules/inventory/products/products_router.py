# backend/app/modules/inventory/products/products_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from . import products_schemas, products_service
from ....core.dependencies import get_db, require_permission
from .... import models

router = APIRouter(
    prefix="/inventory/products",
    tags=["Inventário - Produtos"]
)

@router.post("/", response_model=products_schemas.Produto, status_code=status.HTTP_201_CREATED)
def create_produto_endpoint(
    obj_in: products_schemas.ProdutoCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return products_service.product_service.create(db=db, obj_in=obj_in)

@router.get("/", response_model=List[products_schemas.Produto])
def read_produtos_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    is_active: Optional[bool] = None,
    current_user: models.Usuario = Depends(require_permission("inventory:read"))
):
    return products_service.product_service.get_all(
        db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order
    )

@router.get("/{id}", response_model=products_schemas.Produto)
def read_produto_endpoint(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:read"))
):
    return products_service.product_service.get_by_id(db, produto_id=id)

@router.put("/{id}", response_model=products_schemas.Produto)
def update_produto_endpoint(
    id: uuid.UUID,
    obj_in: products_schemas.ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return products_service.product_service.update(db, produto_id=id, obj_in=obj_in)

@router.put("/{id}/deactivate", response_model=products_schemas.Produto)
def deactivate_produto_endpoint(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return products_service.product_service.update_status(db, produto_id=id, is_active=False)

@router.put("/{id}/activate", response_model=products_schemas.Produto)
def activate_produto_endpoint(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return products_service.product_service.update_status(db, produto_id=id, is_active=True)
