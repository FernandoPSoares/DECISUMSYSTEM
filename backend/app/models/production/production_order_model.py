# backend/app/models/production/production_order_model.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class OrdemProducao(Base):
    __tablename__ = 'ordens_producao'
    
    # --- MELHORIAS DE ARQUITETURA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referencia = Column(String(50), unique=True, index=True, nullable=False, comment="Identificador legível para o utilizador (ex: OP-2025-001).")
    external_id = Column(String(100), unique=True, index=True, nullable=True)

    qtd_programada = Column(Numeric(12, 4))
    qtd_realizada = Column(Numeric(12, 4))
    status = Column(String(50), nullable=False)
    documento_origem = Column(String(100))
    datahora_confirmado = Column(DateTime)
    datahora_programada = Column(DateTime)
    datahora_realizado = Column(DateTime)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Tipos de FK corrigidos para String ou UUID, conforme o modelo de destino
    tipo_operacao_id = Column(String(50), ForeignKey('tipos_operacao.id'), nullable=False)
    centro_trabalho_id = Column(UUID(as_uuid=True), ForeignKey('centros_trabalho.id'), nullable=True)
    variante_produto_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=False)
    lote_id = Column(UUID(as_uuid=True), ForeignKey('lotes.id'), nullable=True)
    bom_id = Column(UUID(as_uuid=True), ForeignKey('boms.id'), nullable=False)
    confirmado_por_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    responsavel_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    realizado_por_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)

    # Relações bidirecionais
    tipo_operacao = relationship("TipoOperacao", back_populates="ordens_de_producao")
    centro_trabalho = relationship("CentroTrabalho", back_populates="ordens_de_producao")
    variante_produto = relationship("VarianteProduto", back_populates="ordens_de_producao")
    lote = relationship("Lote") # Lote é um registo final, pode ser unidirecional
    bom = relationship("Bom", back_populates="ordens_de_producao")
    confirmado_por = relationship("Usuario", foreign_keys=[confirmado_por_id])
    responsavel = relationship("Usuario", foreign_keys=[responsavel_id])
    realizado_por = relationship("Usuario", foreign_keys=[realizado_por_id])