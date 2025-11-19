from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

# --- Base ---
class RCAItemBase(BaseModel):
    code: str
    description: str
    is_active: bool = True

# --- Create ---
class RCAItemCreate(RCAItemBase):
    pass

# --- Update ---
class RCAItemUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

# --- Read (Shared) ---
class RCAItemRead(RCAItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID

# Para facilitar, usamos o mesmo schema para Sintomas, Modos e Causas
# pois a estrutura é idêntica (code, description).
class FailureSymptomRead(RCAItemRead): pass
class FailureModeRead(RCAItemRead): pass
class FailureCauseRead(RCAItemRead): pass