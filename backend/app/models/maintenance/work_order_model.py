# File: backend/app/models/maintenance/work_order_model.py
import uuid
import enum
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text,
    Integer, Enum, Table, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base
# Importa o modelo de Utilizador (corrigido para 'Usuario')
from app.models.administration.user_model import Usuario

# --- Tabelas de Associação Many-to-Many ---
# (Usando a sintaxe 'Table' para evitar mais ciclos de importação)

wo_failure_symptoms_association = Table(
    'maintenance_wo_symptoms',
    Base.metadata,
    Column('work_order_id', UUID(as_uuid=True), ForeignKey('maintenance_work_orders.id'), primary_key=True),
    Column('symptom_id', UUID(as_uuid=True), ForeignKey('maintenance_failure_symptoms.id'), primary_key=True)
)

wo_failure_modes_association = Table(
    'maintenance_wo_failure_modes',
    Base.metadata,
    Column('work_order_id', UUID(as_uuid=True), ForeignKey('maintenance_work_orders.id'), primary_key=True),
    Column('failure_mode_id', UUID(as_uuid=True), ForeignKey('maintenance_failure_modes.id'), primary_key=True)
)

wo_failure_causes_association = Table(
    'maintenance_wo_failure_causes',
    Base.metadata,
    Column('work_order_id', UUID(as_uuid=True), ForeignKey('maintenance_work_orders.id'), primary_key=True),
    Column('failure_cause_id', UUID(as_uuid=True), ForeignKey('maintenance_failure_causes.id'), primary_key=True)
)


# --- Enums para a Ordem de Serviço ---

class WorkOrderStatus(enum.Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class WorkOrderType(enum.Enum):
    CORRECTIVE = "CORRECTIVE"
    PREVENTIVE = "PREVENTIVE"
    PREDICTIVE = "PREDICTIVE"
    IMPROVEMENT = "IMPROVEMENT"
    SAFETY = "SAFETY"

class WorkOrderPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

# --- Modelo Principal da Ordem de Serviço ---

class WorkOrder(Base):
    """
    A Ordem de Serviço (OS) de Manutenção.
    Este é o objeto central do fluxo de trabalho.
    """
    __tablename__ = 'maintenance_work_orders'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wo_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False) # Ex: OS-2025-0001
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Enums
    status: Mapped[WorkOrderStatus] = mapped_column(Enum(WorkOrderStatus), nullable=False, default=WorkOrderStatus.DRAFT)
    wo_type: Mapped[WorkOrderType] = mapped_column(Enum(WorkOrderType), nullable=False, default=WorkOrderType.CORRECTIVE)
    priority: Mapped[WorkOrderPriority] = mapped_column(Enum(WorkOrderPriority), nullable=False, default=WorkOrderPriority.MEDIUM)

    # Datas
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True)) # Data limite
    completed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True)) # Data de conclusão
    
    # Rastreio de Parada (Downtime)
    downtime_start: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    downtime_end: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    downtime_hours: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))

    # --- Chaves Estrangeiras ---
    
    # Ligação ao Ativo
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_assets.id'), nullable=False, index=True)
    
    # Quem criou a OS (ligado ao seu modelo 'Usuario')
    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)
    
    # A quem esta OS está atribuída (Técnico ou Equipa)
    assigned_to_technician_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_technicians.id'), nullable=True)
    assigned_to_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_teams.id'), nullable=True)

    # Ligação ao Plano de PM (agora descomentado)
    pm_plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_pm_plans.id'), nullable=True)
    
    # --- Relacionamentos ---
    
    asset: Mapped["Asset"] = relationship(back_populates="work_orders")
    
    # Ligação ao seu modelo 'Usuario'
    created_by_user: Mapped[Optional["Usuario"]] = relationship(
        "Usuario", 
        back_populates="created_work_orders"
    )
    
    assigned_to_technician: Mapped[Optional["Technician"]] = relationship(back_populates="assigned_work_orders")
    assigned_to_team: Mapped[Optional["MaintenanceTeam"]] = relationship(back_populates="assigned_work_orders")

    # Ligação aos apontamentos de horas (mão de obra)
    labor_logs: Mapped[List["WorkOrderLaborLog"]] = relationship(
        back_populates="work_order"
    )
    
    # Ligação às peças usadas
    parts_used: Mapped[List["WorkOrderPartUsage"]] = relationship(
        back_populates="work_order"
    )
    
    # Ligação ao Plano de PM (agora descomentado)
    pm_plan: Mapped[Optional["PMPlan"]] = relationship(back_populates="generated_work_orders")

    # Relacionamentos Many-to-Many para Análise de Falha
    failure_symptoms: Mapped[List["MaintenanceFailureSymptom"]] = relationship(
        secondary=wo_failure_symptoms_association,
        back_populates="work_orders"
    )
    failure_modes: Mapped[List["MaintenanceFailureMode"]] = relationship(
        secondary=wo_failure_modes_association,
        back_populates="work_orders"
    )
    failure_causes: Mapped[List["MaintenanceFailureCause"]] = relationship(
        secondary=wo_failure_causes_association,
        back_populates="work_orders"
    )

    # Ligação ao Checklist de Tarefas
    tasks: Mapped[List["WorkOrderTask"]] = relationship(
        back_populates="work_order",
        order_by="WorkOrderTask.order_index",
        cascade="all, delete-orphan"
    )

    # Ligação aos Logs de Atividade/Comentários
    activity_logs: Mapped[List["WorkOrderLog"]] = relationship(
        back_populates="work_order",
        order_by="asc(WorkOrderLog.created_at)",
        cascade="all, delete-orphan"
    )

    # --- NOVA RELAÇÃO (Back-populates de asset_meter_model.py) ---
    # Leituras de medidores registadas durante esta OS
    meter_readings: Mapped[List["AssetMeterReading"]] = relationship(
        back_populates="work_order"
    )
    # --- FIM DA NOVA RELAÇÃO ---