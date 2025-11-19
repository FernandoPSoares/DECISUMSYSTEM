# File: backend/app/modules/maintenance/work_orders/parts/work_order_parts_schemas.py

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# Importa o schema mínimo partilhado
from ..work_orders_shared_schemas import UserReadMinimal

# (Nota: Futuramente, poderemos importar um 'ProductReadMinimal'
#  do módulo de inventário para exibir o nome/código do produto)


# --- Schemas de WorkOrderPartUsage (Consumo de Peças) ---

class WorkOrderPartUsageBase(BaseModel):
    """Schema base com os campos essenciais para o consumo de uma peça."""
    
    # O ID do Produto (do módulo de Inventário)
    product_id: uuid.UUID 
    
    quantity_used: float = Field(..., gt=0, description="Quantidade utilizada (ex: 2.5).")


class WorkOrderPartUsageCreate(WorkOrderPartUsageBase):
    """Schema usado para registar o consumo de uma nova peça na OS."""
    # Os IDs 'work_order_id' e 'created_by_user_id'
    # serão injetados pelo 'service'.
    pass

class WorkOrderPartUsageUpdate(BaseModel):
    """
    Schema para atualizar um consumo de peça.
    (Normalmente, apenas a quantidade é editável).
    """
    # Não permitimos a alteração do 'product_id';
    # O utilizador deve apagar e registar novamente.
    quantity_used: Optional[float] = Field(None, gt=0, description="Nova quantidade utilizada.")
    
    
class WorkOrderPartUsageRead(WorkOrderPartUsageBase):
    """Schema completo para leitura (retorno da API) de um Consumo de Peça."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    work_order_id: uuid.UUID
    created_at: datetime
    
    # Relações: Quem registou o consumo
    created_by_user: Optional[UserReadMinimal] = None
    
    # (Futuramente, adicionaremos 'product: ProductReadMinimal = None'
    #  quando a fatia de Inventário estiver pronta para essa integração)