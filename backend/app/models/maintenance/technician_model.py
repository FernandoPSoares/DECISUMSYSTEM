# File: backend/app/models/maintenance/technician_model.py
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional

# Importa a nossa Base partilhada
from app.core.database import Base
# Importa o modelo de Utilizador do módulo de administração
from app.models.administration.user_model import Usuario

class Technician(Base):
    """
    Representa um Técnico de Manutenção.
    Está ligado a um Utilizador do sistema (One-to-One) e
    pertence a uma Equipa de Manutenção (Many-to-One).
    """
    __tablename__ = 'maintenance_technicians'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Chave estrangeira para o Utilizador (One-to-One)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('usuarios.id'), unique=True, nullable=False, index=True)
    
    # Chave estrangeira para a Equipa (Many-to-One)
    team_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('maintenance_teams.id'), nullable=True, index=True)

    # --- NOVO CAMPO (Soft Delete) ---
    # Adiciona o campo 'is_active' para suportar a exclusão lógica.
    # Isto é crucial para manter o histórico (OSs antigas) ligado a técnicos inativos.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    # --- FIM DO NOVO CAMPO ---

    # --- Relacionamentos ---

    # --- CORREÇÃO DO ERRO ---
    # O 'back_populates' foi corrigido de "technician_profile" para "technician_record",
    # para corresponder ao nome da propriedade no modelo Usuario.
    user: Mapped["Usuario"] = relationship(
        "Usuario", 
        back_populates="technician_record"
    )
    # --- FIM DA CORREÇÃO ---
    
    # Relacionamento Many-to-One com MaintenanceTeam
    team: Mapped[Optional["MaintenanceTeam"]] = relationship(
        "MaintenanceTeam", 
        back_populates="technicians"
    )

    # Relacionamento One-to-Many com WorkOrder (Ordens de Serviço atribuídas)
    assigned_work_orders: Mapped[List["WorkOrder"]] = relationship(
        back_populates="assigned_to_technician"
    )

    # --- RELAÇÃO (Back-populates de work_order_labor_log_model.py) ---
    labor_logs: Mapped[List["WorkOrderLaborLog"]] = relationship(
        back_populates="technician"
    )
    # --- FIM DA RELAÇÃO ---

    # --- NOVA RELAÇÃO (Back-populates de pm_plan_model.py) ---
    # Planos de Preventiva atribuídos diretamente a este técnico
    pm_plans: Mapped[List["PMPlan"]] = relationship(
        back_populates="assigned_to_technician"
    )
    # --- FIM DA NOVA RELAÇÃO ---