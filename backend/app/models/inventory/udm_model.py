# backend/app/modules/inventory/products/udm_model.py

from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class CategoriaUdm(Base):
    __tablename__ = 'categorias_udm'
    id = Column(String(50), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # --- ALTERAÇÃO E ADIÇÃO CRÍTICA AQUI ---
    # Coluna para guardar o ID da UDM de referência.
    # É 'nullable=True' porque o valor só pode ser definido DEPOIS de a categoria
    # e a sua UDM de referência serem criadas. A nossa camada de serviço irá garantir esta lógica.
    unidade_referencia_id = Column(String(50), ForeignKey('udm.id'), nullable=True)

    # Relação para aceder a todas as UDMs que pertencem a esta categoria.
    # Adicionamos 'foreign_keys' para resolver a ambiguidade de ter duas relações com 'Udm'.
    udms = relationship("Udm", back_populates="categoria_udm", foreign_keys="[Udm.categoria_udm_id]")
    
    # Relação para aceder diretamente à UDM de referência.
    unidade_referencia = relationship("Udm", foreign_keys=[unidade_referencia_id])


class Udm(Base):
    __tablename__ = 'udm'
    id = Column(String(50), primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    proporcao_combinada = Column(Numeric(10, 4), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    categoria_udm_id = Column(String(50), ForeignKey('categorias_udm.id'), nullable=False)
    
    # A relação agora especifica 'foreign_keys' para ser explícita e resolver a ambiguidade.
    categoria_udm = relationship("CategoriaUdm", back_populates="udms", foreign_keys=[categoria_udm_id])
