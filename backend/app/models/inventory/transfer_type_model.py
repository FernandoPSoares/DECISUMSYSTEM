# backend/app/models/inventory/transfer_type_model.py

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class TipoTransferencia(Base):
    __tablename__ = 'tipos_transferencia'
    
    # Para uma tabela de configuração, um ID em String legível é uma boa prática.
    id = Column(String(50), primary_key=True)
    nome = Column(String(150), nullable=False, unique=True)
    cod = Column(String(20), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)

    # --- MELHORIAS DE ARQUITETURA ---
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Tipos de FK corrigidos para UUID para corresponder à tabela 'locais'
    local_origem_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=True)
    local_destino_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=True)
    local_sucata_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    
    # As relações continuam corretas, pois o SQLAlchemy lida com a ligação
    local_origem = relationship("Local", foreign_keys=[local_origem_id])
    local_destino = relationship("Local", foreign_keys=[local_destino_id])
    local_sucata = relationship("Local", foreign_keys=[local_sucata_id])

