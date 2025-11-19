# backend/app/models/purchasing/purchase_order_model.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class OrdemDeCompra(Base):
    __tablename__ = 'ordens_de_compra'
    
    # --- MELHORIAS DE ARQUITETURA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referencia = Column(String(50), unique=True, index=True, nullable=False)
    external_id = Column(String(100), unique=True, index=True, nullable=True)

    nfe = Column(String(100))
    datahora_saida = Column(DateTime)
    datahora_prev_entrega = Column(DateTime)
    valor_total = Column(Numeric(12, 2))
    status = Column(String(50), default='Pendente', nullable=False)
    documento_origem = Column(String(50))
    datahora_confirmado = Column(DateTime)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Tipos de FK corrigidos para UUID
    responsavel_receb_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    confirmado_por_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    fornecedor_id = Column(UUID(as_uuid=True), ForeignKey('fornecedores.id'), nullable=False)

    # Relações bidirecionais
    fornecedor = relationship("Fornecedor", back_populates="ordens_de_compra")
    confirmado_por = relationship("Usuario", foreign_keys=[confirmado_por_id])
    responsavel_recebimento = relationship("Usuario", foreign_keys=[responsavel_receb_id])

    # Relação com as linhas do pedido
    linhas = relationship("OrdemDeCompraLinha", back_populates="ordem_de_compra")


class OrdemDeCompraLinha(Base):
    """Armazena os itens de uma Ordem de Compra."""
    __tablename__ = 'ordem_de_compra_linhas'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    quantidade = Column(Numeric(12, 4), nullable=False)
    preco_unitario = Column(Numeric(12, 4), nullable=False)
    
    ordem_de_compra_id = Column(UUID(as_uuid=True), ForeignKey('ordens_de_compra.id'), nullable=False)
    variante_produto_id = Column(UUID(as_uuid=True), ForeignKey('variantes_produto.id'), nullable=False)

    ordem_de_compra = relationship("OrdemDeCompra", back_populates="linhas")
    variante_produto = relationship("VarianteProduto", back_populates="linhas_de_compra")