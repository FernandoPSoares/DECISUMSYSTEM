# File: backend/app/modules/maintenance/work_orders/labor_logs/work_order_labor_logs_schemas.py

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# Importa os schemas mínimos partilhados
from ..work_orders_shared_schemas import UserReadMinimal, TechnicianReadMinimal


# --- Schemas de WorkOrderLaborLog (Apontamento de Horas) ---

class WorkOrderLaborLogBase(BaseModel):
    """Schema base com os campos essenciais para um apontamento."""
    start_time: datetime = Field(..., description="Data e hora de início do trabalho.")
    hours: float = Field(..., gt=0, description="Total de horas trabalhadas (ex: 1.5 para 1h 30min).")
    
    # O 'end_time' pode ser calculado (start_time + hours)
    end_time: Optional[datetime] = None
    
    # ID do técnico que realizou o trabalho
    technician_id: uuid.UUID


class WorkOrderLaborLogCreate(WorkOrderLaborLogBase):
    """Schema usado para criar um novo apontamento de horas via API."""
    # Os IDs 'work_order_id' e 'created_by_user_id'
    # serão injetados pelo 'service'
    pass

class WorkOrderLaborLogUpdate(BaseModel):
    """
    Schema para atualizar um apontamento de horas.
    Todos os campos são opcionais.
    """
    start_time: Optional[datetime] = None
    hours: Optional[float] = Field(None, gt=0)
    end_time: Optional[datetime] = None
    technician_id: Optional[uuid.UUID] = None
    
    
class WorkOrderLaborLogRead(WorkOrderLaborLogBase):
    """Schema completo para leitura (retorno da API) de um Apontamento."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    work_order_id: uuid.UUID
    created_at: datetime
    
    # Relações: Quem criou o log e quem executou o trabalho
    created_by_user: Optional[UserReadMinimal] = None
    technician: Optional[TechnicianReadMinimal] = None