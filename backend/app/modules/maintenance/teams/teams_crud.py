# File: backend/app/modules/maintenance/teams/teams_crud.py

from sqlalchemy.orm import Session
from typing import Optional

# Importa a classe CRUDBase, o modelo SQLAlchemy e os schemas Pydantic
from app.core.crud_base import CRUDBase
from app.models.maintenance.maintenance_team_model import MaintenanceTeam
from .teams_schemas import MaintenanceTeamCreate, MaintenanceTeamUpdate

class CRUDMaintenanceTeam(CRUDBase[MaintenanceTeam, MaintenanceTeamCreate, MaintenanceTeamUpdate]):
    """
    Classe CRUD para o modelo MaintenanceTeam.
    Herda de CRUDBase e adiciona métodos de consulta específicos
    para equipas de manutenção.
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[MaintenanceTeam]:
        """
        Procura uma equipa de manutenção ATIVA pelo nome.
        
        Args:
            db (Session): A sessão da base de dados.
            name (str): O nome da equipa a procurar.
            
        Returns:
            Optional[MaintenanceTeam]: A equipa encontrada ou None.
        """
        # --- ALTERAÇÃO SOFT DELETE ---
        # Adicionamos 'self.model.is_active == True' para garantir
        # que esta consulta personalizada só retorna equipas ativas.
        return db.query(self.model).filter(
            self.model.name == name, 
            self.model.is_active == True
        ).first()
        # --- FIM DA ALTERAÇÃO ---

# Cria uma instância única (singleton) da classe CRUD para ser usada
# pelos serviços e routers.
maintenance_team_crud = CRUDMaintenanceTeam(MaintenanceTeam)