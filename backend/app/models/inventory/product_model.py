# backend/app/models/inventory/product_model.py

from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List, Optional

from ...core.database import Base

class CategoriaProduto(Base):
    __tablename__ = 'categorias_produto'
    id = Column(String(50), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    metodo_custeio = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    categoria_pai_id = Column(String(50), ForeignKey('categorias_produto.id'), nullable=True)
    categoria_pai = relationship("CategoriaProduto", remote_side=[id])
    produtos: Mapped[List["Produto"]] = relationship(back_populates="categoria_produto")

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    nome = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Chaves estrangeiras
    udm_id = Column(String(50), ForeignKey('udm.id'), nullable=False)
    categoria_produto_id = Column(String(50), ForeignKey('categorias_produto.id'), nullable=False)
    
    # --- NOVA COLUNA E RELAÇÃO PARA MARCA ---
    marca_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey('marcas.id'), nullable=True)
    
    # Relações
    udm = relationship("Udm")
    categoria_produto = relationship("CategoriaProduto", back_populates="produtos")
    marca: Mapped[Optional["Marca"]] = relationship(back_populates="produtos") # <-- NOVA RELAÇÃO
    
    variantes: Mapped[List["VarianteProduto"]] = relationship(back_populates="produto")
    boms: Mapped[List["Bom"]] = relationship(back_populates="produto", foreign_keys="[Bom.produto_id]")

class VarianteProduto(Base):
    __tablename__ = 'variantes_produto'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    referencia = Column(String(100), nullable=False, unique=True)
    nome = Column(String(200), nullable=False)
    valores_variante = Column(Text) # Ex: {"cor": "Azul", "tamanho": "M"}
    nome_exibido = Column(String(500))
    custo_padrao = Column(Numeric(12, 4))
    is_active = Column(Boolean, nullable=False, default=True)
    produto_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('produtos.id'), nullable=False)
    
    produto: Mapped["Produto"] = relationship(back_populates="variantes")
    lotes: Mapped[List["Lote"]] = relationship(back_populates="variante_produto")
    boms: Mapped[List["Bom"]] = relationship(back_populates="variante_produto", foreign_keys="[Bom.variante_produto_id]")
    ordens_de_producao: Mapped[List["OrdemProducao"]] = relationship(back_populates="variante_produto")
    linhas_de_compra: Mapped[List["OrdemDeCompraLinha"]] = relationship(back_populates="variante_produto")
