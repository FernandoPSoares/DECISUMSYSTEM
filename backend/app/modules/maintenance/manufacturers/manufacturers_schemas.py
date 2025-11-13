# File: backend/app/modules/maintenance/manufacturers/manufacturers_schemas.py

import uuid
from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional

# --- Schema Base ---
# Campos comuns a todos os schemas de Fabricante
class ManufacturerBase(BaseModel):
    name: str
    website: Optional[HttpUrl] = None
    support_phone: Optional[str] = None
    support_email: Optional[EmailStr] = None

    class Config:
        # Habilita o modo "from_attributes" (anteriormente orm_mode)
        # Permite que o Pydantic leia dados de objetos ORM (modelos SQLAlchemy)
        from_attributes = True

# --- Schema de Criação ---
# O que a API espera no body de um POST para criar um fabricante.
class ManufacturerCreate(ManufacturerBase):
    # Neste caso, é idêntico ao Base.
    # Podemos adicionar validações @validator aqui se necessário no futuro.
    pass

# --- Schema de Atualização ---
# O que a API espera no body de um PUT/PATCH (todos os campos opcionais)
class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[HttpUrl] = None
    support_phone: Optional[str] = None
    support_email: Optional[EmailStr] = None

# --- Schema de Leitura ---
# O que a API retorna ao ler um fabricante.
# Inclui o ID e os campos do Base.
class ManufacturerRead(ManufacturerBase):
    id: uuid.UUID