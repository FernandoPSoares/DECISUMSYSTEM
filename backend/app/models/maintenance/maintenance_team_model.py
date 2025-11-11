import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class MaintenanceTeam(Base):
    """
    Modelo da Tabela para Equipes de Manutenção (MaintenanceTeam).
    Define os grupos de trabalho responsáveis pela manutenção.
    """
    __tablename__ = "maintenance_teams"

    # Chave primária UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Nome da equipe (ex: "Mecânica A", "Elétrica")
    # Deve ser único e indexado para buscas rápidas.
    name = Column(String(100), nullable=False, index=True, unique=True)

    # --- Relacionamentos (Definidos aqui, mas implementados nos outros modelos) ---

    # Relacionamento One-to-Many: Uma equipe para muitos técnicos
    # O 'back_populates' aponta para o atributo 'team' no modelo 'Technician'
    technicians = relationship(
        "Technician", 
        back_populates="team",
        cascade="all, delete-orphan" # Opcional: se deletar a equipe, deleta os técnicos (discutível)
    )

    # Relacionamento One-to-Many: Uma equipe para muitas Ordens de Serviço
    # O 'back_populates' aponta para 'assigned_team' no modelo 'WorkOrder'
    assigned_work_orders = relationship(
        "WorkOrder", 
        back_populates="assigned_team"
    )

    # Relacionamento One-to-Many: Uma equipe para muitos Planos de Preventiva
    # O 'back_populates' aponta para 'assigned_team' no modelo 'PMPlan'
    pm_plans = relationship(
        "PMPlan", 
        back_populates="assigned_team"
    )