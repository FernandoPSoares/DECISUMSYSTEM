# backend/app/modules/production/work_centers/work_centers_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from . import work_centers_schemas, work_centers_service
from ....core.dependencies import get_db, require_permission
from .... import models

router = APIRouter(
    prefix="/centros-trabalho",
    tags=["Centros de Trabalho"]
)

@router.post("/", response_model=work_centers_schemas.CentroTrabalho, summary="Criar um novo centro de trabalho")
def create_centro_trabalho_endpoint(
    centro_trabalho_in: work_centers_schemas.CentroTrabalhoCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("centros_trabalho:criar"))
):
    return work_centers_service.centro_trabalho_service.create(db=db, centro_trabalho_in=centro_trabalho_in)

@router.get("/", response_model=List[work_centers_schemas.CentroTrabalho], summary="Listar centros de trabalho")
def read_centros_trabalho_endpoint(
    active_only: bool = True, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("centros_trabalho:ler"))
):
    return work_centers_service.centro_trabalho_service.get_all(db, skip=skip, limit=limit, active_only=active_only)

@router.get("/{centro_trabalho_id}", response_model=work_centers_schemas.CentroTrabalho, summary="Obter um centro de trabalho por ID")
def read_centro_trabalho_endpoint(
    centro_trabalho_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("centros_trabalho:ler"))
):
    return work_centers_service.centro_trabalho_service.get_by_id(db, centro_trabalho_id=centro_trabalho_id)

@router.put("/{centro_trabalho_id}", response_model=work_centers_schemas.CentroTrabalho, summary="Atualizar um centro de trabalho")
def update_centro_trabalho_endpoint(
    centro_trabalho_id: str, 
    centro_trabalho_in: work_centers_schemas.CentroTrabalhoUpdate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("centros_trabalho:editar"))
):
    return work_centers_service.centro_trabalho_service.update(db, centro_trabalho_id=centro_trabalho_id, centro_trabalho_in=centro_trabalho_in)

@router.put("/{centro_trabalho_id}/deactivate", response_model=work_centers_schemas.CentroTrabalho, summary="Desativar um centro de trabalho")
def deactivate_centro_trabalho_endpoint(
    centro_trabalho_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("centros_trabalho:ativar_desativar"))
):
    return work_centers_service.centro_trabalho_service.update_status(db, centro_trabalho_id=centro_trabalho_id, is_active=False)

@router.put("/{centro_trabalho_id}/activate", response_model=work_centers_schemas.CentroTrabalho, summary="Reativar um centro de trabalho")
def activate_centro_trabalho_endpoint(
    centro_trabalho_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("centros_trabalho:ativar_desativar"))
):
    return work_centers_service.centro_trabalho_service.update_status(db, centro_trabalho_id=centro_trabalho_id, is_active=True)
