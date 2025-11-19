# File: backend/app/modules/maintenance/assets/assets_router.py

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, Body, status

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario

# Importa os schemas e o serviço da fatia "Assets"
from .assets_schemas import AssetRead, AssetCreate, AssetUpdate
from .assets_service import asset_service, AssetService

# --- CORREÇÃO AQUI ---
# Alterado de "/maintenance/assets" para "/assets".
# O prefixo "/maintenance" já vem do router pai em api_router.py
router = APIRouter(
    prefix="/assets",
    tags=["Maintenance - Assets"],
    dependencies=[Depends(get_current_active_user)] # Protege todos os endpoints
)
# --- FIM DA CORREÇÃO ---

@router.post(
    "/",
    response_model=AssetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo Ativo"
)
def create_asset(
    asset_in: AssetCreate = Body(...),
    db: Session = Depends(get_db),
    # current_user: Usuario = Depends(get_current_active_user) # (Opcional, se precisar do ID do criador)
):
    """
    Cria um novo ativo (equipamento, máquina, componente) no CMMS.
    
    A lógica de negócio no 'service' validará:
    - Unicidade da TAG Interna.
    - Unicidade do Número de Série (se fornecido).
    - Existência de Local, Fabricante ou Ativo Pai (se fornecidos).
    """
    return asset_service.create_asset(db=db, obj_in=asset_in)


@router.get(
    "/",
    response_model=List[AssetRead],
    summary="Listar Ativos"
)
def read_assets(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registos a pular"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registos a retornar"),
    search: Optional[str] = Query(None, description="Pesquisa em campos de texto (nome, tag, serial, descrição)"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar (ex: 'name', 'location.name')"),
    sort_order: str = Query("asc", description="Ordem de ordenação: 'asc' ou 'desc'")
):
    """
    Obtém uma lista de ativos com filtros de paginação, busca e ordenação.
    
    Nota: O 'asset_model' ainda não possui 'is_active', portanto, 
    este endpoint retornará todos os ativos (não inativos).
    """
    return asset_service.get_assets(
        db=db, 
        skip=skip, 
        limit=limit, 
        search=search, 
        sort_by=sort_by, 
        sort_order=sort_order
    )


@router.get(
    "/{asset_id}",
    response_model=AssetRead,
    summary="Obter Ativo por ID"
)
def read_asset(
    asset_id: uuid.UUID = Path(..., description="ID do Ativo"),
    db: Session = Depends(get_db)
):
    """
    Obtém os detalhes completos de um ativo específico pelo seu ID.
    Levanta um erro 404 se o ativo não for encontrado.
    """
    return asset_service.get_asset(db=db, asset_id=asset_id)


@router.put(
    "/{asset_id}",
    response_model=AssetRead,
    summary="Atualizar Ativo"
)
def update_asset(
    asset_id: uuid.UUID = Path(..., description="ID do Ativo a atualizar"),
    asset_in: AssetUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Atualiza os detalhes de um ativo existente.
    
    A lógica de negócio no 'service' validará:
    - Unicidade de TAG Interna e N/S (se alterados).
    - Existência de FKs (se alterados).
    - Prevenção de hierarquia cíclica (ativo não pode ser pai de si mesmo).
    """
    return asset_service.update_asset(db=db, asset_id=asset_id, obj_in=asset_in)


@router.delete(
    "/{asset_id}",
    response_model=AssetRead,
    summary="Eliminar Ativo"
)
def delete_asset(
    asset_id: uuid.UUID = Path(..., description="ID do Ativo a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina um ativo (HARD DELETE).
    
    A lógica de negócio no 'service' **impedirá** a eliminação (Erro 400) se:
    - O ativo possuir Ordens de Serviço (histórico).
    - O ativo possuir Planos de Manutenção Preventiva.
    - O ativo possuir Ativos Filhos (sub-ativos).
    """
    return asset_service.delete_asset(db=db, asset_id=asset_id)