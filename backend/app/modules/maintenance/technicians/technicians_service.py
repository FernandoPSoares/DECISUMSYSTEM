# File: backend/app/modules/maintenance/technicians/technicians_service.py

import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

# Schemas (Contratos)
from .technicians_schemas import TechnicianCreate, TechnicianUpdate
# CRUD (Operário da BD)
from .technicians_crud import technician_crud
# Modelo (para type hinting)
from app.models.maintenance.technician_model import Technician

# --- Dependências de Outras Fatias/Módulos ---
# Precisamos de validar se o 'user_id' e o 'team_id' existem.

# 1. Para validar o user_id, usamos o crud de usuários
from app.modules.administration.users.users_crud import usuario_crud
# 2. Para validar o team_id, usamos o serviço de equipas (que já tem um 404)
from app.modules.maintenance.teams.teams_service import maintenance_team_service


class TechnicianService:
    """
    Serviço para a lógica de negócio dos Técnicos de Manutenção.
    """

    def get_technician_by_id(self, db: Session, technician_id: uuid.UUID) -> Technician:
        """
        Obtém um técnico ATIVO pelo seu ID, com dados de utilizador e equipa.
        Lança HTTPException 404 se não for encontrado.
        """
        # Usamos o método otimizado do nosso CRUD
        # (que agora filtra por is_active = True)
        technician = technician_crud.get_with_relations(db, id=technician_id)
        if not technician:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Técnico com o ID {technician_id} não encontrado.",
            )
        return technician

    def get_all_technicians(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Technician]:
        """
        Obtém uma lista paginada de todos os técnicos ATIVOS.
        """
        # Usamos o método otimizado do nosso CRUD
        # (que agora filtra por is_active = True)
        return technician_crud.get_multi_with_relations(db, skip=skip, limit=limit)

    def create_technician(
        self, db: Session, *, technician_in: TechnicianCreate
    ) -> Technician:
        """
        Cria um novo Técnico.
        
        Regras de Negócio:
        1. O 'user_id' fornecido deve pertencer a um 'Usuario' existente.
        2. O 'user_id' não pode já estar associado a outro técnico (1-para-1).
        3. O 'team_id' (se fornecido) deve pertencer a uma 'MaintenanceTeam' ATIVA.
        """
        
        # Regra 1: Validar user_id
        user = usuario_crud.get(db, id=technician_in.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com o ID {technician_in.user_id} não encontrado. Não é possível criar o técnico.",
            )

        # Regra 2: Validar 1-para-1
        # (O crud.get_by_user_id agora verifica TODOS os registos, ativos ou inativos)
        existing_technician = technician_crud.get_by_user_id(db, user_id=technician_in.user_id)
        if existing_technician:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Este usuário (ID: {technician_in.user_id}) já está associado a um perfil de técnico.",
            )

        # Regra 3: Validar team_id (se existir)
        if technician_in.team_id:
            # Usamos o serviço de equipas, que já trata do 404 e filtra por ativo
            maintenance_team_service.get_team_by_id(db, team_id=technician_in.team_id)

        # Se todas as regras passarem, cria o técnico
        technician = technician_crud.create(db, obj_in=technician_in)
        
        # Retornamos o técnico com as relações carregadas para corresponder ao schema 'Read'
        # (O 'create' simples não carrega as relações por defeito)
        db.refresh(technician) # Garante que temos o objeto acabado de criar
        return self.get_technician_by_id(db, technician_id=technician.id)


    def update_technician(
        self, db: Session, *, technician_id: uuid.UUID, technician_in: TechnicianUpdate
    ) -> Technician:
        """
        Atualiza um Técnico (atualmente, apenas a sua equipa).
        
        Regra de Negócio:
        1. O 'team_id' (se fornecido) deve pertencer a uma 'MaintenanceTeam' ATIVA.
        """
        # Garante que o técnico existe
        technician_db = self.get_technician_by_id(db, technician_id=technician_id)
        
        # Regra 1: Validar team_id (se foi alterado)
        if (
            technician_in.team_id is not None and
            technician_in.team_id != technician_db.team_id
        ):
            # Valida a nova equipa
            maintenance_team_service.get_team_by_id(db, team_id=technician_in.team_id)

        # Atualiza o técnico
        technician = technician_crud.update(db, db_obj=technician_db, obj_in=technician_in)
        
        # Re-carrega as relações para garantir que a resposta está completa
        return self.get_technician_by_id(db, technician_id=technician.id)

    # --- MÉTODO DELETE CORRIGIDO (Soft Delete) ---
    def delete_technician(self, db: Session, *, technician_id: uuid.UUID) -> Technician:
        """
        Elimina (logicamente) um Técnico.
        Define 'is_active = False' no registo.
        """
        # 1. Garante que o técnico ATIVO existe e carrega as suas relações (user, team)
        #    O 'get_technician_by_id' já faz isso e já trata o 404.
        technician_to_delete = self.get_technician_by_id(db, technician_id=technician_id)

        # (Regra Futura: Não permitir eliminar se o técnico tiver OSs abertas, etc.)

        # 2. Chama o .remove() da CRUDBase, que faz o SOFT DELETE (UPDATE is_active = False)
        # O 'deleted_technician' é o objeto atualizado (com is_active=False),
        # mas *sem* os relacionamentos 'user' e 'team' carregados.
        deleted_technician = technician_crud.remove(db, id=technician_id)

        # 3. Prepara a resposta para o frontend.
        # O router espera um schema 'TechnicianRead' (que inclui user e team).
        # Copiamos as relações do objeto que tínhamos carregado no passo 1
        # para o objeto atualizado (com is_active=False).
        deleted_technician.user = technician_to_delete.user
        deleted_technician.team = technician_to_delete.team
        
        return deleted_technician # Retorna o objeto atualizado *com* as relações
    # --- FIM DA CORREÇÃO ---

# Cria uma instância única (singleton) do serviço
technician_service = TechnicianService()