# File: backend/app/modules/maintenance/work_orders/work_orders_crud.py

import uuid
from datetime import datetime
from typing import Optional, Any, List
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, func, desc, inspect, String, Text, or_

from app.core.crud_base import CRUDBase
from app.models.maintenance.work_order_model import WorkOrder
from app.models.administration.user_model import Usuario
from app.models.maintenance.asset_model import Asset # Necessário para a busca
from .work_orders_schemas import WorkOrderCreate, WorkOrderUpdate

class CRUDWorkOrder(CRUDBase[WorkOrder, WorkOrderCreate, WorkOrderUpdate]):
    """Classe CRUD específica para o modelo WorkOrder."""

    def get(self, db: Session, id: Any) -> Optional[WorkOrder]:
        """
        Obtém uma única Ordem de Serviço pelo ID, otimizando o
        carregamento de *todos* os relacionamentos (Eager Loading)
        para a vista de detalhe.
        """
        statement = select(self.model).where(self.model.id == id).options(
            joinedload(self.model.asset),
            joinedload(self.model.created_by_user),
            joinedload(self.model.assigned_to_technician),
            joinedload(self.model.assigned_to_team),
            joinedload(self.model.pm_plan),
            # Usar selectinload para listas (evita N+1 queries)
            selectinload(self.model.tasks),
            selectinload(self.model.labor_logs),
            selectinload(self.model.parts_used),
            selectinload(self.model.activity_logs),
            # (Futuras relações de Análise de Falha entrariam aqui)
        )
        return db.scalars(statement).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None, # O modelo WorkOrder não usa soft-delete
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[WorkOrder]:
        """
        Obtém uma lista de Ordens de Serviço, com otimização (Eager Loading)
        para as relações mais comuns da listagem e busca personalizada.
        
        Sobrescreve o get_multi base para adicionar otimizações.
        """
        
        # Inicia a query otimizada (apenas relações da listagem)
        query = db.query(self.model).options(
            joinedload(self.model.asset),
            joinedload(self.model.assigned_to_technician),
            joinedload(self.model.assigned_to_team),
        )
        
        # Lógica de Pesquisa (Customizada para WorkOrder)
        if search:
            # Garante o JOIN em Asset para a busca
            query = query.join(WorkOrder.asset, isouter=True) 
            
            search_filters = [
                self.model.wo_number.ilike(f"%{search}%"),
                self.model.title.ilike(f"%{search}%"),
                Asset.name.ilike(f"%{search}%"), # Busca no nome do Ativo
                Asset.internal_tag.ilike(f"%{search}%") # Busca na TAG do Ativo
            ]
            query = query.filter(or_(*search_filters))
                
        # Lógica de Ordenação (copiada do CRUDBase)
        if sort_by:
            sort_column = None
            if '.' in sort_by:
                try:
                    relation_name, column_name = sort_by.split('.')
                    relation_attr = getattr(self.model, relation_name)
                    # Otimização: Não faz join se já fizemos (ex: 'asset')
                    if relation_name != 'asset':
                        query = query.join(relation_attr, isouter=True) 
                        
                    related_model = relation_attr.property.mapper.class_
                    sort_column = getattr(related_model, column_name)
                except Exception:
                    sort_column = None
            else:
                if hasattr(self.model, sort_by):
                    sort_column = getattr(self.model, sort_by)

            if sort_column is not None:
                order_expression = sort_column
                if isinstance(sort_column.type, (String, Text)):
                    order_expression = func.lower(sort_column)
                
                if sort_order.lower() == "desc":
                    query = query.order_by(desc(order_expression))
                else:
                    query = query.order_by(asc(order_expression))
        else:
            # Padrão: ordenar pela OS mais recente
             query = query.order_by(desc(self.model.created_at))

        return query.offset(skip).limit(limit).all()


    def _get_next_wo_number(self, db: Session) -> str:
        """
        Gera o próximo número sequencial da Ordem de Serviço (wo_number)
        no formato OS-YYYY-NNNN.
        """
        current_year = datetime.now().year
        prefix = f"OS-{current_year}-"

        # 1. Encontra o último número de OS *deste ano*
        stmt = select(self.model.wo_number)\
            .where(self.model.wo_number.like(f"{prefix}%"))\
            .order_by(desc(self.model.wo_number))\
            .limit(1)
        
        last_wo_number_str = db.scalars(stmt).first()

        next_seq = 1
        if last_wo_number_str:
            try:
                # Extrai a parte numérica (ex: "0001" de "OS-2025-0001")
                last_seq_str = last_wo_number_str.split('-')[-1]
                last_seq = int(last_seq_str)
                next_seq = last_seq + 1
            except (ValueError, IndexError, TypeError):
                # Se o formato falhar, começa do 1 (ou loga um erro)
                next_seq = 1

        # 3. Formata o novo número com 4 dígitos (ex: 0001)
        return f"{prefix}{next_seq:04d}"

    def create(
        self, 
        db: Session, 
        *, 
        obj_in: WorkOrderCreate, 
        created_by_user_id: uuid.UUID
    ) -> WorkOrder:
        """
        Cria uma nova Ordem de Serviço, substituindo o
        método 'create' base para:
        1. Gerar o 'wo_number' sequencial.
        2. Adicionar o 'created_by_user_id' do utilizador logado.
        """
        
        # 1. Gera o próximo número de OS
        next_wo_number = self._get_next_wo_number(db)
        
        # 2. Prepara os dados do objeto
        obj_in_data = obj_in.model_dump()
        
        # 3. Adiciona os campos gerados
        db_obj = self.model(
            **obj_in_data,
            wo_number=next_wo_number,
            created_by_user_id=created_by_user_id
        )
        
        # 4. Salva no banco
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Instância única da classe CRUD para ser usada nos services e routers
crud_work_order = CRUDWorkOrder(WorkOrder)