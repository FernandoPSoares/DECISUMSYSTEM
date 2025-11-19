# File: backend/app/modules/maintenance/work_orders/parts/work_order_parts_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, Path, Body, status

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario

# Importações da sub-fatia
from .work_order_parts_service import work_order_part_usage_service
from .work_order_parts_schemas import (
    WorkOrderPartUsageRead, 
    WorkOrderPartUsageCreate, 
    WorkOrderPartUsageUpdate
)

# Este router será "aninhado" (nested) dentro do work_orders_router
# Não definimos um 'prefix' aqui.
router = APIRouter(
    tags=["Maintenance - Work Order Parts"],
    dependencies=[Depends(get_current_active_user)] # Protege todos os endpoints
)

@router.get(
    "/",
    response_model=List[WorkOrderPartUsageRead],
    summary="Listar consumo de peças de uma OS"
)
def read_parts_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    db: Session = Depends(get_db)
):
    """
    Obtém a lista de todos os consumos de peças (materiais)
    para uma Ordem de Serviço específica, ordenados por data de criação.
    
    O 'service' irá primeiro verificar se a Ordem de Serviço (pai) existe.
    """
    return work_order_part_usage_service.get_parts_for_wo(
        db=db, 
        work_order_id=wo_id
    )


@router.post(
    "/",
    response_model=WorkOrderPartUsageRead,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar um consumo de peça a uma OS"
)
def create_part_usage_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    part_in: WorkOrderPartUsageCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Cria um novo registo de consumo de peça (material) associado a uma OS.
    O utilizador logado é automaticamente definido como o criador.
    
    O 'service' irá verificar se a OS (pai) e o Produto (peça) existem e estão ativos.
    """
    return work_order_part_usage_service.create_part_usage_for_wo(
        db=db, 
        work_order_id=wo_id, 
        obj_in=part_in, 
        current_user=current_user
    )


@router.put(
    "/{part_usage_id}",
    response_model=WorkOrderPartUsageRead,
    summary="Atualizar um consumo de peça"
)
def update_part_usage(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    part_usage_id: uuid.UUID = Path(..., description="ID do Registo de Consumo a atualizar"),
    part_in: WorkOrderPartUsageUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Atualiza um registo de consumo de peça (normalmente a quantidade).
    
    O 'service' validará que a OS e o registo de consumo existem
    e que o registo pertence à OS.
    """
    return work_order_part_usage_service.update_part_usage(
        db=db,
        work_order_id=wo_id,
        part_usage_id=part_usage_id,
        obj_in=part_in
    )


@router.delete(
    "/{part_usage_id}",
    response_model=WorkOrderPartUsageRead,
    summary="Eliminar um consumo de peça"
)
def delete_part_usage(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    part_usage_id: uuid.UUID = Path(..., description="ID do Registo de Consumo a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina (HARD DELETE) um registo de consumo de peça.
    
    O 'service' validará que tanto a OS como o Registo de Consumo existem
    e que o registo pertence à OS.
    """
    return work_order_part_usage_service.delete_part_usage(
        db=db,
        work_order_id=wo_id,
        part_usage_id=part_usage_id
    )