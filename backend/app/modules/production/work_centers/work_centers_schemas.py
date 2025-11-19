# backend/app/modules/production/work_centers/work_centers_schemas.py

from pydantic import BaseModel
from typing import Optional

class CentroTrabalhoBase(BaseModel):
    id: str
    nome: str

class CentroTrabalhoCreate(CentroTrabalhoBase):
    pass

class CentroTrabalhoUpdate(BaseModel):
    nome: Optional[str] = None

class CentroTrabalho(CentroTrabalhoBase):
    is_active: bool

    class Config:
        from_attributes = True
