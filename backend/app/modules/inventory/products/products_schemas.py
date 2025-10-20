# backend/app/modules/inventory/products/products_schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List

# --- Schemas de Unidade de Medida (Udm) ---

class UdmBase(BaseModel):
    id: str
    nome: str
    proporcao_combinada: float = Field(..., gt=0, description="Proporção em relação à unidade de referência (deve ser > 0)")

# --- Schemas de Categoria de Unidade de Medida (CategoriaUdm) ---

class CategoriaUdmBase(BaseModel):
    id: str
    nome: str

class CategoriaUdmCreate(CategoriaUdmBase):
    unidade_referencia_id: str
    unidade_referencia_nome: str

class CategoriaUdmUpdate(BaseModel):
    nome: Optional[str] = None

class ChangeReferenceUdmRequest(BaseModel):
    new_reference_udm_id: str

# --- 1. CORREÇÃO: Adicionado unidade_referencia_id para consistência ---
class CategoriaUdm(CategoriaUdmBase):
    is_active: bool
    unidade_referencia_id: Optional[str] = None
    unidade_referencia: Optional[UdmBase] = None # Usar UdmBase para evitar ciclos
    class Config:
        from_attributes = True

# --- 2. CORREÇÃO: Adicionado o objeto da categoria para o formulário ---
class Udm(UdmBase):
    is_active: bool
    categoria_udm: Optional[CategoriaUdmBase] = None # Essencial para pré-preencher o formulário
    class Config:
        from_attributes = True

class CategoriaUdmDetail(CategoriaUdm):
    udms: List[Udm] = []

# --- Schemas para UDM (completos) ---
class UdmCreate(UdmBase):
    categoria_udm_id: str
    proporcao_combinada: float = Field(default=1.0, gt=0, description="Proporção em relação à unidade de referência (deve ser > 0)")

class UdmUpdate(BaseModel):
    nome: Optional[str] = None
    proporcao_combinada: Optional[float] = Field(None, gt=0, description="Nova proporção (deve ser > 0)")
    categoria_udm_id: Optional[str] = Field(None, description="ID da nova categoria para mover a UDM")

# --- Schemas de Categoria de Produto ---
# (O resto do ficheiro permanece igual)
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

CategoriaUdm.model_rebuild()
CategoriaProduto.model_rebuild()

