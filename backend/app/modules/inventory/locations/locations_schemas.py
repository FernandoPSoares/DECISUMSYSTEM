# backend/app/modules/inventory/locations/locations_schemas.py

from pydantic import BaseModel
from typing import Optional

# --- Schemas de Tipo de Local ---

class TipoLocalBase(BaseModel):
    id: str
    nome: str

class TipoLocalCreate(TipoLocalBase):
    pass

class TipoLocalUpdate(BaseModel):
    nome: Optional[str] = None

class TipoLocal(TipoLocalBase):
    is_active: bool
    
    class Config:
        from_attributes = True

# --- Schemas de Local ---

class LocalBase(BaseModel):
    id: str
    nome: str
    local_sucata: bool = False
    tipo_local_id: str
    local_pai_id: Optional[str] = None

class LocalCreate(LocalBase):
    pass

class LocalUpdate(BaseModel):
    nome: Optional[str] = None
    local_sucata: Optional[bool] = None
    tipo_local_id: Optional[str] = None
    local_pai_id: Optional[str] = None

class Local(LocalBase):
    is_active: bool
    tipo_local: TipoLocal # Devolve o objeto TipoLocal aninhado

    class Config:
        from_attributes = True
