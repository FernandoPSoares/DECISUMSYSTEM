# backend/app/models/inventory/product_model.py

from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ...core.database import Base

class CategoriaProduto(Base):
    # ... (sem alterações)
    __tablename__ = 'categorias_produto'
    id = Column(String(50), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    metodo_custeio = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    categoria_pai_id = Column(String(50), ForeignKey('categorias_produto.id'), nullable=True)
    categoria_pai = relationship("CategoriaProduto", remote_side=[id])

class Produto(Base):
    # ... (sem alterações)
    __tablename__ = 'produtos'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    nome = Column(String(200), nullable=False)
    brand = Column(String(100))
    is_active = Column(Boolean, nullable=False, default=True)
    udm_id = Column(String(50), ForeignKey('udm.id'), nullable=False)
    categoria_produto_id = Column(String(50), ForeignKey('categorias_produto.id'), nullable=False)
    udm = relationship("Udm")
    categoria_produto = relationship("CategoriaProduto")
    variantes = relationship("VarianteProduto", back_populates="produto")
    boms = relationship("Bom", back_populates="produto", foreign_keys="[Bom.produto_id]")

class VarianteProduto(Base):
    __tablename__ = 'variantes_produto'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    referencia = Column(String(100), nullable=False, unique=True)
    nome = Column(String(200), nullable=False)
    valores_variante = Column(Text)
    nome_exibido = Column(String(500))
    custo_padrao = Column(Numeric(12, 4))
    is_active = Column(Boolean, nullable=False, default=True)
    produto_id = Column(UUID(as_uuid=True), ForeignKey('produtos.id'), nullable=False)
    
    produto = relationship("Produto", back_populates="variantes")
    lotes = relationship("Lote", back_populates="variante_produto")
    boms = relationship("Bom", back_populates="variante_produto", foreign_keys="[Bom.variante_produto_id]")
    ordens_de_producao = relationship("OrdemProducao", back_populates="variante_produto")

    # --- RELAÇÃO INVERSA QUE ESTAVA EM FALTA, ADICIONADA AQUI ---
    # Isto completa a ligação com o 'back_populates' do modelo OrdemDeCompraLinha.
    linhas_de_compra = relationship("OrdemDeCompraLinha", back_populates="variante_produto")

