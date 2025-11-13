# File: backend/app/models/maintenance/work_order_log_model.py
import uuid
import enum
from sqlalchemy import (
    Column, String, Boolean, ForeignKey, DateTime, func, Text,
    Enum  # 1. IMPORTAR 'DateTime' e 'func'
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base

class WorkOrderLogType(enum.Enum):
    """Define o tipo de entrada de log: uma mudança de sistema ou um comentário humano."""
    SYSTEM = "SYSTEM"    # Ex: "Estado alterado de ABERTO para EM ANDAMENTO"
    COMMENT = "COMMENT"  # Ex: "Técnico comentou: A aguardar peça X"

class WorkOrderLog(Base):
    """
    Armazena um histórico (log de auditoria) de todas as alterações e 
    comentários numa Ordem de Serviço.
    """
    __tablename__ = 'maintenance_wo_logs'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Chave estrangeira para a Ordem de Serviço principal
    work_order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_work_orders.id'), nullable=False, index=True)

    log_type: Mapped[WorkOrderLogType] = mapped_column(Enum(WorkOrderLogType), nullable=False)

    # Chave estrangeira para o Utilizador que fez a ação
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=True)

    comment: Mapped[Optional[str]] = mapped_column(Text, comment="O conteúdo do log ou comentário")

    # --- 2. ADICIONAR A COLUNA 'created_at' ---
    # Esta é a coluna que faltava e que causou o erro.
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    # --- FIM DA CORREÇÃO ---

    # --- Relacionamentos ---
    
    work_order: Mapped["WorkOrder"] = relationship(
        back_populates="activity_logs"
    )
    
    user: Mapped[Optional["Usuario"]] = relationship(
        back_populates="wo_activity_logs"
    )