# File: backend/app/modules/maintenance/work_orders/tasks/work_order_tasks_service.py

import uuid
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.maintenance.work_order_task_model import WorkOrderTask
from app.models.administration.user_model import Usuario

# Importa o CRUD e Schemas desta sub-fatia
from .work_order_tasks_crud import crud_work_order_task, CRUDWorkOrderTask
from .work_order_tasks_schemas import WorkOrderTaskCreate, WorkOrderTaskUpdate, WorkOrderTaskRead

# Importa o serviço da fatia "pai" (WorkOrder) para validação
from ..work_orders_service import work_order_service


class WorkOrderTaskService:
    """
    Camada de Serviço (Lógica de Negócio) para as Tarefas (Checklist)
    da Ordem de Serviço.
    """

    def __init__(self, crud_task: CRUDWorkOrderTask):
        self.crud_task = crud_task

    def _get_task_or_404(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID, 
        task_id: uuid.UUID
    ) -> WorkOrderTask:
        """
        Helper privado: Obtém uma tarefa específica, garantindo que
        a OS pai existe e que a tarefa pertence a ela.
        Levanta 404 se a OS ou a Tarefa não forem encontradas.
        """
        # 1. Valida se a OS "pai" existe (o service já levanta 404)
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca a tarefa específica (o crud valida a relação)
        db_task = self.crud_task.get_by_id_and_wo_id(
            db=db, 
            task_id=task_id, 
            work_order_id=work_order_id
        )
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa (item do checklist) não encontrada nesta Ordem de Serviço."
            )
        return db_task

    def get_tasks_for_wo(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderTaskRead]:
        """
        Obtém todas as tarefas (checklist) para uma OS específica.
        """
        # 1. Valida se a OS "pai" existe
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca as tarefas (o crud já as ordena por 'order_index')
        return self.crud_task.get_multi_by_work_order(
            db=db, 
            work_order_id=work_order_id
        )

    def create_task_for_wo(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        obj_in: WorkOrderTaskCreate
    ) -> WorkOrderTaskRead:
        """
        Cria uma nova tarefa (item de checklist) para uma OS.
        O CRUD irá calcular automaticamente o 'order_index'.
        """
        # 1. Valida se a OS "pai" existe
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Cria a tarefa
        return self.crud_task.create_task_for_wo(
            db=db,
            obj_in=obj_in,
            work_order_id=work_order_id
        )

    def update_task(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        task_id: uuid.UUID,
        obj_in: WorkOrderTaskUpdate
    ) -> WorkOrderTaskRead:
        """
        Atualiza uma tarefa:
        - Marca como concluída/não concluída
        - Edita a descrição
        - Altera a ordem (order_index)
        """
        # 1. Obtém a tarefa (helper já valida a OS pai e a tarefa)
        db_task = self._get_task_or_404(
            db, 
            work_order_id=work_order_id, 
            task_id=task_id
        )
        
        # 2. Converte o schema de update para dict
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # (Lógica de Negócio Futura: Se 'completed' for alterado,
        # poderíamos adicionar um WorkOrderLog automático)
        
        # 3. Aplica a atualização (usando o 'update' genérico do CRUDBase)
        return self.crud_task.update(
            db=db, 
            db_obj=db_task, 
            obj_in=update_data
        )

    def delete_task(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        task_id: uuid.UUID
    ) -> WorkOrderTaskRead:
        """
        Elimina (Hard Delete) uma tarefa do checklist.
        """
        # 1. Obtém a tarefa (helper já valida a OS pai e a tarefa)
        db_task = self._get_task_or_404(
            db, 
            work_order_id=work_order_id, 
            task_id=task_id
        )
        
        # 2. Remove a tarefa
        # (O CRUDBase fará um HARD DELETE, pois WorkOrderTask não
        # tem 'is_active', o que é o comportamento esperado para tarefas)
        return self.crud_task.remove(db=db, id=db_task.id)

# Instância única do serviço
work_order_task_service = WorkOrderTaskService(crud_work_order_task)