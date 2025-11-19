# File: backend/app/modules/maintenance/work_orders/logs/work_order_logs_schemas.py

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# --- CORREÇÃO DE IMPORTAÇÃO CIRCULAR ---
# Importa o schema mínimo do novo ficheiro partilhado
from ..work_orders_shared_schemas import UserReadMinimal
# --- FIM DA CORREÇÃO ---


# --- Schemas de WorkOrderLog ---

class WorkOrderLogBase(BaseModel):
    """Schema base com o campo de criação (o próprio comentário)."""
    log_entry: str

class WorkOrderLogCreate(WorkOrderLogBase):
    """Schema usado para criar um novo log (comentário) via API."""
    pass
    
class WorkOrderLogRead(WorkOrderLogBase):
    """Schema completo para leitura (retorno da API) de um Log."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    work_order_id: uuid.UUID
    created_at: datetime
    
    # Relação: Quem criou o log (agora importado do ficheiro partilhado)
    created_by_user: Optional[UserReadMinimal] = None