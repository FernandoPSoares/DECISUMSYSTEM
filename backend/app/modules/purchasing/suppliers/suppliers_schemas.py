# backend/app/modules/purchasing/suppliers/suppliers_schemas.py

from pydantic import BaseModel
from typing import Optional

class FornecedorBase(BaseModel):
    id: str
    nome: str
    cnpj: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None

class Fornecedor(FornecedorBase):
    is_active: bool

    class Config:
        from_attributes = True
