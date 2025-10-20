# backend/app/models/purchasing/supplier_model.py

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    # --- MELHORIAS DE ARQUITETURA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)

    nome = Column(String(150), nullable=False)
    cnpj = Column(String(14), unique=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # Campos de auditoria
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relação inversa para Ordens de Compra
    # Isto completa a ligação com o 'back_populates' do modelo OrdemDeCompra.
    ordens_de_compra = relationship("OrdemDeCompra", back_populates="fornecedor")

