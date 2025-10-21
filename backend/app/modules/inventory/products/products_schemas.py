# backend/app/modules/inventory/products/products_schemas.py

from pydantic import BaseModel
from typing import Optional, List
import uuid

# Importa schemas de outros módulos que serão usados aqui
from ..udms.udms_schemas import Udm
from ..product_categories.product_categories_schemas import CategoriaProduto
from ..brands.brands_schemas import Marca as MarcaSchema

# --- SCHEMAS PARA PRODUTO ---

class ProdutoBase(BaseModel):
    nome: str
    external_id: Optional[str] = None
    udm_id: str
    categoria_produto_id: str
    marca_id: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    external_id: Optional[str] = None
    udm_id: Optional[str] = None
    categoria_produto_id: Optional[str] = None
    marca_id: Optional[str] = None

class Produto(ProdutoBase):
    id: uuid.UUID
    is_active: bool
    # Campos aninhados para exibir informações relacionadas
    udm: Optional[Udm] = None
    categoria_produto: Optional[CategoriaProduto] = None
    marca: Optional[MarcaSchema] = None

    class Config:
        from_attributes = True

Produto.model_rebuild()

