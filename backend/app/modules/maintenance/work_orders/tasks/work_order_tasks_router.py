# File: backend/app/modules/maintenance/work_orders/tasks/work_order_tasks_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, Path, Body, status

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
# (Não precisamos do 'current_user' aqui, pois a tarefa não
# está ligada a quem a criou, mas o router está protegido)

# Importações da sub-fatia
from .work_order_tasks_service import work_order_task_service
from .work_order_tasks_schemas import (
    WorkOrderTaskRead, 
    WorkOrderTaskCreate, 
    WorkOrderTaskUpdate
)

# Este router será "aninhado" (nested) dentro do work_orders_router
# Não definimos um 'prefix' aqui.
router = APIRouter(
    tags=["Maintenance - Work Order Tasks"],
    dependencies=[Depends(get_current_active_user)] # Protege todos os endpoints
)

@router.get(
    "/",
    response_model=List[WorkOrderTaskRead],
    summary="Listar tarefas (checklist) de uma OS"
)
def read_tasks_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    db: Session = Depends(get_db)
):
    """
    Obtém a lista de todas as tarefas (checklist)
    para uma Ordem de Serviço específica, ordenadas por 'order_index'.
    
    O 'service' irá primeiro verificar se a Ordem de Serviço (pai) existe.
    """
    return work_order_task_service.get_tasks_for_wo(db=db, work_order_id=wo_id)


@router.post(
    "/",
    response_model=WorkOrderTaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar uma tarefa (checklist) a uma OS"
)
def create_task_for_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    task_in: WorkOrderTaskCreate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova tarefa (item de checklist) para uma OS.
    O 'service' (via 'crud') irá calcular o 'order_index' automaticamente.
    
    O 'service' irá primeiro verificar se a Ordem de Serviço (pai) existe.
    """
    return work_order_task_service.create_task_for_wo(
        db=db, 
        work_order_id=wo_id, 
        obj_in=task_in
    )


@router.put(
    "/{task_id}",
    response_model=WorkOrderTaskRead,
    summary="Atualizar uma tarefa (marcar/desmarcar, reordenar)"
)
def update_task(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    task_id: uuid.UUID = Path(..., description="ID da Tarefa a atualizar"),
    task_in: WorkOrderTaskUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Atualiza uma tarefa (item de checklist) específica.
    Usado para marcar/desmarcar, editar texto, ou reordenar.
    
    O 'service' validará que tanto a OS como a Tarefa existem
    e que a tarefa pertence à OS.
    """
    return work_order_task_service.update_task(
        db=db,
        work_order_id=wo_id,
        task_id=task_id,
        obj_in=task_in
    )


@router.delete(
    "/{task_id}",
    response_model=WorkOrderTaskRead,
    summary="Eliminar uma tarefa (checklist)"
)
def delete_task(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço (pai)"),
    task_id: uuid.UUID = Path(..., description="ID da Tarefa a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina (HARD DELETE) uma tarefa (item de checklist) de uma OS.
    
    O 'service' validará que tanto a OS como a Tarefa existem
    e que a tarefa pertence à OS.
    """
    return work_order_task_service.delete_task(
        db=db,
        work_order_id=wo_id,
        task_id=task_id
    )