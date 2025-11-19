# File: backend/app/models/maintenance/pm_parts_list_model.py
import uuid
from sqlalchemy import (
    Column, String, ForeignKey, func, Numeric, Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from app.core.database import Base

class PMRequiredPart(Base):
    """
    Define uma peça (um item de Produto/Variante) e a quantidade
    necessária para um Plano de Manutenção Preventiva (PMPlan).
    Esta é a "Lista de Materiais" (BOM) do plano de preventiva.
    """
    __tablename__ = 'maintenance_pm_required_parts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # A que plano esta peça pertence?
    pm_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_pm_plans.id'), 
        nullable=False, 
        index=True
    )
    
    # Que peça (Variante) é necessária?
    product_variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('variantes_produto.id'), 
        nullable=False, 
        index=True
    )
    
    # Quantas são necessárias?
    quantity_required: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False, default=1.0)
    
    notes: Mapped[Optional[str]] = mapped_column(Text)

    # --- Relacionamentos ---
    
    # Ligação de volta ao Plano de PM
    pm_plan: Mapped["PMPlan"] = relationship(
        back_populates="required_parts"
    )
    
    # Ligação de volta à Variante do Produto
    product_variant: Mapped["VarianteProduto"] = relationship(
        back_populates="pm_required_parts"
    )