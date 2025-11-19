# File: backend/app/modules/maintenance/work_orders/work_orders_shared_schemas.py

import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

"""
Este ficheiro quebra as importações circulares.

Contém os schemas "Mínimos" que são necessários tanto pelo
'work_orders_schemas.py' como pelas suas sub-fatias
(como 'logs/work_order_logs_schemas.py').
"""

class UserReadMinimal(BaseModel):
    """Schema mínimo para exibir o criador ou participante de uma OS."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    full_name: Optional[str] = None
    email: str

class TechnicianReadMinimal(BaseModel):
    """Schema mínimo para exibir um técnico associado."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    is_active: bool

class MaintenanceTeamReadMinimal(BaseModel):
    """Schema mínimo para exibir uma equipa associada."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    is_active: bool