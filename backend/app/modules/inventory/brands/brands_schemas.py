# backend/app/modules/inventory/brands/brands_schemas.py

from pydantic import BaseModel
from typing import Optional

class MarcaBase(BaseModel):
    """Schema base para uma marca, usado para criação."""
    id: str
    nome: str

class MarcaCreate(MarcaBase):
    """Schema para a criação de uma nova marca."""
    pass

class MarcaUpdate(BaseModel):
    """Schema para a atualização de uma marca. Todos os campos são opcionais."""
    nome: Optional[str] = None

class Marca(MarcaBase):
    """
    Schema para a leitura de uma marca (respostas da API).
    Inclui campos adicionais como 'is_active'.
    """
    is_active: bool

    class Config:
        from_attributes = True
