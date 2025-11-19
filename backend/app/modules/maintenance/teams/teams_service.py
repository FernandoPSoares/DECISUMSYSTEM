# File: backend/app/modules/maintenance/teams/teams_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
import uuid

# Importa o CRUD e os Schemas que criámos nos passos anteriores
from .teams_crud import maintenance_team_crud
from .teams_schemas import MaintenanceTeamCreate, MaintenanceTeamUpdate
from app.models.maintenance.maintenance_team_model import MaintenanceTeam

class MaintenanceTeamService:
    """
    Serviço para a lógica de negócio das Equipas de Manutenção.
    Orquestra as operações de CRUD e aplica as regras de negócio.
    """

    def get_team_by_id(self, db: Session, team_id: uuid.UUID) -> MaintenanceTeam:
        """
        Obtém uma equipa pelo seu ID.
        Lança HTTPException 404 se não for encontrada.
        (Nota: O CRUDBase.get() permite obter itens inativos pelo ID,
        o que é útil para ver o histórico.)
        """
        team = maintenance_team_crud.get(db, id=team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipa com o ID {team_id} não encontrada.",
            )
        return team

    def get_all_teams(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[MaintenanceTeam]:
        """
        Obtém uma lista paginada de todas as equipas ATIVAS.
        (Graças ao CRUDBase alterado, get_multi() agora
        filtra por 'is_active = True' por defeito.)
        """
        return maintenance_team_crud.get_multi(db, skip=skip, limit=limit)

    def create_team(self, db: Session, *, team_in: MaintenanceTeamCreate) -> MaintenanceTeam:
        """
        Cria uma nova equipa de manutenção.
        
        Regra de Negócio: Não permite a criação de equipas com nomes duplicados
        (entre as equipas ativas).
        """
        # Graças ao teams_crud.py alterado, get_by_name() agora
        # filtra por 'is_active = True'.
        existing_team = maintenance_team_crud.get_by_name(db, name=team_in.name)
        if existing_team:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Uma equipa ativa com o nome '{team_in.name}' já existe.",
            )
        
        # Se passar na verificação, cria a equipa
        team = maintenance_team_crud.create(db, obj_in=team_in)
        return team

    def update_team(
        self, db: Session, *, team_id: uuid.UUID, team_in: MaintenanceTeamUpdate
    ) -> MaintenanceTeam:
        """
        Atualiza uma equipa de manutenção.
        
        Regra de Negócio: Se um novo nome for fornecido, verifica se já existe
        entre as equipas ativas.
        """
        # 1. Garante que a equipa existe (o get() encontra mesmo se inativa)
        team_db = self.get_team_by_id(db, team_id=team_id)
        
        # 2. Regra de Negócio: Verifica se o novo nome (se fornecido) já está em uso
        if team_in.name and team_in.name != team_db.name:
            # O get_by_name() já filtra por 'is_active',
            # garantindo que não colidimos com outro nome ativo.
            existing_team = maintenance_team_crud.get_by_name(db, name=team_in.name)
            if existing_team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Uma equipa ativa com o nome '{team_in.name}' já existe.",
                )
        
        # 3. Atualiza a equipa
        team = maintenance_team_crud.update(db, db_obj=team_db, obj_in=team_in)
        return team

    def delete_team(self, db: Session, *, team_id: uuid.UUID) -> MaintenanceTeam:
        """
        Elimina (logicamente) uma equipa de manutenção.
        """
        # 1. Garante que a equipa existe antes de tentar eliminar
        team_to_delete = self.get_team_by_id(db, team_id=team_id)
        
        # (Futuramente, podemos adicionar regras - ex: "Não eliminar equipa se tiver OSs ativas")
        
        # --- LÓGICA DE SOFT DELETE ---
        # Graças ao CRUDBase alterado, o .remove() agora faz
        # um soft delete (UPDATE is_active = False) automaticamente.
        team = maintenance_team_crud.remove(db, id=team_id)
        # --- FIM DA LÓGICA ---
        
        # Se o 'team' for None (não encontrado), o .remove() da CRUDBase já
        # teria retornado None, mas o nosso 'get_team_by_id' já tratou o 404.
        # Retornamos o objeto atualizado (agora com is_active=False).
        return team

# Cria uma instância única (singleton) do serviço
maintenance_team_service = MaintenanceTeamService()