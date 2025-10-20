# backend/app/modules/inventory/products/products_schemas.py

from pydantic import BaseModel
from typing import Optional, List

# --- Schemas de Unidade de Medida (Udm) ---
# Definidos primeiro para serem usados pelos schemas de CategoriaUdm

class UdmBase(BaseModel):
    id: str
    nome: str
    proporcao_combinada: float

class Udm(UdmBase):
    is_active: bool
    class Config:
        from_attributes = True

# --- Schemas de Categoria de Unidade de Medida (CategoriaUdm) ---

class CategoriaUdmBase(BaseModel):
    id: str
    nome: str

class CategoriaUdmCreate(CategoriaUdmBase):
    """O 'contrato' para criar uma nova categoria. Exige os dados da sua unidade de referência."""
    unidade_referencia_id: str
    unidade_referencia_nome: str

class CategoriaUdmUpdate(BaseModel):
    nome: Optional[str] = None

class CategoriaUdm(CategoriaUdmBase):
    """Schema de resposta básico, com a unidade de referência."""
    is_active: bool
    unidade_referencia: Optional[Udm] = None
    
    class Config:
        from_attributes = True

class CategoriaUdmDetail(CategoriaUdm):
    """Schema de resposta completo, que inclui a lista de todas as UDMs da categoria."""
    udms: List[Udm] = []


# --- Schemas para UDM (completos) ---
class UdmCreate(UdmBase):
    categoria_udm_id: str

class UdmUpdate(BaseModel):
    nome: Optional[str] = None
    proporcao_combinada: Optional[float] = None

# --- Schemas de Categoria de Produto ---

class CategoriaProdutoBase(BaseModel):
    id: str
    nome: str
    metodo_custeio: str
    # O ID da categoria-pai é opcional
    categoria_pai_id: Optional[str] = None

class CategoriaProdutoCreate(CategoriaProdutoBase):
    pass

class CategoriaProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    metodo_custeio: Optional[str] = None
    categoria_pai_id: Optional[str] = None

class CategoriaProduto(CategoriaProdutoBase):
    is_active: bool
    # A resposta da API pode incluir o objeto da categoria-pai aninhado
    categoria_pai: Optional['CategoriaProduto'] = None

    class Config:
        from_attributes = True

# Permite que o Pydantic resolva as referências circulares
CategoriaUdm.model_rebuild()
CategoriaProduto.model_rebuild()

