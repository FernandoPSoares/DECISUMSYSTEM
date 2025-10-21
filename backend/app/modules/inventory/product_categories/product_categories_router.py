# backend/app/modules/inventory/product_categories/product_categories_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import product_categories_schemas, product_categories_service
from ....core.dependencies import get_db, require_permission
from .... import models

router = APIRouter(
    prefix="/inventory/categorias-produto",
    tags=["Inventário - Estrutura de Produtos"]
)

@router.post("/", response_model=product_categories_schemas.CategoriaProduto, status_code=status.HTTP_201_CREATED)
def create_categoria_produto_endpoint(obj_in: product_categories_schemas.CategoriaProdutoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return product_categories_service.product_category_service.create(db=db, obj_in=obj_in)

@router.get("/", response_model=List[product_categories_schemas.CategoriaProduto])
def read_categorias_produto_endpoint(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search: Optional[str] = None, sort_by: Optional[str] = None, sort_order: str = "asc", is_active: Optional[bool] = None, exclude_id: Optional[str] = None, current_user: models.Usuario = Depends(require_permission("inventory:read"))):
    return product_categories_service.product_category_service.get_all(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order, is_active=is_active, exclude_id=exclude_id)

@router.put("/{id}", response_model=product_categories_schemas.CategoriaProduto)
def update_categoria_produto_endpoint(id: str, obj_in: product_categories_schemas.CategoriaProdutoUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return product_categories_service.product_category_service.update(db, id=id, obj_in=obj_in)

@router.put("/{id}/deactivate", response_model=product_categories_schemas.CategoriaProduto)
def deactivate_categoria_produto_endpoint(id: str, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return product_categories_service.product_category_service.update_status(db, id=id, is_active=False)

@router.put("/{id}/activate", response_model=product_categories_schemas.CategoriaProduto)
def activate_categoria_produto_endpoint(id: str, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return product_categories_service.product_category_service.update_status(db, id=id, is_active=True)
