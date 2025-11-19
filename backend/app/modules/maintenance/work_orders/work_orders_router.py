# File: backend/app/modules/maintenance/work_orders/work_orders_router.py

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, Body, status

from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.models.administration.user_model import Usuario

# Importa os schemas e o serviço da fatia "WorkOrders"
from .work_orders_schemas import WorkOrderRead, WorkOrderCreate, WorkOrderUpdate
from .work_orders_service import work_order_service, WorkOrderService

# --- IMPORTAÇÃO DE SUB-FATIASC ---
from .logs.work_order_logs_router import router as logs_router
from .tasks.work_order_tasks_router import router as tasks_router
from .labor_logs.work_order_labor_logs_router import router as labor_logs_router
# --- NOVA IMPORTAÇÃO (Sub-Fatia de Peças) ---
from .parts.work_order_parts_router import router as parts_router
# --- FIM DA IMPORTAÇÃO ---


router = APIRouter(
    prefix="/maintenance/work-orders",
    tags=["Maintenance - Work Orders"],
    dependencies=[Depends(get_current_active_user)] # Protege todos os endpoints
)

@router.post(
    "/",
    response_model=WorkOrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova Ordem de Serviço"
)
def create_work_order(
    wo_in: WorkOrderCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user) # Obtém o utilizador logado
):
    """
    Cria uma nova Ordem de Serviço (OS) de manutenção.
    
    O 'service' irá:
    - Gerar o próximo 'wo_number' sequencial (ex: OS-2025-0001).
    - Associar o utilizador logado como o criador.
    - Validar a existência do Ativo, Técnico e/ou Equipa.
    """
    return work_order_service.create_work_order(
        db=db, 
        obj_in=wo_in, 
        current_user=current_user
    )


@router.get(
    "/",
    response_model=List[WorkOrderRead],
    summary="Listar Ordens de Serviço"
)
def read_work_orders(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registos a pular"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registos a retornar"),
    search: Optional[str] = Query(None, description="Pesquisa (Nº OS, Título, Nome do Ativo, TAG do Ativo)"),
    sort_by: Optional[str] = Query(None, description="Campo para ordenar (ex: 'wo_number', 'asset.name')"),
    sort_order: str = Query("desc", description="Ordem: 'asc' ou 'desc' (padrão 'desc' por data de criação)")
):
    """
    Obtém uma lista de Ordens de Serviço com paginação, busca e ordenação.
    A busca é otimizada para procurar no Nº da OS, título, nome do ativo e TAG.
    """
    return work_order_service.get_work_orders(
        db=db, 
        skip=skip, 
        limit=limit, 
        search=search, 
        sort_by=sort_by, 
        sort_order=sort_order
    )


@router.get(
    "/{wo_id}",
    response_model=WorkOrderRead,
    summary="Obter Ordem de Serviço por ID"
)
def read_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço"),
    db: Session = Depends(get_db)
):
    """
    Obtém os detalhes completos de uma Ordem de Serviço, incluindo:
    - Ativo, Criador, Responsáveis
    - Tarefas (Checklist)
    - Apontamentos de Horas (Mão de Obra)
    - Peças Utilizadas
    - Logs de Atividade (Comentários)
    """
    return work_order_service.get_work_order(db=db, wo_id=wo_id)


@router.put(
    "/{wo_id}",
    response_model=WorkOrderRead,
    summary="Atualizar Ordem de Serviço"
)
def update_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço a atualizar"),
    wo_in: WorkOrderUpdate = Body(...),
    db: Session = Depends(get_db)
):
    """
    Atualiza os detalhes de uma Ordem de Serviço existente.
    
    O 'service' irá:
    - Validar FKs (Ativo, Técnico, Equipa) se forem alterados.
    - Gerir automaticamente o campo 'completed_at' se o status for 'COMPLETED'.
    """
    return work_order_service.update_work_order(db=db, wo_id=wo_id, obj_in=wo_in)


@router.delete(
    "/{wo_id}",
    response_model=WorkOrderRead,
    summary="Eliminar Ordem de Serviço (Apenas Rascunhos)"
)
def delete_work_order(
    wo_id: uuid.UUID = Path(..., description="ID da Ordem de Serviço a eliminar"),
    db: Session = Depends(get_db)
):
    """
    Elimina (HARD DELETE) uma Ordem de Serviço.
    
    O 'service' **impedirá** a eliminação (Erro 400) se a OS
    não estiver no status 'DRAFT' (Rascunho).
    """
    return work_order_service.delete_work_order(db=db, wo_id=wo_id)


# --- INCLUSÃO DO ROUTER ANINHADO (LOGS) ---
# Monta os endpoints de logs sob o caminho "/{wo_id}/logs"
router.include_router(
    logs_router,
    prefix="/{wo_id}/logs"
)
# --- FIM DA INCLUSÃO ---


# --- INCLUSÃO (SUB-FATIA DE TAREFAS) ---
# Monta os endpoints de tarefas (checklist) sob o caminho "/{wo_id}/tasks"
router.include_router(
    tasks_router,
    prefix="/{wo_id}/tasks"
)
# --- FIM DA INCLUSÃO ---


# --- INCLUSÃO (SUB-FATIA DE MÃO DE OBRA) ---
# Monta os endpoints de apontamentos sob o caminho "/{wo_id}/labor-logs"
router.include_router(
    labor_logs_router,
    prefix="/{wo_id}/labor-logs"
)
# --- FIM DA INCLUSÃO ---


# --- NOVA INCLUSÃO (SUB-FATIA DE PEÇAS) ---
# Monta os endpoints de consumo de peças sob o caminho "/{wo_id}/parts"
router.include_router(
    parts_router,
    prefix="/{wo_id}/parts"
)
# --- FIM DA NOVA INCLUSÃO ---