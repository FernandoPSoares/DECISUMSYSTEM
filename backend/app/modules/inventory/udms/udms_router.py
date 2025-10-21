# backend/app/modules/inventory/udms/udms_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import udms_schemas, udms_service
from ....core.dependencies import get_db, require_permission
from .... import models

# Roteador para Categorias de UDM
router_categorias_udm = APIRouter(
    prefix="/inventory/categorias-udm",
    tags=["Inventário - Estrutura de Produtos"]
)

@router_categorias_udm.post("/", response_model=udms_schemas.CategoriaUdm, status_code=status.HTTP_201_CREATED, summary="Criar uma nova Categoria de UDM")
def create_categoria_udm_endpoint(obj_in: udms_schemas.CategoriaUdmCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.create_categoria_udm(db=db, categoria_in=obj_in)

@router_categorias_udm.get("/", response_model=List[udms_schemas.CategoriaUdmDetail], summary="Listar Categorias de UDM com as suas UDMs")
def read_categorias_udm_endpoint(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search: Optional[str] = None, sort_by: Optional[str] = None, sort_order: str = "asc", is_active: Optional[bool] = None, current_user: models.Usuario = Depends(require_permission("inventory:read"))):
    return udms_service.udm_service.get_all_categorias_udm(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order, is_active=is_active)

@router_categorias_udm.put("/{id}", response_model=udms_schemas.CategoriaUdm, summary="Atualizar uma Categoria de UDM")
def update_categoria_udm_endpoint(id: str, obj_in: udms_schemas.CategoriaUdmUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.update_categoria_udm(db, id=id, obj_in=obj_in)

@router_categorias_udm.put("/{id}/change-reference", response_model=udms_schemas.CategoriaUdmDetail, summary="Alterar a UDM de Referência de uma Categoria")
def change_reference_udm_endpoint(id: str, request_body: udms_schemas.ChangeReferenceUdmRequest, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.change_reference_udm(db, category_id=id, new_ref_udm_id=request_body.new_reference_udm_id)

@router_categorias_udm.put("/{id}/deactivate", response_model=udms_schemas.CategoriaUdm, summary="Desativar uma Categoria de UDM")
def deactivate_categoria_udm_endpoint(id: str, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.update_categoria_udm_status(db, id=id, is_active=False)

@router_categorias_udm.put("/{id}/activate", response_model=udms_schemas.CategoriaUdm, summary="Reativar uma Categoria de UDM")
def activate_categoria_udm_endpoint(id: str, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.update_categoria_udm_status(db, id=id, is_active=True)

# Roteador para Unidades de Medida (UDM)
router_udm = APIRouter(
    prefix="/inventory/udm",
    tags=["Inventário - Estrutura de Produtos"]
)

@router_udm.post("/", response_model=udms_schemas.Udm, status_code=status.HTTP_201_CREATED, summary="Criar uma nova Unidade de Medida")
def create_udm_endpoint(obj_in: udms_schemas.UdmCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.create_udm(db=db, udm_in=obj_in)

@router_udm.get("/", response_model=List[udms_schemas.Udm], summary="Listar Unidades de Medida")
def read_udm_endpoint(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search: Optional[str] = None, sort_by: Optional[str] = None, sort_order: str = "asc", is_active: Optional[bool] = None, current_user: models.Usuario = Depends(require_permission("inventory:read"))):
    return udms_service.udm_service.get_all_udm(db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order, is_active=is_active)
    
@router_udm.put("/{id}", response_model=udms_schemas.Udm, summary="Atualizar uma Unidade de Medida")
def update_udm_endpoint(id: str, obj_in: udms_schemas.UdmUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.update_udm(db, id=id, obj_in=obj_in)

@router_udm.put("/{id}/deactivate", response_model=udms_schemas.Udm, summary="Desativar uma Unidade de Medida")
def deactivate_udm_endpoint(id: str, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.update_udm_status(db, udm_id=id, is_active=False)

@router_udm.put("/{id}/activate", response_model=udms_schemas.Udm, summary="Reativar uma Unidade de Medida")
def activate_udm_endpoint(id: str, db: Session = Depends(get_db), current_user: models.Usuario = Depends(require_permission("inventory:admin"))):
    return udms_service.udm_service.update_udm_status(db, udm_id=id, is_active=True)
