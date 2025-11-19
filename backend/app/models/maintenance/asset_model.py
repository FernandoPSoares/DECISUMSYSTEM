# File: backend/app/models/maintenance/asset_model.py
import uuid
import enum
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text,
    Integer, Enum 
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base
from app.models.inventory.location_model import Local
from app.models.maintenance.asset_category_model import AssetCategory

class AssetStatus(enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    NON_OPERATIONAL = "NON_OPERATIONAL"
    MAINTENANCE = "MAINTENANCE"
    DECOMMISSIONED = "DECOMMISSIONED"

class Asset(Base):
    """
    Representa um Ativo (Equipamento, Máquina, Componente) que 
    requer manutenção.
    """
    __tablename__ = 'maintenance_assets'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    serial_number: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)
    internal_tag: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    status: Mapped[AssetStatus] = mapped_column(Enum(AssetStatus), nullable=False, default=AssetStatus.OPERATIONAL)
    
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Datas de aquisição e instalação
    purchase_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    installation_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    warranty_expiry_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))

    # Chaves Estrangeiras
    manufacturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_manufacturers.id'), nullable=True)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_asset_categories.id'), nullable=True)
    
    # --- CORREÇÃO DE TIPO DE DADO ---
    # O ID da tabela 'locais' é String(36), não UUID.
    location_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('locais.id'), nullable=True)
    # --- FIM DA CORREÇÃO ---
    
    # Auto-relacionamento para hierarquia (Pai/Filho)
    parent_asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_assets.id'), nullable=True)

    # --- Relacionamentos ---
    manufacturer: Mapped[Optional["Manufacturer"]] = relationship(back_populates="assets")
    category: Mapped[Optional["AssetCategory"]] = relationship(back_populates="assets")
    
    location: Mapped[Optional["Local"]] = relationship(back_populates="assets")

    # Hierarquia (Pai)
    parent_asset: Mapped[Optional["Asset"]] = relationship(
        "Asset", 
        back_populates="child_assets", 
        remote_side=[id]
    )
    # Hierarquia (Filhos)
    child_assets: Mapped[List["Asset"]] = relationship(
        "Asset", 
        back_populates="parent_asset",
        cascade="all, delete-orphan"
    )

    # Peças sobressalentes (BOM de Manutenção)
    spare_parts: Mapped[List["AssetSparePart"]] = relationship(
        back_populates="asset",
        cascade="all, delete-orphan"
    )
    
    # Medidores (Horímetros, etc.)
    meters: Mapped[List["AssetMeter"]] = relationship(
        back_populates="asset",
        cascade="all, delete-orphan"
    )

    # Ordens de Serviço ligadas a este ativo
    work_orders: Mapped[List["WorkOrder"]] = relationship(back_populates="asset")
    
    # Planos de Manutenção Preventiva associados a este ativo
    pm_plans: Mapped[List["PMPlan"]] = relationship(
        back_populates="asset",
        cascade="all, delete-orphan"
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)