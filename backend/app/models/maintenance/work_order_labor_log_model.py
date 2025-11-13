# File: backend/app/models/maintenance/work_order_labor_log_model.py
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

class WorkOrderLaborLog(Base):
    """
    Regista o tempo (mão de obra) gasto pelos técnicos numa Ordem de Serviço.
    Cada entrada é um "apontamento de horas".
    """
    __tablename__ = 'maintenance_work_order_labor_logs'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- Chaves Estrangeiras ---
    
    # Ligação à Ordem de Serviço
    work_order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_work_orders.id'), 
        nullable=False, 
        index=True
    )
    
    # Ligação ao Técnico que fez o trabalho
    technician_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('maintenance_technicians.id'), 
        nullable=False, 
        index=True
    )
    
    # --- Dados do Apontamento ---
    
    date_worked: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    hours_spent: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    # --- Relacionamentos (bidirecionais) ---

    # Ligação de volta para a Ordem de Serviço
    work_order: Mapped["WorkOrder"] = relationship(
        back_populates="labor_logs"
    )
    
    # Ligação de volta para o Técnico
    technician: Mapped["Technician"] = relationship(
        back_populates="labor_logs"
    )