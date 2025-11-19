# File: backend/app/modules/maintenance/work_orders/labor_logs/work_order_labor_logs_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, Path, Body, status

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario

# Importações da sub-fatia
from .work_order_labor_logs_service import work_order_labor_log_service
from .work_order_labor_logs_schemas import (
    WorkOrderLaborLogRead, 
    WorkOrderLaborLogCreate, 
    WorkOrderLaborLogUpdate
)

# Este router será "aninhado" (nested) dentro do work_orders_router
# Não definimos um 'prefix' aqui.
router = APIRouter(
    tags=["Maintenance - Work Order Labor"],
    dependencies=[Depends(get_current_active_user)] # Protege todos os endpoints
)

@router.get(
    "/",
    response_model=List[WorkOrderLaborLogRead],
    summary="Listar apontamentos de mão de obra de uma OS"
)
def read_labor_logs_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    db: Session = Depends(get_db)
):
    """
    Obtém a lista de todos os apontamentos de mão de obra (horas)
    para uma Ordem de Serviço específica, ordenados por data de início.
    
    O 'service' irá primeiro verificar se a Ordem de Serviço (pai) existe.
    """
    return work_order_labor_log_service.get_labor_logs_for_wo(
        db=db, 
        work_order_id=wo_id
    )


@router.post(
    "/",
    response_model=WorkOrderLaborLogRead,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar um apontamento de mão de obra a uma OS"
)
def create_labor_log_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    labor_log_in: WorkOrderLaborLogCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cria um novo apontamento de mão de obra (horas) associado a uma OS.
    O utilizador logado é automaticamente definido como o criador.
    
    O 'service' irá verificar se a OS (pai) e o Técnico (filho) existem e estão ativos.
    """
    return work_order_labor_log_service.create_labor_log_for_wo(
        db=db, 
        work_order_id=wo_id, 
        obj_in=labor_log_in, 
        current_user=current_user
    )


@router.put(
    "/{labor_log_id}",
    response_model=WorkOrderLaborLogRead,
    summary="Atualizar um apontamento de mão de obra"
)
def update_labor_log(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    labor_log_id: uuid.UUID = Path(..., description="ID do Apontamento a atualizar"),
    labor_log_in: WorkOrderLaborLogUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Atualiza um apontamento de mão de obra (horas) específico.
    
    O 'service' validará que a OS, o apontamento, e (se alterado)
    o Técnico existem e são válidos.
    """
    return work_order_labor_log_service.update_labor_log(
        db=db,
        work_order_id=wo_id,
        labor_log_id=labor_log_id,
        obj_in=labor_log_in
    )


@router.delete(
    "/{labor_log_id}",
    response_model=WorkOrderLaborLogRead,
    summary="Eliminar um apontamento de mão de obra"
)
def delete_labor_log(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    labor_log_id: uuid.UUID = Path(..., description="ID do Apontamento a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina (HARD DELETE) um apontamento de mão de obra (horas).
    
    O 'service' validará que tanto a OS como o Apontamento existem
    e que o apontamento pertence à OS.
    """
    return work_order_labor_log_service.delete_labor_log(
        db=db,
        work_order_id=wo_id,
        labor_log_id=labor_log_id
    )