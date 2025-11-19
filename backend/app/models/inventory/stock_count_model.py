# backend/app/models/inventory/stock_count_model.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class ContagemInventario(Base):
    __tablename__ = 'contagens_inventario'
    
    # Padrão de ID de excelência
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referencia = Column(String(50), unique=True, index=True, nullable=False)
    
    data_contagem = Column(DateTime, nullable=False)
    data_aprovacao = Column(DateTime)
    status = Column(String(50), nullable=False, default='Em Aberto')

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # --- CORREÇÃO CRÍTICA AQUI ---
    # Tipos de FK corrigidos de String para UUID para corresponder aos modelos de destino
    local_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    responsavel_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    aprovador_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'))

    local = relationship("Local")
    responsavel = relationship("Usuario", foreign_keys=[responsavel_id])
    aprovador = relationship("Usuario", foreign_keys=[aprovador_id])

    linhas = relationship("ContagemInventarioLinha", back_populates="contagem")

class ContagemInventarioLinha(Base):
    __tablename__ = 'contagem_inventario_linhas'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quantidade_sistema = Column(Numeric(12, 4), nullable=False)
    quantidade_contada = Column(Numeric(12, 4), nullable=False)
    diferenca = Column(Numeric(12, 4), nullable=False)

    # --- CORREÇÃO CRÍTICA AQUI ---
    # Tipos de FK corrigidos de String para UUID
    contagem_id = Column(UUID(as_uuid=True), ForeignKey('contagens_inventario.id'), nullable=False)
    variante_produto_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=False)
    lote_id = Column(UUID(as_uuid=True), ForeignKey('lotes.id'), nullable=True) # Lote pode ser opcional

    contagem = relationship("ContagemInventario", back_populates="linhas")
    variante_produto = relationship("VarianteProduto")
    lote = relationship("Lote")

