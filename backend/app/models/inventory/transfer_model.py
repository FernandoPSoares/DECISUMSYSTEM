# backend/app/models/inventory/transfer_model.py

from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class Transferencia(Base):
    __tablename__ = 'transferencias'
    
    # --- MELHORIAS DE ARQUITETURA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referencia = Column(String(50), unique=True, index=True, nullable=False, comment="Identificador legível para o utilizador (ex: TRANSF-2025-001).")
    external_id = Column(String(100), unique=True, index=True, nullable=True, comment="ID de um sistema externo, para integrações.")

    status = Column(String(50), nullable=False)
    documento_origem = Column(String(100))
    datahora_confirmado = Column(DateTime)
    datahora_programada = Column(DateTime)
    datahora_realizado = Column(DateTime)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tipo_transferencia_id = Column(String(50), ForeignKey('tipos_transferencia.id'), nullable=False)
    # Tipos de FK corrigidos para UUID
    confirmado_por_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    responsavel_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    realizado_por_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)

    tipo_transferencia = relationship("TipoTransferencia")
    confirmado_por = relationship("Usuario", foreign_keys=[confirmado_por_id])
    responsavel = relationship("Usuario", foreign_keys=[responsavel_id])
    realizado_por = relationship("Usuario", foreign_keys=[realizado_por_id])

