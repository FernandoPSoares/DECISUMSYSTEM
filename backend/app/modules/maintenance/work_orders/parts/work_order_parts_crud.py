# File: backend/app/modules/maintenance/work_orders/parts/work_order_parts_crud.py

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, asc

from app.core.crud_base import CRUDBase
from app.models.maintenance.work_order_parts_model import WorkOrderPartUsage
from .work_order_parts_schemas import (
    WorkOrderPartUsageCreate, 
    WorkOrderPartUsageUpdate
)


class CRUDWorkOrderPartUsage(CRUDBase[WorkOrderPartUsage, WorkOrderPartUsageCreate, WorkOrderPartUsageUpdate]):
    """
    Classe CRUD especializada para o Consumo de Peças (PartUsage)
    da Ordem de Serviço.
    """

    def get_by_id_and_wo_id(
        self, 
        db: Session, 
        *, 
        part_usage_id: uuid.UUID, 
        work_order_id: uuid.UUID
    ) -> Optional[WorkOrderPartUsage]:
        """
        Obtém um registo de consumo específico, garantindo que ele
        pertence à Ordem de Serviço (pai) correta e otimiza o
        carregamento das relações (utilizador e produto).
        """
        statement = select(self.model).where(
            self.model.id == part_usage_id,
            self.model.work_order_id == work_order_id
        ).options(
            joinedload(self.model.created_by_user),
            joinedload(self.model.product) # Otimização: carrega os dados do produto
        )
        return db.scalars(statement).first()

    def get_multi_by_work_order(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderPartUsage]:
        """
        Obtém todos os consumos de peças para uma Ordem de Serviço
        específica, ordenados por data de criação e otimizados.
        """
        statement = select(self.model)\
            .where(self.model.work_order_id == work_order_id)\
            .options(
                joinedload(self.model.created_by_user),
                joinedload(self.model.product) # Otimização: carrega os dados do produto
            )\
            .order_by(asc(self.model.created_at))
            
        return db.scalars(statement).all()

    def create_part_usage(
        self,
        db: Session,
        *,
        obj_in: WorkOrderPartUsageCreate,
        work_order_id: uuid.UUID,
        created_by_user_id: uuid.UUID
    ) -> WorkOrderPartUsage:
        """
        Cria um novo registo de consumo de peça para uma OS.
        Este método substitui o 'create' genérico do CRUDBase.
        """
        
        # Cria o objeto a partir do schema
        obj_in_data = obj_in.model_dump()
        
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
    
    # Nota: O método 'update' do CRUDBase genérico será usado
    # para editar o consumo (se a regra de negócio permitir).
    
    # Nota: O método 'remove' do CRUDBase genérico será usado
    # (executará um HARD DELETE, que está correto para esta entidade).


# Instância única da classe CRUD
crud_work_order_part_usage = CRUDWorkOrderPartUsage(WorkOrderPartUsage)