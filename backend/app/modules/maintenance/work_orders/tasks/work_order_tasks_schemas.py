# File: backend/app/modules/maintenance/work_orders/tasks/work_order_tasks_schemas.py

import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

# --- Schemas de WorkOrderTask (Checklist) ---

class WorkOrderTaskCreate(BaseModel):
    """
    Schema para criar uma nova tarefa (item do checklist).
    A descrição é o único campo necessário.
    """
    description: str
    # O 'order_index' (ordem) será idealmente calculado pelo
    # 'service' ou 'crud' (ex: max(index) + 1) para garantir
    # que a nova tarefa vá para o fim da lista.


class WorkOrderTaskUpdate(BaseModel):
    """
    Schema para atualizar uma tarefa (item do checklist).
    Usado para:
    1. Marcar uma tarefa como 'completed: true'.
    2. Editar o texto da 'description'.
    3. Reordenar (mudar 'order_index').
    """
    description: Optional[str] = None
    completed: Optional[bool] = None
    order_index: Optional[int] = None
    

class WorkOrderTaskRead(BaseModel):
    """Schema completo para leitura (retorno da API) de uma Tarefa."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    work_order_id: uuid.UUID
    description: str
    completed: bool
    order_index: int