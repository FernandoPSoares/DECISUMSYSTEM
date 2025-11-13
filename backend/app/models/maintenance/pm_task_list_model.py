# File: backend/app/models/maintenance/pm_task_list_model.py
import uuid
from sqlalchemy import (
    Column, String, Integer, Text, ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base

class PMTask(Base):
    """
    Define uma tarefa individual (um item de checklist) dentro de um
    Plano de Manutenção Preventiva (PMPlan).
    Ex: "1. Verificar nível do óleo", "2. Limpar filtro de ar".
    """
    __tablename__ = 'maintenance_pm_tasks'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # A que plano esta tarefa pertence?
    pm_plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_pm_plans.id'), nullable=False, index=True)
    
    # Ordem da tarefa (1, 2, 3...)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    # Descrição da tarefa
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    # Tempo estimado para esta tarefa (em minutos)
    estimated_time_minutes: Mapped[Optional[int]] = mapped_column(Integer)

    # --- Relacionamentos ---
    
    # Ligação de volta ao Plano de PM
    pm_plan: Mapped["PMPlan"] = relationship(
        back_populates="tasks"
    )