# backend/app/modules/inventory/brands/brands_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import brands_schemas, brands_service
from ....core.dependencies import get_db, require_permission
from .... import models

router = APIRouter(
    prefix="/inventory/brands",
    tags=["Inventário - Estrutura de Produtos"]
)

@router.post("/", response_model=brands_schemas.Marca, status_code=status.HTTP_201_CREATED, summary="Criar uma nova Marca")
def create_marca_endpoint(
    obj_in: brands_schemas.MarcaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return brands_service.marca_service.create(db=db, marca_in=obj_in)

@router.get("/", response_model=List[brands_schemas.Marca], summary="Listar Marcas")
def read_marcas_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    is_active: Optional[bool] = None,
    current_user: models.Usuario = Depends(require_permission("inventory:read"))
):
    return brands_service.marca_service.get_all(
        db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order
    )

@router.put("/{id}", response_model=brands_schemas.Marca, summary="Atualizar uma Marca")
def update_marca_endpoint(
    id: str,
    obj_in: brands_schemas.MarcaUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return brands_service.marca_service.update(db, marca_id=id, marca_in=obj_in)

@router.put("/{id}/deactivate", response_model=brands_schemas.Marca, summary="Desativar uma Marca")
def deactivate_marca_endpoint(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return brands_service.marca_service.update_status(db, marca_id=id, is_active=False)

@router.put("/{id}/activate", response_model=brands_schemas.Marca, summary="Reativar uma Marca")
def activate_marca_endpoint(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("inventory:admin"))
):
    return brands_service.marca_service.update_status(db, marca_id=id, is_active=True)
