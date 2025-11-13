# File: backend/app/models/maintenance/work_order_parts_model.py
import uuid
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text,
    Integer, Numeric
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Importa a nossa Base partilhada a partir do core da aplicação
from app.core.database import Base

class WorkOrderPartUsage(Base):
    """
    Regista as peças (Produtos/Variantes) consumidas numa Ordem de Serviço.
    Cada entrada é uma "saída de material" para a OS.
    """
    __tablename__ = 'maintenance_work_order_parts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- Chaves Estrangeiras ---
    
    # Ligação à Ordem de Serviço
    work_order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_work_orders.id'), 
        nullable=False, 
        index=True
    )
    
    # Ligação à Variante do Produto (o item de stock)
    # Usamos VarianteProduto em vez de Produto para rastreio exato de stock.
    product_variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('variantes_produto.id'), 
        nullable=False, 
        index=True
    )
    
    # Ligação ao Lote (para rastreabilidade)
    lot_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('lotes.id'), 
        nullable=True, 
        index=True
    )

    # --- Dados do Consumo ---
    
    quantity_planned: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False, default=0.0)
    quantity_used: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False, default=0.0)
    
    # Guarda o custo unitário no momento do consumo para relatórios de custo precisos
    unit_cost: Mapped[Optional[float]] = mapped_column(Numeric(12, 4)) 

    # --- Relacionamentos (bidirecionais) ---

    # Ligação de volta para a Ordem de Serviço
    work_order: Mapped["WorkOrder"] = relationship(
        back_populates="parts_used"
    )
    
    # Ligação de volta para a Variante do Produto
    product_variant: Mapped["VarianteProduto"] = relationship(
        back_populates="wo_part_usages"
    )
    
    # Ligação de volta para o Lote
    lot: Mapped[Optional["Lote"]] = relationship(
        back_populates="wo_part_usages"
    )