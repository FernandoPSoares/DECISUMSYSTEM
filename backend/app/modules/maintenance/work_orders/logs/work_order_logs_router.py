# File: backend/app/modules/maintenance/work_orders/logs/work_order_logs_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, Path, Body, status

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario

# Importações da sub-fatia
from .work_order_logs_service import work_order_log_service
from .work_order_logs_schemas import WorkOrderLogRead, WorkOrderLogCreate

# Este router será "aninhado" (nested) dentro do work_orders_router
# Não definimos um 'prefix' aqui.
router = APIRouter(
    tags=["Maintenance - Work Order Logs"],
    dependencies=[Depends(get_current_active_user)] # Protege todos os endpoints
)

@router.get(
    "/",
    response_model=List[WorkOrderLogRead],
    summary="Listar logs (comentários) de uma OS"
)
def read_logs_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    db: Session = Depends(get_db)
):
    """
    Obtém a lista de todos os logs de atividade (comentários)
    para uma Ordem de Serviço específica, ordenados cronologicamente.
    
    O 'service' irá primeiro verificar se a Ordem de Serviço (pai) existe.
    """
    return work_order_log_service.get_logs_for_wo(db=db, work_order_id=wo_id)


@router.post(
    "/",
    response_model=WorkOrderLogRead,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar um log (comentário) a uma OS"
)
def create_log_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    log_in: WorkOrderLogCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cria um novo log (comentário) associado a uma Ordem de Serviço.
    O utilizador logado é automaticamente definido como o autor.
    
    O 'service' irá primeiro verificar se a Ordem de Serviço (pai) existe.
    """
    return work_order_log_service.create_log_for_wo(
        db=db, 
        work_order_id=wo_id, 
        obj_in=log_in, 
        current_user=current_user
    )


@router.delete(
    "/{log_id}",
    response_model=WorkOrderLogRead,
    summary="Eliminar um log (comentário)"
)
def delete_log(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai) - (presente na URL)"),
    log_id: uuid.UUID = Path(..., description="ID do Log (comentário) a eliminar"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Elimina um log de atividade (comentário) específico.
    
    (A lógica de negócio no 'service' pode ser expandida
    para permitir que apenas o autor ou um admin possa eliminar).
    """
    # O wo_id é necessário para construir o path, mas o service
    # só precisa do log_id para encontrar e eliminar o comentário.
    return work_order_log_service.delete_log(
        db=db, 
        log_id=log_id, 
        current_user=current_user
    )