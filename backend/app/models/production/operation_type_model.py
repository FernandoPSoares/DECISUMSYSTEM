# backend/app/models/production/operation_type_model.py

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ...core.database import Base

class TipoOperacao(Base):
    __tablename__ = 'tipos_operacao'
    
    id = Column(String(50), primary_key=True)
    nome = Column(String(150), nullable=False, unique=True)
    cod = Column(String(20), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    consumido_local_origem_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    consumido_local_destino_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    produzido_local_origem_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    produzido_local_destino_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    local_sucata_id = Column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=False)
    
    consumido_local_origem = relationship("Local", foreign_keys=[consumido_local_origem_id])
    consumido_local_destino = relationship("Local", foreign_keys=[consumido_local_destino_id])
    produzido_local_origem = relationship("Local", foreign_keys=[produzido_local_origem_id])
    produzido_local_destino = relationship("Local", foreign_keys=[produzido_local_destino_id])
    local_sucata = relationship("Local", foreign_keys=[local_sucata_id])

    # --- RELAÇÃO INVERSA QUE ESTAVA EM FALTA, ADICIONADA AQUI ---
    # Isto completa a ligação com o 'back_populates' do modelo OrdemProducao.
    ordens_de_producao = relationship("OrdemProducao", back_populates="tipo_operacao")

