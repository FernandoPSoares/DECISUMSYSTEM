# backend/app/modules/inventory/product_categories/product_categories_schemas.py

from pydantic import BaseModel
from typing import Optional

class CategoriaProdutoBase(BaseModel):
    id: str
    nome: str
    metodo_custeio: str
    categoria_pai_id: Optional[str] = None

class CategoriaProdutoCreate(CategoriaProdutoBase):
    pass

class CategoriaProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    metodo_custeio: Optional[str] = None
    categoria_pai_id: Optional[str] = None

class CategoriaProduto(CategoriaProdutoBase):
    is_active: bool
    categoria_pai: Optional['CategoriaProduto'] = None
    class Config:
        from_attributes = True

CategoriaProduto.model_rebuild()
