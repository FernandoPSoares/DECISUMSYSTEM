# File: backend/app/models/maintenance/asset_category_model.py
import uuid
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import List
from app.core.database import Base

class AssetCategory(Base):
    """
    Representa uma categoria para agrupar ativos.
    Ex: "Mecânico", "Elétrico", "Hidráulico", "Infraestrutura"
    """
    __tablename__ = 'maintenance_asset_categories'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Relacionamento com Ativos
    assets: Mapped[List["Asset"]] = relationship(
        "Asset", 
        back_populates="category",
        cascade="all, delete-orphan"
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<AssetCategory(name='{self.name}')>"
