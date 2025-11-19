# File: backend/app/modules/maintenance/work_orders/logs/work_order_logs_crud.py

import uuid
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.core.crud_base import CRUDBase
from app.models.maintenance.work_order_log_model import WorkOrderLog
from .work_order_logs_schemas import WorkOrderLogCreate

# Nota: O modelo WorkOrderLog não tem um schema de 'Update'.
# Passamos 'BaseModel' como o marcador de posição 'UpdateSchemaType'
# para o CRUDBase genérico.
class CRUDWorkOrderLog(CRUDBase[WorkOrderLog, WorkOrderLogCreate, BaseModel]):
    """
    Classe CRUD especializada para os Logs de Atividade (Comentários)
    da Ordem de Serviço.
    """

    def get(self, db: Session, id: uuid.UUID) -> Optional[WorkOrderLog]:
        """
        Obtém um log específico, otimizando o carregamento do
        utilizador que o criou (created_by_user).
        """
        statement = select(self.model).where(self.model.id == id).options(
            joinedload(self.model.created_by_user)
        )
        return db.scalars(statement).first()

    def get_multi_by_work_order(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderLog]:
        """
        Obtém todos os logs (comentários) para uma Ordem de Serviço específica.
        
        Os logs são otimizados (joinedload) e ordenados cronologicamente.
        """
        statement = select(self.model)\
            .where(self.model.work_order_id == work_order_id)\
            .options(joinedload(self.model.created_by_user))\
            .order_by(self.model.created_at.asc()) # Do mais antigo para o mais novo
            
        return db.scalars(statement).all()

    def create_log(
        self, 
        db: Session, 
        *, 
        obj_in: WorkOrderLogCreate,
        work_order_id: uuid.UUID,
        created_by_user_id: uuid.UUID
    ) -> WorkOrderLog:
        """
        Cria um novo log (comentário) associado a uma OS e a um Utilizador.
        Este método substitui o 'create' genérico do CRUDBase.
        """
        # Converte o schema Pydantic para um dict
        obj_in_data = obj_in.model_dump()
        
        # Cria a instância do modelo, adicionando as chaves estrangeiras
        db_obj = self.model(
            **obj_in_data,
            work_order_id=work_order_id,
            created_by_user_id=created_by_user_id
        )
        
        # Salva no banco
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Nota: Não precisamos de 'update'. Logs são imutáveis.
    
    # Nota: O 'remove' do CRUDBase será usado. Como o 'WorkOrderLog'
    # não tem 'is_active', o CRUDBase executará um HARD DELETE,
    # o que está correto para esta entidade (se a política
    # de negócio permitir a exclusão de comentários).


# Instância única da classe CRUD
crud_work_order_log = CRUDWorkOrderLog(WorkOrderLog)