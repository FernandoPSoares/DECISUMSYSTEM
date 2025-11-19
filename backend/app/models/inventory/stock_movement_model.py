# backend/app/models/inventory/stock_movement_model.py

from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class MovimentacaoLivroRazao(Base):
    __tablename__ = 'movimentacao_livro_razao'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referencia = Column(String(100), nullable=False, index=True, comment="Referência ao documento de origem (ex: OP-001, OC-002, CI-003).")
    qtd_prevista = Column(Numeric(12, 4))
    qtd_realizada = Column(Numeric(12, 4))
    preco_un = Column(Numeric(12, 4))
    status = Column(String(50), nullable=False, comment="Status do movimento (ex: 'Planeado', 'Concluído').")
    
    # --- MELHORIAS DE ARQUITETURA ---
    data_movimento = Column(DateTime, nullable=False, comment="Data e hora em que a movimentação física ocorreu.")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Tipos de FK corrigidos para UUID
    variante_produto_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=False)
    lote_id = Column(UUID(as_uuid=True), ForeignKey('lotes.id'), nullable=True) # Lote pode ser opcional
    local_origem_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=True) # Origem pode ser nula (ex: compra)
    local_destino_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=True) # Destino pode ser nulo (ex: venda)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True, comment="Utilizador que registou a movimentação.")

    variante_produto = relationship("VarianteProduto")
    lote = relationship("Lote")
    local_origem = relationship("Local", foreign_keys=[local_origem_id])
    local_destino = relationship("Local", foreign_keys=[local_destino_id])
    usuario = relationship("Usuario")

