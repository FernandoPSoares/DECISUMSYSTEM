# File: backend/app/modules/maintenance/technicians/technicians_router.py

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Dependências centrais do projeto
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario # Para o type hint do Depends

# Componentes desta "fatia" (slice)
from .technicians_service import technician_service
from .technicians_schemas import (
    TechnicianRead,
    TechnicianCreate,
    TechnicianUpdate
)

router = APIRouter(
    prefix="/maintenance/technicians",
    tags=["Manutenção - Técnicos"],
    # Todos os endpoints nesta fatia exigem um utilizador autenticado
    dependencies=[Depends(get_current_active_user)]
)

@router.post(
    "/",
    response_model=TechnicianRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo Técnico",
    description="Cria um novo perfil de técnico e associa-o a um utilizador existente."
)
def create_technician(
    *,
    db: Session = Depends(get_db),
    technician_in: TechnicianCreate,
    current_user: Usuario = Depends(get_current_active_user) # Para verificação de permissões futuras
):
    """
    Cria um novo técnico.
    
    - **db**: Sessão da base de dados.
    - **technician_in**: Dados de criação (user_id, team_id).
    - **current_user**: Utilizador autenticado (para futuras verificações de permissões).
    """
    # (Ponto futuro: Adicionar verificação de permissões aqui, ex:)
    # if not user_has_permission(current_user, "technician:create"):
    #     raise HTTPException(status.HTTP_403_FORBIDDEN, "Sem permissão.")
        
    # O serviço trata de toda a lógica de negócio (validação de IDs, duplicados, etc.)
    return technician_service.create_technician(db=db, technician_in=technician_in)

@router.get(
    "/",
    response_model=List[TechnicianRead],
    summary="Listar todos os Técnicos",
    description="Obtém uma lista paginada de todos os técnicos, com os seus dados de utilizador e equipa."
)
def read_technicians(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtém uma lista paginada de técnicos.
    """
    return technician_service.get_all_technicians(db=db, skip=skip, limit=limit)

@router.get(
    "/{technician_id}",
    response_model=TechnicianRead,
    summary="Obter um Técnico por ID",
    description="Obtém os detalhes de um técnico específico, incluindo utilizador e equipa."
)
def read_technician(
    *,
    db: Session = Depends(get_db),
    technician_id: uuid.UUID
):
    """
    Obtém um técnico específico pelo seu ID.
    O serviço 'get_technician_by_id' já trata do erro 404.
    """
    return technician_service.get_technician_by_id(db=db, technician_id=technician_id)

@router.put(
    "/{technician_id}",
    response_model=TechnicianRead,
    summary="Atualizar um Técnico",
    description="Atualiza a equipa de um técnico existente."
)
def update_technician(
    *,
    db: Session = Depends(get_db),
    technician_id: uuid.UUID,
    technician_in: TechnicianUpdate,
    current_user: Usuario = Depends(get_current_active_user) # Para permissões
):
    """
    Atualiza um técnico (atualmente, apenas a sua associação de equipa).
    """
    # (Ponto futuro: Adicionar verificação de permissões)
    
    # O serviço trata da lógica de validação (404, etc.)
    return technician_service.update_technician(
        db=db, technician_id=technician_id, technician_in=technician_in
    )

@router.delete(
    "/{technician_id}",
    response_model=TechnicianRead, # Retorna o objeto que foi apagado
    summary="Eliminar um Técnico",
    description="Elimina um perfil de técnico."
)
def delete_technician(
    *,
    db: Session = Depends(get_db),
    technician_id: uuid.UUID,
    current_user: Usuario = Depends(get_current_active_user) # Para permissões
):
    """
    Elimina um técnico.
    O serviço trata do 404 e retorna o objeto eliminado.
    """
    # (Ponto futuro: Adicionar verificação de permissões)
    
    return technician_service.delete_technician(db=db, technician_id=technician_id)