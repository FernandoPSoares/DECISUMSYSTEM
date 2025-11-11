# File: backend/app/models/maintenance/technician_model.py

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Optional
from app.core.database import Base
# --- CORREÇÃO AQUI ---
# Importar 'Usuario' em vez de 'User'
from app.models.administration.user_model import Usuario
# --- FIM DA CORREÇÃO ---
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Technician(Base):
    """
    Representa um técnico de manutenção, que é um Perfil 
    ligado a um Utilizador do sistema.
    """
    __tablename__ = 'maintenance_technicians'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ligação One-to-One com o utilizador
    # A ForeignKey 'usuarios.id' parece estar correta pela sua nomenclatura
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), unique=True, nullable=False)
    
    # Ligação à equipa de manutenção
    team_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_teams.id'), nullable=True)

    # --- CORREÇÃO AQUI ---
    # O tipo do relacionamento é 'Usuario'
    user: Mapped["Usuario"] = relationship(back_populates="technician_profile")
    # --- FIM DA CORREÇÃO ---

    team: Mapped[Optional["MaintenanceTeam"]] = relationship(back_populates="technicians")

    # Relacionamentos futuros
    work_orders: Mapped[List["WorkOrder"]] = relationship(back_populates="assigned_technician")
    labor_logs: Mapped[List["WorkOrderLaborLog"]] = relationship(back_populates="technician")