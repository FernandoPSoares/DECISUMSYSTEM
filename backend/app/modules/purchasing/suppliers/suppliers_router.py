# backend/app/modules/purchasing/suppliers/suppliers_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from . import suppliers_schemas, suppliers_service
from ....core.dependencies import get_db, require_permission
from .... import models

router = APIRouter(
    prefix="/fornecedores",
    tags=["Fornecedores"]
)

@router.post("/", response_model=suppliers_schemas.Fornecedor, summary="Criar um novo fornecedor")
def create_fornecedor_endpoint(
    fornecedor_in: suppliers_schemas.FornecedorCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("fornecedores:criar"))
):
    return suppliers_service.fornecedor_service.create(db=db, fornecedor_in=fornecedor_in)

@router.get("/", response_model=List[suppliers_schemas.Fornecedor], summary="Listar todos os fornecedores")
def read_fornecedores_endpoint(
    active_only: bool = True, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("fornecedores:ler"))
):
    return suppliers_service.fornecedor_service.get_all(db, skip=skip, limit=limit, active_only=active_only)

@router.get("/{fornecedor_id}", response_model=suppliers_schemas.Fornecedor, summary="Obter um fornecedor por ID")
def read_fornecedor_endpoint(
    fornecedor_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("fornecedores:ler"))
):
    return suppliers_service.fornecedor_service.get_by_id(db, fornecedor_id=fornecedor_id)

@router.put("/{fornecedor_id}", response_model=suppliers_schemas.Fornecedor, summary="Atualizar um fornecedor")
def update_fornecedor_endpoint(
    fornecedor_id: str, 
    fornecedor_in: suppliers_schemas.FornecedorUpdate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("fornecedores:editar"))
):
    return suppliers_service.fornecedor_service.update(db, fornecedor_id=fornecedor_id, fornecedor_in=fornecedor_in)

@router.put("/{fornecedor_id}/deactivate", response_model=suppliers_schemas.Fornecedor, summary="Desativar um fornecedor")
def deactivate_fornecedor_endpoint(
    fornecedor_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("fornecedores:ativar_desativar"))
):
    return suppliers_service.fornecedor_service.update_status(db, fornecedor_id=fornecedor_id, is_active=False)

@router.put("/{fornecedor_id}/activate", response_model=suppliers_schemas.Fornecedor, summary="Reativar um fornecedor")
def activate_fornecedor_endpoint(
    fornecedor_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("fornecedores:ativar_desativar"))
):
    return suppliers_service.fornecedor_service.update_status(db, fornecedor_id=fornecedor_id, is_active=True)
