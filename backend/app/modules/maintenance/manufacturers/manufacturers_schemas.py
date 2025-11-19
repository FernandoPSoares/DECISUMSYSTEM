# File: backend/app/modules/maintenance/manufacturers/manufacturers_schemas.py

from typing import Optional, List
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr

# --- Schemas Base ---

class ManufacturerBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    # CORREÇÃO: Removido o campo 'website' que causava o erro
    # website: Optional[str] = None 
    is_active: bool = True

# --- Schemas de Criação ---

class ManufacturerCreate(ManufacturerBase):
    pass

# --- Schemas de Atualização ---

class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    # website: Optional[str] = None  <-- Também removido daqui
    is_active: Optional[bool] = None

# --- Schemas de Leitura ---

class ManufacturerRead(ManufacturerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID

# Schema simplificado para listas dropdown
class ManufacturerReadSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str