# backend/app/models/production/work_center_model.py

from sqlalchemy import Column, String, Boolean, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class CentroTrabalho(Base):
    __tablename__ = 'centros_trabalho'
    
    # --- MELHORIAS DE ARQUITETURA ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String(100), unique=True, index=True, nullable=True)
    
    nome = Column(String(150), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Campos de excelência para planeamento e custeio
    capacidade_por_hora = Column(Numeric(12, 4), comment="Capacidade de produção por hora (em UDM do produto).")
    custo_hora = Column(Numeric(12, 4), comment="Custo operacional por hora.")

    # Campos de auditoria
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relação inversa para Ordens de Produção
    ordens_de_producao = relationship("OrdemProducao", back_populates="centro_trabalho")

