# File: backend/app/models/maintenance/pm_plan_model.py
import uuid
import enum
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text,
    Integer, Enum, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

from app.core.database import Base
# Importa os Enums de WorkOrder para usar como template
from .work_order_model import WorkOrderPriority, WorkOrderType


class PMTriggerType(enum.Enum):
    """Define o 'gatilho' que gera uma Ordem de Serviço Preventiva."""
    CALENDAR = "CALENDAR"  # Baseado em tempo (ex: a cada 30 dias)
    METER = "METER"        # Baseado em uso (ex: a cada 500 horas)
    MANUAL = "MANUAL"      # Apenas gera OS quando acionado manualmente


class PMPlan(Base):
    """
    Define um Plano de Manutenção Preventiva (PM).
    Este modelo é o "molde" que gera Ordens de Serviço (WorkOrders)
    com base em gatilhos de tempo ou medidores.
    """
    __tablename__ = 'maintenance_pm_plans'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment="Ex: PM-PRENSA-001")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="Ex: Lubrificação Semanal - Prensa 2")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # --- Chaves Estrangeiras (O Quê e Quem) ---
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_assets.id'), nullable=False, index=True)
    
    assigned_to_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_teams.id'), 
        nullable=True
    )
    assigned_to_technician_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_technicians.id'), 
        nullable=True
    )

    # --- Lógica do Gatilho (Quando) ---
    trigger_type: Mapped[PMTriggerType] = mapped_column(Enum(PMTriggerType), nullable=False)
    
    # Para gatilhos CALENDAR
    interval_days: Mapped[Optional[int]] = mapped_column(Integer, comment="Ex: Gerar a cada 30 dias")
    
    # Para gatilhos METER
    meter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_asset_meters.id'), 
        nullable=True,
        comment="Medidor (ex: Horímetro) que aciona esta PM"
    )
    meter_trigger_value: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), 
        comment="Ex: Gerar a cada 500 horas"
    )
    meter_last_reading_at_generation: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), 
        comment="Armazena a leitura do medidor na última vez que a OS foi gerada"
    )

    # --- Lógica de Agendamento ---
    start_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        comment="Data de início de vigência do plano"
    )
    next_due_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), 
        comment="A data de vencimento da próxima OS a ser gerada"
    )
    lead_time_days: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0, 
        comment="Dias de antecedência para gerar a OS (ex: 7 dias antes do vencimento)"
    )

    # --- Campos de Template (O que fazer) ---
    # Estes campos são usados para pré-preencher a OS gerada
    wo_title_template: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        default="Manutenção Preventiva: {asset_name}"
    )
    wo_description_template: Mapped[Optional[str]] = mapped_column(Text)
    wo_priority: Mapped[WorkOrderPriority] = mapped_column(
        Enum(WorkOrderPriority), 
        nullable=False, 
        default=WorkOrderPriority.MEDIUM
    )
    # O tipo de OS gerada será sempre PREVENTIVA
    wo_type: Mapped[WorkOrderType] = mapped_column(
        Enum(WorkOrderType), 
        nullable=False, 
        default=WorkOrderType.PREVENTIVE
    )

    # --- Relacionamentos (bidirecionais) ---
    
    asset: Mapped["Asset"] = relationship(back_populates="pm_plans")
    assigned_to_team: Mapped[Optional["MaintenanceTeam"]] = relationship(back_populates="pm_plans")
    assigned_to_technician: Mapped[Optional["Technician"]] = relationship(back_populates="pm_plans")
    
    trigger_meter: Mapped[Optional["AssetMeter"]] = relationship(
        "AssetMeter", 
        back_populates="pm_plans_triggered_by",
        foreign_keys=[meter_id] 
    )
    
    # A lista de OSs que este plano já gerou
    generated_work_orders: Mapped[List["WorkOrder"]] = relationship(
        back_populates="pm_plan"
    )

    # O checklist de tarefas para este Plano de PM
    tasks: Mapped[List["PMTask"]] = relationship(
        back_populates="pm_plan",
        order_by="PMTask.order_index", 
        cascade="all, delete-orphan"  
    )

    # --- NOVA RELAÇÃO (Back-populates de pm_parts_list_model.py) ---
    # A lista de peças (BOM) necessárias para este Plano de PM
    required_parts: Mapped[List["PMRequiredPart"]] = relationship(
        back_populates="pm_plan",
        cascade="all, delete-orphan"  # Se o plano for apagado, a lista de peças também é
    )
    # --- FIM DA NOVA RELAÇÃO ---