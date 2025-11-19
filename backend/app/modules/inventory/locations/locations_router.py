# backend/app/modules/inventory/locations/locations_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from . import locations_schemas, locations_service
from ....core.dependencies import get_db, require_permission
from .... import models

# --- Roteador para Tipos de Local ---
router_tipos_local = APIRouter(
    prefix="/tipos-local",
    tags=["Estrutura Logística"]
)

@router_tipos_local.post("/", response_model=locations_schemas.TipoLocal, summary="Criar um novo tipo de local")
def create_tipo_local_endpoint(
    tipo_local_in: locations_schemas.TipoLocalCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:criar"))
):
    return locations_service.local_service.create_tipo_local(db=db, tipo_local_in=tipo_local_in)

@router_tipos_local.get("/", response_model=List[locations_schemas.TipoLocal], summary="Listar tipos de local")
def read_tipos_local_endpoint(
    active_only: bool = True, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ler"))
):
    return locations_service.local_service.get_all_tipos_local(db, skip=0, limit=1000, active_only=active_only)

@router_tipos_local.put("/{tipo_local_id}", response_model=locations_schemas.TipoLocal, summary="Atualizar um tipo de local")
def update_tipo_local_endpoint(
    tipo_local_id: str, tipo_local_in: locations_schemas.TipoLocalUpdate, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:editar"))
):
    return locations_service.local_service.update_tipo_local(db, tipo_local_id=tipo_local_id, tipo_local_in=tipo_local_in)

@router_tipos_local.put("/{tipo_local_id}/deactivate", response_model=locations_schemas.TipoLocal, summary="Desativar um tipo de local")
def deactivate_tipo_local_endpoint(
    tipo_local_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ativar_desativar"))
):
    return locations_service.local_service.update_tipo_local_status(db, tipo_local_id=tipo_local_id, is_active=False)

@router_tipos_local.put("/{tipo_local_id}/activate", response_model=locations_schemas.TipoLocal, summary="Reativar um tipo de local")
def activate_tipo_local_endpoint(
    tipo_local_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ativar_desativar"))
):
    return locations_service.local_service.update_tipo_local_status(db, tipo_local_id=tipo_local_id, is_active=True)

# --- Roteador para Locais ---
router_locais = APIRouter(
    prefix="/locais",
    tags=["Estrutura Logística"]
)

@router_locais.post("/", response_model=locations_schemas.Local, summary="Criar um novo local")
def create_local_endpoint(
    local_in: locations_schemas.LocalCreate, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:criar"))
):
    return locations_service.local_service.create_local(db=db, local_in=local_in)

@router_locais.get("/", response_model=List[locations_schemas.Local], summary="Listar locais")
def read_locais_endpoint(
    active_only: bool = True, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ler"))
):
    return locations_service.local_service.get_all_locais(db, skip=skip, limit=limit, active_only=active_only)

@router_locais.get("/{local_id}", response_model=locations_schemas.Local, summary="Obter um local por ID")
def read_local_endpoint(
    local_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ler"))
):
    return locations_service.local_service.get_local_by_id(db, local_id=local_id)

@router_locais.put("/{local_id}", response_model=locations_schemas.Local, summary="Atualizar um local")
def update_local_endpoint(
    local_id: str, local_in: locations_schemas.LocalUpdate, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:editar"))
):
    return locations_service.local_service.update_local(db, local_id=local_id, local_in=local_in)

@router_locais.put("/{local_id}/deactivate", response_model=locations_schemas.Local, summary="Desativar um local")
def deactivate_local_endpoint(
    local_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ativar_desativar"))
):
    return locations_service.local_service.update_local_status(db, local_id=local_id, is_active=False)

@router_locais.put("/{local_id}/activate", response_model=locations_schemas.Local, summary="Reativar um local")
def activate_local_endpoint(
    local_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("locais:ativar_desativar"))
):
    return locations_service.local_service.update_local_status(db, local_id=local_id, is_active=True)
