# File: backend/app/models/maintenance/asset_meter_model.py
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base

class AssetMeter(Base):
    """
    Define um medidor associado a um ativo (ex: horímetro, contador de ciclos).
    Isto armazena a *definição* do medidor, não as suas leituras.
    """
    __tablename__ = 'maintenance_asset_meters'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # A que ativo este medidor pertence?
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_assets.id'), nullable=False)
    
    # Qual é a unidade de medida? (Ex: "Horas", "Ciclos", "km")
    # Ligado ao modelo UDM existente do inventário.
    udm_id: Mapped[str] = mapped_column(String(50), ForeignKey('udm.id'), nullable=False)

    # --- Relacionamentos ---
    asset: Mapped["Asset"] = relationship(back_populates="meters")
    
    # Ligação simples, UDM não precisa saber sobre medidores (assumindo que 'Udm' está importado ou disponível no Base)
    udm: Mapped["Udm"] = relationship() 
    
    readings: Mapped[List["AssetMeterReading"]] = relationship(
        back_populates="meter", 
        cascade="all, delete-orphan",
        order_by="desc(AssetMeterReading.reading_date)" # Útil: ter sempre a última leitura primeiro
    )

    # --- NOVA RELAÇÃO (Back-populates de pm_plan_model.py) ---
    # Planos de Preventiva que são acionados por este medidor
    pm_plans_triggered_by: Mapped[List["PMPlan"]] = relationship(
        back_populates="trigger_meter"
    )
    # --- FIM DA NOVA RELAÇÃO ---

class AssetMeterReading(Base):
    """
    Armazena uma leitura individual de um medidor num determinado momento.
    O histórico de leituras de um Ativo.
    """
    __tablename__ = 'maintenance_asset_meter_readings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # A que medidor esta leitura se refere?
    meter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_asset_meters.id'), nullable=False)
    
    reading_value: Mapped[float] = mapped_column(Float, nullable=False)
    reading_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Quem registou a leitura? (Opcional)
    technician_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_technicians.id'), nullable=True)
    
    # A leitura foi registada durante uma Ordem de Serviço? (Opcional)
    work_order_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_work_orders.id'), nullable=True)

    # --- Relacionamentos ---
    meter: Mapped["AssetMeter"] = relationship(back_populates="readings")
    
    # Ligação simples, Técnico não precisa saber todas as suas leituras
    technician: Mapped[Optional["Technician"]] = relationship() 
    
    # Ligação futura para a Ordem de Serviço
    # O "back_populates" será "meter_readings" na classe WorkOrder
    work_order: Mapped[Optional["WorkOrder"]] = relationship(back_populates="meter_readings")