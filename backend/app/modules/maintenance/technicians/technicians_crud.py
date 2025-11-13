# File: backend/app/modules/maintenance/technicians/technicians_crud.py

import uuid
from sqlalchemy.orm import Session, joinedload
from typing import List

# Importa a base de CRUD que o seu projeto já usa
from app.core.crud_base import CRUDBase

# Modelos com os quais este CRUD irá interagir
from app.models.maintenance.technician_model import Technician
from app.models.administration.user_model import Usuario
from app.models.maintenance.maintenance_team_model import MaintenanceTeam

# Schemas (para type hinting da classe base)
from .technicians_schemas import TechnicianCreate, TechnicianUpdate


class CRUDTechnician(CRUDBase[Technician, TechnicianCreate, TechnicianUpdate]):
    """
    Classe CRUD especializada para Técnicos de Manutenção.
    Estende o CRUDBase para incluir carregamento otimizado (eager loading)
    dos relacionamentos 'user' e 'team' e para filtrar por 'is_active'.
    """

    # --- Overrides com Eager Loading ---
    # Sobrescrevemos os métodos 'get' padrão para otimizar as consultas,
    # carregando os dados relacionados (user e team) na mesma query.

    def get_with_relations(self, db: Session, id: uuid.UUID) -> Technician | None:
        """
        Obtém um único técnico ATIVO pelo ID, incluindo os seus relacionamentos
        (user e team) de forma otimizada (eager loading).
        """
        return db.query(self.model).options(
            joinedload(self.model.user),  # Carrega o perfil do Usuario
            joinedload(self.model.team)  # Carrega a Equipa de Manutenção
        ).filter(
            self.model.id == id,
            self.model.is_active == True  # <-- PACTO SOFT DELETE APLICADO
        ).first()

    def get_multi_with_relations(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Technician]:
        """
        Obtém uma lista de técnicos ATIVOS, incluindo os seus relacionamentos
        (user e team) de forma otimizada (eager loading).
        """
        return db.query(self.model).options(
            joinedload(self.model.user),  # Carrega o perfil do Usuario
            joinedload(self.model.team)  # Carrega a Equipa de Manutenção
        ).filter(
            self.model.is_active == True  # <-- PACTO SOFT DELETE APLICADO
        ).offset(skip).limit(limit).all()

    # --- Métodos Personalizados ---

    def get_by_user_id(self, db: Session, *, user_id: uuid.UUID) -> Technician | None:
        """
        Verifica se já existe um técnico ATIVO associado a um determinado ID de utilizador.
        Isto é crucial para a lógica de negócio (evitar duplicados).
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.is_active == True  # <-- PACTO SOFT DELETE APLICADO
        ).first()


# Cria uma instância única (singleton) do CRUD
technician_crud = CRUDTechnician(Technician)