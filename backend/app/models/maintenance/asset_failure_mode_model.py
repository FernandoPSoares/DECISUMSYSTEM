# File: backend/app/models/maintenance/asset_failure_mode_model.py
import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from app.core.database import Base

# --- Tabelas de Lookup para Análise de Causa Raiz (RCA) ---
# Estas tabelas armazenam as *opções* que um técnico pode selecionar
# ao fechar uma Ordem de Serviço. Os relacionamentos (Many-to-Many)
# com a Ordem de Serviço serão definidos quando criarmos o modelo WorkOrder.

class MaintenanceFailureSymptom(Base):
    """
    Sintoma da Falha: Qual foi o primeiro sinal?
    Ex: "Vibração excessiva", "Ruído alto", "Fumo".
    """
    __tablename__ = 'maintenance_failure_symptoms'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # O relacionamento M-M com WorkOrder será adicionado depois,
    # usando a tabela 'maintenance_wo_failure_symptoms'.
    # work_orders: Mapped[List["WorkOrder"]] = relationship(
    #     secondary="maintenance_wo_failure_symptoms",
    #     back_populates="failure_symptoms"
    # )

class MaintenanceFailureMode(Base):
    """
    Modo de Falha: O que falhou? 
    Ex: "Rolamento partido", "Motor sobre-aquecido", "Correia partida".
    """
    __tablename__ = 'maintenance_failure_modes'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # O relacionamento M-M com WorkOrder será adicionado depois,
    # usando a tabela 'maintenance_wo_failure_modes'.
    # work_orders: Mapped[List["WorkOrder"]] = relationship(
    #     secondary="maintenance_wo_failure_modes",
    #     back_populates="failure_modes"
    # )

class MaintenanceFailureCause(Base):
    """
    Causa da Falha: Por que falhou? (A Causa Raiz)
    Ex: "Falta de lubrificação", "Desgaste normal", "Erro de operação".
    """
    __tablename__ = 'maintenance_failure_causes'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # O relacionamento M-M com WorkOrder será adicionado depois,
    # usando a tabela 'maintenance_wo_failure_causes'.
    # work_orders: Mapped[List["WorkOrder"]] = relationship(
    #     secondary="maintenance_wo_failure_causes",
    #     back_populates="failure_causes"
    # )