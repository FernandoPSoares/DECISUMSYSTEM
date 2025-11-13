# File: backend/app/models/maintenance/work_order_task_model.py
import uuid
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text, 
    Integer  # <--- 1. IMPORTAR O TIPO 'Integer'
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base

class WorkOrderTask(Base):
    """
    Define um item individual do "checklist" de uma Ordem de Serviço.
    Ex: "1. Verificar tensão", "2. Lubrificar", etc.
    """
    __tablename__ = 'maintenance_wo_tasks'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Chave estrangeira para a Ordem de Serviço principal
    work_order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_work_orders.id'), nullable=False, index=True)
    
    # --- 2. ADICIONAR A COLUNA 'order_index' ---
    # Esta é a coluna que faltava e que causou o erro.
    order_index: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0, 
        comment="Controla a ordem da tarefa no checklist (0, 1, 2...)"
    )
    # --- FIM DA CORREÇÃO ---
    
    task_description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Controlo de conclusão
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Quem completou a tarefa?
    completed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)

    # --- Relacionamentos ---
    
    work_order: Mapped["WorkOrder"] = relationship(
        back_populates="tasks"
    )
    
    completed_by_user: Mapped[Optional["Usuario"]] = relationship(
        back_populates="completed_wo_tasks"
    )