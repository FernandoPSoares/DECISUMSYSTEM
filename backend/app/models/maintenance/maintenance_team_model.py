# File: backend/app/models/maintenance/maintenance_team_model.py
import uuid
# --- CORREÇÃO: Importar o TIPO UUID do SQLAlchemy e o NOVO Boolean ---
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
# --- FIM DA CORREÇÃO ---
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from app.core.database import Base

class MaintenanceTeam(Base):
    """
    Modelo da Tabela para Equipes de Manutenção (MaintenanceTeam).
    Define os grupos de trabalho responsáveis pela manutenção.
    """
    __tablename__ = "maintenance_teams"

    # --- CORREÇÃO: Sintaxe 'mapped_column' corrigida ---
    # A anotação de tipo (Mapped[uuid.UUID]) usa o 'uuid' do Python.
    # A função (mapped_column) usa o 'PG_UUID' do SQLAlchemy.
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, unique=True)
    
    # --- NOVA COLUNA (Soft Delete) ---
    # Adicionamos este campo para que o CRUDBase.remove() 
    # possa fazer o soft delete (definindo isto como False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    # --- FIM DA NOVA COLUNA ---

    # --- Relacionamentos ---

    technicians: Mapped[List["Technician"]] = relationship(
        "Technician", 
        back_populates="team",
        cascade="all, delete-orphan"
    )

    assigned_work_orders: Mapped[List["WorkOrder"]] = relationship(
        "WorkOrder", 
        back_populates="assigned_to_team"
    )

    pm_plans: Mapped[List["PMPlan"]] = relationship(
        "PMPlan", 
        back_populates="assigned_to_team"
    )