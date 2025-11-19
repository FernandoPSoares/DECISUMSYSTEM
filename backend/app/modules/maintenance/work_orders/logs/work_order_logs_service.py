# File: backend/app/modules/maintenance/work_orders/logs/work_order_logs_service.py

import uuid
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.administration.user_model import Usuario

# Importa o CRUD desta sub-fatia
from .work_order_logs_crud import crud_work_order_log, CRUDWorkOrderLog
# Importa os schemas desta sub-fatia
from .work_order_logs_schemas import WorkOrderLogCreate, WorkOrderLogRead

# Importa o serviço da fatia "pai" (WorkOrder) para validação
from ..work_orders_service import work_order_service


class WorkOrderLogService:
    """
    Camada de Serviço (Lógica de Negócio) para os Logs (Comentários)
    da Ordem de Serviço.
    """

    def __init__(self, crud_log: CRUDWorkOrderLog):
        self.crud_log = crud_log

    def get_logs_for_wo(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderLogRead]:
        """
        Obtém todos os logs para uma Ordem de Serviço específica.
        
        Valida se a OS principal existe antes de procurar os logs.
        """
        # 1. Valida se a OS "pai" existe (o service já levanta 404)
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca os logs associados (o crud já otimiza a query)
        return self.crud_log.get_multi_by_work_order(db=db, work_order_id=work_order_id)

    def create_log_for_wo(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        obj_in: WorkOrderLogCreate,
        current_user: Usuario
    ) -> WorkOrderLogRead:
        """
        Cria um novo log (comentário) para uma Ordem de Serviço.
        
        Associa o log ao utilizador logado.
        """
        # 1. Valida se a OS "pai" existe (o service já levanta 404)
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Cria o log (o crud lida com a associação das FKs)
        return self.crud_log.create_log(
            db=db,
            obj_in=obj_in,
            work_order_id=work_order_id,
            created_by_user_id=current_user.id
        )

    def delete_log(
        self,
        db: Session,
        *,
        log_id: uuid.UUID,
        current_user: Usuario # (Reservado para validação de permissão futura)
    ) -> WorkOrderLogRead:
        """
        Elimina um log de atividade (comentário).
        
        (Lógica de Negócio Futura: Permitir que apenas o
        próprio utilizador ou um admin possa eliminar)
        """
        # 1. Busca o log
        db_log = self.crud_log.get(db, id=log_id)
        if not db_log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Log de atividade não encontrado."
            )
            
        # TODO: Adicionar lógica de permissão (ex:)
        # if db_log.created_by_user_id != current_user.id and not current_user.is_superuser:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Não tem permissão para eliminar este comentário."
        #     )
            
        # 2. Remove o log
        # (O CRUDBase fará um HARD DELETE, pois WorkOrderLog não
        # tem 'is_active', o que é o comportamento esperado para logs)
        return self.crud_log.remove(db=db, id=log_id)


# Instância única do serviço
work_order_log_service = WorkOrderLogService(crud_work_order_log)