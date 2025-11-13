# File: backend/app/models/inventory/lot_model.py

from sqlalchemy import Column, String, DateTime, ForeignKey, func
# --- ALTERAÇÃO: Importações Mapped e List adicionadas ---
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List # Importação de List

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class Lote(Base):
    __tablename__ = 'lotes'
    
    # --- ARQUITETURA DE ID CORRIGIDA ---
    # A chave primária é um UUID gerado automaticamente.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- CAMPO EXTERNAL_ID ADICIONADO ---
    # Para a integração com o sistema antigo. É opcional, mas se existir, tem de ser único.
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    
    nome = Column(String(100), nullable=False, index=True, comment="Nome ou código do lote (ex: LOTE2025-A1)")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    data_de_expiracao = Column(DateTime)
    
    # Chave estrangeira que aponta para o ID UUID da Variante de Produto
    variante_produto_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=False)
    
    # Relação bidirecional com a Variante de Produto
    variante_produto = relationship("VarianteProduto", back_populates="lotes")

    # --- NOVA RELAÇÃO (Back-populates de work_order_parts_model.py) ---
    wo_part_usages: Mapped[List["WorkOrderPartUsage"]] = relationship(
        back_populates="lot"
    )
    # --- FIM DA NOVA RELAÇÃO ---