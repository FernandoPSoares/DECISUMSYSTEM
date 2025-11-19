# File: backend/app/modules/maintenance/work_orders/labor_logs/work_order_labor_logs_crud.py

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, asc

from app.core.crud_base import CRUDBase
from app.models.maintenance.work_order_labor_log_model import WorkOrderLaborLog
from .work_order_labor_logs_schemas import (
    WorkOrderLaborLogCreate, 
    WorkOrderLaborLogUpdate
)


class CRUDWorkOrderLaborLog(CRUDBase[WorkOrderLaborLog, WorkOrderLaborLogCreate, WorkOrderLaborLogUpdate]):
    """
    Classe CRUD especializada para os Apontamentos de Mão de Obra (LaborLog)
    da Ordem de Serviço.
    """

    def get_by_id_and_wo_id(
        self, 
        db: Session, 
        *, 
        labor_log_id: uuid.UUID, 
        work_order_id: uuid.UUID
    ) -> Optional[WorkOrderLaborLog]:
        """
        Obtém um apontamento específico, garantindo que ele pertence
        à Ordem de Serviço (pai) correta e otimiza o carregamento
        das relações (técnico e utilizador).
        """
        statement = select(self.model).where(
            self.model.id == labor_log_id,
            self.model.work_order_id == work_order_id
        ).options(
            joinedload(self.model.technician),
            joinedload(self.model.created_by_user)
        )
        return db.scalars(statement).first()

    def get_multi_by_work_order(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderLaborLog]:
        """
        Obtém todos os apontamentos de horas para uma Ordem de Serviço
        específica, ordenados pelo início e otimizados.
        """
        statement = select(self.model)\
            .where(self.model.work_order_id == work_order_id)\
            .options(
                joinedload(self.model.technician),
                joinedload(self.model.created_by_user)
            )\
            .order_by(asc(self.model.start_time))
            
        return db.scalars(statement).all()

    def create_labor_log(
        self,
        db: Session,
        *,
        obj_in: WorkOrderLaborLogCreate,
        work_order_id: uuid.UUID,
        created_by_user_id: uuid.UUID
    ) -> WorkOrderLaborLog:
        """
        Cria um novo apontamento de horas para uma OS.
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
    # para editar apontamentos (se a regra de negócio permitir).
    
    # Nota: O método 'remove' do CRUDBase genérico será usado
    # (executará um HARD DELETE, que está correto para esta entidade).


# Instância única da classe CRUD
crud_work_order_labor_log = CRUDWorkOrderLaborLog(WorkOrderLaborLog)