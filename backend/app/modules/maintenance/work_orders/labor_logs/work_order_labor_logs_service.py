# File: backend/app/modules/maintenance/work_orders/labor_logs/work_order_labor_logs_service.py

import uuid
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.maintenance.work_order_labor_log_model import WorkOrderLaborLog
from app.models.administration.user_model import Usuario

# Importa o CRUD e Schemas desta sub-fatia
from .work_order_labor_logs_crud import crud_work_order_labor_log, CRUDWorkOrderLaborLog
from .work_order_labor_logs_schemas import (
    WorkOrderLaborLogCreate, 
    WorkOrderLaborLogUpdate, 
    WorkOrderLaborLogRead
)

# Importa o serviço "pai" (WorkOrder) para validação
from ..work_orders_service import work_order_service
# Importa o CRUD de Técnicos para validar o technician_id
from app.modules.maintenance.technicians.technicians_crud import technician_crud


class WorkOrderLaborLogService:
    """
    Camada de Serviço (Lógica de Negócio) para os Apontamentos
    de Mão de Obra (Labor Logs) da Ordem de Serviço.
    """

    def __init__(self, crud_labor_log: CRUDWorkOrderLaborLog):
        self.crud_labor_log = crud_labor_log

    def _get_labor_log_or_404(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID, 
        labor_log_id: uuid.UUID
    ) -> WorkOrderLaborLog:
        """
        Helper privado: Obtém um apontamento específico, garantindo que
        a OS pai existe e que o apontamento pertence a ela.
        """
        # 1. Valida se a OS "pai" existe (o service já levanta 404)
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca o apontamento (o crud valida a relação)
        db_log = self.crud_labor_log.get_by_id_and_wo_id(
            db=db, 
            labor_log_id=labor_log_id, 
            work_order_id=work_order_id
        )
        
        if not db_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Apontamento de mão de obra não encontrado nesta Ordem de Serviço."
            )
        return db_log

    def _validate_foreign_keys(
        self, 
        db: Session, 
        *, 
        technician_id: uuid.UUID
    ):
        """Helper privado para validar o técnico."""
        if technician_id:
            technician = technician_crud.get(db, id=technician_id)
            if not technician:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Técnico com ID {technician_id} não encontrado."
                )
            if not technician.is_active: # Respeita o soft-delete
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Não é possível associar o Técnico '{technician.name}', pois ele está inativo."
                )

    def get_labor_logs_for_wo(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderLaborLogRead]:
        """
        Obtém todos os apontamentos de horas para uma OS específica.
        """
        # 1. Valida se a OS "pai" existe
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca os apontamentos (o crud já os ordena e otimiza)
        return self.crud_labor_log.get_multi_by_work_order(
            db=db, 
            work_order_id=work_order_id
        )

    def create_labor_log_for_wo(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        obj_in: WorkOrderLaborLogCreate,
        current_user: Usuario
    ) -> WorkOrderLaborLogRead:
        """
        Cria um novo apontamento de horas para uma OS.
        O 'created_by_user_id' é preenchido automaticamente.
        """
        # 1. Valida se a OS "pai" existe
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Valida o Técnico
        self._validate_foreign_keys(db, technician_id=obj_in.technician_id)
        
        # 3. Cria o apontamento
        return self.crud_labor_log.create_labor_log(
            db=db,
            obj_in=obj_in,
            work_order_id=work_order_id,
            created_by_user_id=current_user.id
        )

    def update_labor_log(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        labor_log_id: uuid.UUID,
        obj_in: WorkOrderLaborLogUpdate
    ) -> WorkOrderLaborLogRead:
        """
        Atualiza um apontamento de horas.
        """
        # 1. Obtém o apontamento (helper já valida a OS pai e o apontamento)
        db_log = self._get_labor_log_or_404(
            db, 
            work_order_id=work_order_id, 
            labor_log_id=labor_log_id
        )
        
        # 2. Converte o schema de update para dict
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # 3. Valida o técnico (se ele for alterado)
        if "technician_id" in update_data:
            self._validate_foreign_keys(
                db, 
                technician_id=update_data["technician_id"]
            )
        
        # 4. Aplica a atualização (usando o 'update' genérico do CRUDBase)
        return self.crud_labor_log.update(
            db=db, 
            db_obj=db_log, 
            obj_in=update_data
        )

    def delete_labor_log(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        labor_log_id: uuid.UUID
    ) -> WorkOrderLaborLogRead:
        """
        Elimina (Hard Delete) um apontamento de horas.
        """
        # 1. Obtém o apontamento (helper já valida a OS pai e o apontamento)
        db_log = self._get_labor_log_or_404(
            db, 
            work_order_id=work_order_id, 
            labor_log_id=labor_log_id
        )
        
        # 2. Remove o apontamento (o CRUDBase fará um HARD DELETE)
        return self.crud_labor_log.remove(db=db, id=db_log.id)

# Instância única do serviço
work_order_labor_log_service = WorkOrderLaborLogService(crud_work_order_labor_log)