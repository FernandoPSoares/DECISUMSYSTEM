# File: backend/app/modules/maintenance/work_orders/work_orders_schemas.py

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

# Importa Enums
from app.models.maintenance.work_order_model import (
    WorkOrderStatus, 
    WorkOrderType, 
    WorkOrderPriority
)

# Importa schemas de dependências externas
from app.modules.maintenance.assets.assets_schemas import AssetReadMinimal, PMPlanReadMinimal

# --- IMPORTAÇÃO DE SUB-FALIAS ---
# Importa os schemas mínimos do novo ficheiro partilhado
from .work_orders_shared_schemas import (
    UserReadMinimal, 
    TechnicianReadMinimal, 
    MaintenanceTeamReadMinimal
)
# Importa o schema da sub-fatia de Logs
from .logs.work_order_logs_schemas import WorkOrderLogRead
# Importa o schema da sub-fatia de Tarefas
from .tasks.work_order_tasks_schemas import WorkOrderTaskRead
# Importa o schema da sub-fatia de Mão de Obra
from .labor_logs.work_order_labor_logs_schemas import WorkOrderLaborLogRead
# --- NOVA IMPORTAÇÃO (Sub-Fatia de Peças) ---
from .parts.work_order_parts_schemas import WorkOrderPartUsageRead
# --- FIM DA NOVA IMPORTAÇÃO ---


# --- Schemas Mínimos Removidos ---
# As definições de UserReadMinimal, TechnicianReadMinimal, e
# MaintenanceTeamReadMinimal foram movidas para 'work_orders_shared_schemas.py'
# --- FIM DA REMOÇÃO ---


# --- Schemas para Sub-Entidades da WorkOrder (Locais) ---

# --- REMOÇÃO (WorkOrderTaskRead) ---
# (A definição foi movida para a sua própria sub-fatia)
# --- FIM DA REMOÇÃO ---

# --- REMOÇÃO (WorkOrderLaborLogRead) ---
# (A definição foi movida para a sua própria sub-fatia)
# --- FIM DA REMOÇÃO ---

# --- REMOÇÃO (WorkOrderPartUsageRead) ---
# A definição de 'WorkOrderPartUsageRead' foi movida para
# 'backend/app/modules/maintenance/work_orders/parts/work_order_parts_schemas.py'
# e importada no topo deste ficheiro.
# --- FIM DA REMOÇÃO ---


# O 'WorkOrderLogRead' agora é importado do seu próprio ficheiro

# --- Schemas Principais da Ordem de Serviço (WorkOrder) ---

class WorkOrderBase(BaseModel):
    """Schema base com campos comuns."""
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    wo_type: WorkOrderType = WorkOrderType.CORRECTIVE
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    due_date: Optional[datetime] = None
    asset_id: uuid.UUID
    assigned_to_technician_id: Optional[uuid.UUID] = None
    assigned_to_team_id: Optional[uuid.UUID] = None

class WorkOrderCreate(WorkOrderBase):
    """Schema usado para criar uma nova Ordem de Serviço."""
    status: WorkOrderStatus = WorkOrderStatus.OPEN
    pass

class WorkOrderUpdate(BaseModel):
    """Schema usado para atualizar uma Ordem de Serviço."""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[WorkOrderStatus] = None
    wo_type: Optional[WorkOrderType] = None
    priority: Optional[WorkOrderPriority] = None
    due_date: Optional[datetime] = None
    asset_id: Optional[uuid.UUID] = None
    assigned_to_technician_id: Optional[uuid.UUID] = None
    assigned_to_team_id: Optional[uuid.UUID] = None
    downtime_start: Optional[datetime] = None
    downtime_end: Optional[datetime] = None
    downtime_hours: Optional[float] = None

class WorkOrderRead(WorkOrderBase):
    """Schema completo para leitura (retorno da API) de uma Ordem de Serviço."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    wo_number: str
    status: WorkOrderStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    downtime_start: Optional[datetime] = None
    downtime_end: Optional[datetime] = None
    downtime_hours: Optional[float] = None

    # Relacionamentos
    asset: AssetReadMinimal
    created_by_user: Optional[UserReadMinimal] = None
    assigned_to_technician: Optional[TechnicianReadMinimal] = None
    assigned_to_team: Optional[MaintenanceTeamReadMinimal] = None
    pm_plan: Optional[PMPlanReadMinimal] = None
    
    # Listas de Sub-Entidades
    tasks: List[WorkOrderTaskRead] = [] # (Agora usa o schema importado)
    labor_logs: List[WorkOrderLaborLogRead] = [] # (Agora usa o schema importado)
    parts_used: List[WorkOrderPartUsageRead] = [] # (Agora usa o schema importado)
    activity_logs: List[WorkOrderLogRead] = [] # (Agora usa o schema importado)