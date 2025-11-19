# File: backend/app/modules/maintenance/work_orders/parts/work_order_parts_service.py

import uuid
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.maintenance.work_order_parts_model import WorkOrderPartUsage
from app.models.administration.user_model import Usuario

# Importa o CRUD e Schemas desta sub-fatia
from .work_order_parts_crud import crud_work_order_part_usage, CRUDWorkOrderPartUsage
from .work_order_parts_schemas import (
    WorkOrderPartUsageCreate, 
    WorkOrderPartUsageUpdate, 
    WorkOrderPartUsageRead
)

# Importa o serviço "pai" (WorkOrder) para validação
from ..work_orders_service import work_order_service

# --- VALIDAÇÃO INTER-MODULAR ---
# --- CORREÇÃO DE IMPORTAÇÃO ---
# O nome da instância no módulo de inventário é 'produto_crud'
from app.modules.inventory.products.products_crud import produto_crud
# --- FIM DA CORREÇÃO ---


class WorkOrderPartUsageService:
    """
    Camada de Serviço (Lógica de Negócio) para o Consumo de Peças
    da Ordem de Serviço.
    """

    def __init__(self, crud_part_usage: CRUDWorkOrderPartUsage):
        self.crud_part_usage = crud_part_usage

    def _get_part_usage_or_404(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID, 
        part_usage_id: uuid.UUID
    ) -> WorkOrderPartUsage:
        """
        Helper privado: Obtém um consumo de peça específico, garantindo que
        a OS pai existe e que o consumo pertence a ela.
        """
        # 1. Valida se a OS "pai" existe (o service já levanta 404)
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca o consumo (o crud valida a relação)
        db_part = self.crud_part_usage.get_by_id_and_wo_id(
            db=db, 
            part_usage_id=part_usage_id, 
            work_order_id=work_order_id
        )
        
        if not db_part:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registo de consumo de peça não encontrado nesta Ordem de Serviço."
            )
        return db_part

    def _validate_foreign_keys(
        self, 
        db: Session, 
        *, 
        product_id: uuid.UUID
    ):
        """Helper privado para validar o Produto (Peça)."""
        if product_id:
            # --- CORREÇÃO DE USO ---
            product = produto_crud.get(db, id=product_id)
            # --- FIM DA CORREÇÃO ---
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto (Peça) com ID {product_id} não encontrado no inventário."
                )
            if not product.is_active: # Respeita o soft-delete do produto
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Não é possível consumir o Produto '{product.name}', pois ele está inativo."
                )

    def get_parts_for_wo(
        self, 
        db: Session, 
        *, 
        work_order_id: uuid.UUID
    ) -> List[WorkOrderPartUsageRead]:
        """
        Obtém todos os consumos de peças para uma OS específica.
        """
        # 1. Valida se a OS "pai" existe
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Busca os consumos (o crud já os ordena e otimiza)
        return self.crud_part_usage.get_multi_by_work_order(
            db=db, 
            work_order_id=work_order_id
        )

    def create_part_usage_for_wo(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        obj_in: WorkOrderPartUsageCreate,
        current_user: Usuario
    ) -> WorkOrderPartUsageRead:
        """
        Cria um novo registo de consumo de peça para uma OS.
        O 'created_by_user_id' é preenchido automaticamente.
        """
        # 1. Valida se a OS "pai" existe
        work_order_service.get_work_order(db, wo_id=work_order_id)
        
        # 2. Valida o Produto (Peça)
        self._validate_foreign_keys(db, product_id=obj_in.product_id)
        
        # 3. Cria o registo de consumo
        return self.crud_part_usage.create_part_usage(
            db=db,
            obj_in=obj_in,
            work_order_id=work_order_id,
            created_by_user_id=current_user.id
        )

    def update_part_usage(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        part_usage_id: uuid.UUID,
        obj_in: WorkOrderPartUsageUpdate
    ) -> WorkOrderPartUsageRead:
        """
        Atualiza um consumo de peça (normalmente a quantidade).
        """
        # 1. Obtém o consumo (helper já valida a OS pai e o consumo)
        db_part = self._get_part_usage_or_404(
            db, 
            work_order_id=work_order_id, 
            part_usage_id=part_usage_id
        )
        
        # 2. Converte o schema de update para dict
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # 3. Aplica a atualização
        return self.crud_part_usage.update(
            db=db, 
            db_obj=db_part, 
            obj_in=update_data
        )

    def delete_part_usage(
        self,
        db: Session,
        *,
        work_order_id: uuid.UUID,
        part_usage_id: uuid.UUID
    ) -> WorkOrderPartUsageRead:
        """
        Elimina (Hard Delete) um registo de consumo de peça.
        """
        # 1. Obtém o consumo (helper já valida a OS pai e o consumo)
        db_part = self._get_part_usage_or_404(
            db, 
            work_order_id=work_order_id, 
            part_usage_id=part_usage_id
        )
        
        # 2. Remove o registo
        return self.crud_part_usage.remove(db=db, id=db_part.id)

# Instância única do serviço
# --- CORREÇÃO DE NOME DE INSTÂNCIA ---
# (O nome da classe CRUD é CRUDWorkOrderPartUsage)
work_order_part_usage_service = WorkOrderPartUsageService(crud_work_order_part_usage)
# --- FIM DA CORREÇÃO ---