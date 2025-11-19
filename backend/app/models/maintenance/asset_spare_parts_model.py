# File: backend/app/models/maintenance/asset_spare_parts_model.py
import uuid
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text,
    Integer, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base

# --- CORREÇÃO AQUI ---
# A importação 'from app.models.inventory.product_model import Produto' 
# foi REMOVIDA. É desnecessária e causava uma dependência circular,
# pois já estamos a usar a string "Produto" no Mapped.
# --- FIM DA CORREÇÃO ---

class AssetSparePart(Base):
    """
    Tabela de associação (Many-to-Many) que liga Ativos (Assets)
    aos seus Produtos (Spare Parts / Peças) do inventário.
    Esta é a "Lista de Materiais de Manutenção" (BOM) de um equipamento.
    """
    __tablename__ = 'maintenance_asset_spare_parts'
    
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_assets.id'), 
        primary_key=True
    )
    
    # O nome da tabela de produtos é 'produtos', e a FK deve ser 'produtos.id'
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('produtos.id'), 
        primary_key=True
    )
    
    # Colunas extra para uma BOM de nível líder
    quantity_required: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False, default=1.0)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # --- Relacionamentos (bidirecionais) ---
    # Usamos strings "Asset" e "Produto" para evitar importações diretas
    
    asset: Mapped["Asset"] = relationship(back_populates="spare_parts")
    
    # O nome da classe é 'Produto'
    product: Mapped["Produto"] = relationship(back_populates="assets_using_this_part")