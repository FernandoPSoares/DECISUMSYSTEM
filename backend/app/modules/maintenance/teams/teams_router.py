# File: backend/app/modules/maintenance/teams/teams_router.py

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Dependências centrais do seu projeto
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario # Para o type hint do Depends

# Componentes desta "fatia" (slice)
from .teams_service import maintenance_team_service
from .teams_schemas import (
    MaintenanceTeamRead,
    MaintenanceTeamReadSimple,
    MaintenanceTeamCreate,
    MaintenanceTeamUpdate
)

# --- Definição do Router da Fatia ---

# O prefixo '/maintenance/teams' garante que todos os endpoints aqui
# estarão em /maintenance/teams/..., seguindo a sua arquitetura.
router = APIRouter(
    prefix="/teams",
    tags=["Manutenção - Equipes"],
    # Todos os endpoints nesta fatia exigem um utilizador autenticado
    dependencies=[Depends(get_current_active_user)]
)

# --- Endpoints ---

@router.post(
    "/",
    response_model=MaintenanceTeamRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova Equipa",
    description="Cria uma nova equipa de manutenção."
)
def create_team(
    *,
    db: Session = Depends(get_db),
    team_in: MaintenanceTeamCreate,
    current_user: Usuario = Depends(get_current_active_user) # Para verificação de permissões futuras
):
    """
    Cria uma nova equipa de manutenção.
    
    - **db**: Sessão da base de dados.
    - **team_in**: Dados de criação (nome).
    - **current_user**: Utilizador autenticado (para futuras verificações de permissões).
    """
    # (Ponto futuro: Adicionar verificação de permissões aqui, ex:)
    # if not user_has_permission(current_user, "team:create"):
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, "Sem permissão.")
        
    # O serviço trata de toda a lógica de negócio (validação de nome duplicado, etc.)
    return maintenance_team_service.create_team(db=db, team_in=team_in)

@router.get(
    "/",
    response_model=List[MaintenanceTeamReadSimple],
    summary="Listar todas as Equipas",
    description="Obtém uma lista paginada de todas as equipas de manutenção ativas."
)
def read_teams(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtém uma lista paginada de equipas (apenas ativas por defeito).
    """
    return maintenance_team_service.get_all_teams(db=db, skip=skip, limit=limit)

@router.get(
    "/{team_id}",
    response_model=MaintenanceTeamRead,
    summary="Obter uma Equipa por ID",
    description="Obtém os detalhes de uma equipa de manutenção específica."
)
def read_team(
    *,
    db: Session = Depends(get_db),
    team_id: uuid.UUID
):
    """
    Obtém uma equipa específica pelo seu ID.
    O serviço 'get_team_by_id' já trata do erro 404 (não encontrado).
    """
    return maintenance_team_service.get_team_by_id(db=db, team_id=team_id)

@router.put(
    "/{team_id}",
    response_model=MaintenanceTeamRead,
    summary="Atualizar uma Equipa",
    description="Atualiza o nome de uma equipa de manutenção existente."
)
def update_team(
    *,
    db: Session = Depends(get_db),
    team_id: uuid.UUID,
    team_in: MaintenanceTeamUpdate,
    current_user: Usuario = Depends(get_current_active_user) # Para permissões
):
    """
    Atualiza uma equipa.
    """
    # (Ponto futuro: Adicionar verificação de permissões)
    
    # O serviço trata da lógica de validação (404, nome duplicado, etc.)
    return maintenance_team_service.update_team(
        db=db, team_id=team_id, team_in=team_in
    )

@router.delete(
    "/{team_id}",
    response_model=MaintenanceTeamRead, # Retorna o objeto que foi "apagado"
    summary="Eliminar (logicamente) uma Equipa",
    description="Marca uma equipa de manutenção como inativa (soft delete)."
)
def delete_team(
    *,
    db: Session = Depends(get_db),
    team_id: uuid.UUID,
    current_user: Usuario = Depends(get_current_active_user) # Para permissões
):
    """
    Elimina (logicamente) uma equipa.
    O serviço trata do 404 e retorna o objeto agora inativo.
    """
    # (Ponto futuro: Adicionar verificação de permissões)
    
    # O 'remove()' da CRUDBase fará o soft delete
    return maintenance_team_service.delete_team(db=db, team_id=team_id)