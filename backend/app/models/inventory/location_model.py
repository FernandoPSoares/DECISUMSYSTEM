# File: backend/app/models/inventory/location_model.py

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped  # <-- ALTERAÇÃO: Adicionado Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List  # <-- ALTERAÇÃO: Adicionado List

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class TipoLocal(Base):
    __tablename__ = 'tipos_local'
    id = Column(String(50), primary_key=True) # ID de configuração, pode ser String
    nome = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Local(Base):
    __tablename__ = 'locais'
    
    # --- ARQUITETURA DE ID CORRIGIDA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    
    nome = Column(String(150), nullable=False, unique=True)
    barcode = Column(String(100), unique=True, index=True, nullable=True)
    local_sucata = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tipo_local_id = Column(String(50), ForeignKey('tipos_local.id'), nullable=False)
    # A FK para o auto-relacionamento também deve ser UUID
    local_pai_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=True)

    tipo_local = relationship("TipoLocal")
    local_pai = relationship("Local", remote_side=[id])

    # --- INÍCIO DA ALTERAÇÃO (CMMS) ---
    
    # Relação One-to-Many com Ativos (Assets)
    # Permite que um Local saiba quais equipamentos (Assets) estão nele.
    # Usamos "Asset" como string para evitar erros de importação circular.
    assets: Mapped[List["Asset"]] = relationship(back_populates="location")
    
    # --- FIM DA ALTERAÇÃO ---