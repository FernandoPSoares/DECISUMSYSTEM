# backend/app/models/production/bom_model.py

from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey, Interval, PrimaryKeyConstraint, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ...core.database import Base

class Bom(Base):
    __tablename__ = 'boms'
    
    # --- MELHORIAS DE ARQUITETURA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    
    qtd_producao = Column(Numeric(12, 4), nullable=False)
    duracao = Column(Interval)
    balanco_massa = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Tipos de FK corrigidos para UUID
    produto_id = Column(UUID(as_uuid=True), ForeignKey('produtos.id'), nullable=False)
    variante_produto_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=True)
    
    # Relações bidirecionais
    produto = relationship("Produto", back_populates="boms")
    variante_produto = relationship("VarianteProduto", back_populates="boms")
    componentes = relationship("BomComponente", back_populates="bom")
    ordens_de_producao = relationship("OrdemProducao", back_populates="bom")

class BomComponente(Base):
    __tablename__ = 'bom_componentes'
    __table_args__ = (PrimaryKeyConstraint('bom_id', 'componente_variante_id'),)

    # Tipos de FK corrigidos para UUID
    bom_id = Column(UUID(as_uuid=True), ForeignKey('boms.id'), nullable=False)
    componente_produto_id = Column(UUID(as_uuid=True), ForeignKey('produtos.id'), nullable=False)
    componente_variante_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=False)
    
    qtd = Column(Numeric(12, 4), nullable=False)

    # Relações bidirecionais
    bom = relationship("Bom", back_populates="componentes")
    componente_produto = relationship("Produto", foreign_keys=[componente_produto_id])
    componente_variante = relationship("VarianteProduto", foreign_keys=[componente_variante_id])

