# backend/app/models/inventory/brand_model.py

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship, Mapped
from typing import List

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class Marca(Base):
    __tablename__ = 'marcas'

    # ID de configuração, String legível
    id = Column(String(50), primary_key=True)
    nome = Column(String(150), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # Campos de auditoria
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relação inversa para Produtos (um-para-muitos)
    # Usando a sintaxe Mapped recomendada pelo SQLAlchemy 2.0
    produtos: Mapped[List["Produto"]] = relationship(back_populates="marca")
