# File: backend/app/modules/maintenance/work_orders/tasks/work_order_tasks_crud.py

import uuid
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc

from app.core.crud_base import CRUDBase
from app.models.maintenance.work_order_task_model import WorkOrderTask
from .work_order_tasks_schemas import WorkOrderTaskCreate, WorkOrderTaskUpdate


class CRUDWorkOrderTask(CRUDBase[WorkOrderTask, WorkOrderTaskCreate, WorkOrderTaskUpdate]):
    """
    Classe CRUD especializada para as Tarefas (Checklist)
    da Ordem de Serviço.
    """

    def get_by_id_and_wo_id(
        self, 
        db: Session, 
        *, 
        task_id: uuid.UUID, 
        work_order_id: uuid.UUID
    ) -> Optional[WorkOrderTask]:
        """
        Obtém uma tarefa específica, garantindo que ela pertence
        à Ordem de Serviço (pai) correta.
        """
        statement = select(self.model).where(
            self.model.id == task_id,
            self.model.work_order_id == work_order_id
        )
        return db.scalars(statement).first()

    def get_multi_by_work_order(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderTask]:
        """
        Obtém todas as tarefas (checklist) para uma Ordem de Serviço
        específica, ordenadas pelo 'order_index'.
        """
        statement = select(self.model)\
            .where(self.model.work_order_id == work_order_id)\
            .order_by(asc(self.model.order_index))
            
        return db.scalars(statement).all()

    def create_task_for_wo(
        self,
        db: Session,
        *,
        obj_in: WorkOrderTaskCreate,
        work_order_id: uuid.UUID
    ) -> WorkOrderTask:
        """
        Cria uma nova tarefa (item de checklist) para uma OS,
        calculando automaticamente o próximo 'order_index'.
        """
        
        # 1. Calcula o próximo índice de ordenação
        stmt = select(func.max(self.model.order_index))\
            .where(self.model.work_order_id == work_order_id)
        
        max_index = db.scalars(stmt).first()
        next_index = (max_index or 0) + 1
        
        # 2. Cria o objeto
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(
            **obj_in_data,
            work_order_id=work_order_id,
            order_index=next_index,
            completed=False # Garante que a nova tarefa começa desmarcada
        )
        
        # 3. Salva no banco
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    # Nota: O método 'update' do CRUDBase genérico será usado
    # para marcar tarefas como completas ou editar a descrição.
    
    # Nota: O método 'remove' do CRUDBase genérico será usado
    # (executará um HARD DELETE, que está correto para esta entidade).


# Instância única da classe CRUD
crud_work_order_task = CRUDWorkOrderTask(WorkOrderTask)