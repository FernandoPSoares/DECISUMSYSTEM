# File: backend/app/modules/maintenance/work_orders/work_orders_service.py

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.maintenance.work_order_model import WorkOrder, WorkOrderStatus
from app.models.maintenance.asset_model import AssetStatus
from app.models.administration.user_model import Usuario
from .work_orders_crud import crud_work_order, CRUDWorkOrder
from .work_orders_schemas import WorkOrderCreate, WorkOrderUpdate

# Importamos os CRUDS de outras fatias para validar as Chaves Estrangeiras (FKs)
from app.modules.maintenance.assets.assets_crud import crud_asset
# --- CORREÇÃO DE IMPORTAÇÃO ---
from app.modules.maintenance.technicians.technicians_crud import technician_crud
from app.modules.maintenance.teams.teams_crud import maintenance_team_crud
# --- FIM DA CORREÇÃO ---


class WorkOrderService:
    """
    Camada de Serviço (Lógica de Negócio) para Ordens de Serviço (OS).
    """

    def __init__(self, crud_wo: CRUDWorkOrder):
        self.crud_work_order = crud_wo

    def get_work_order(self, db: Session, wo_id: uuid.UUID) -> WorkOrder:
        """
        Busca uma OS específica pelo ID.
        Usa o método 'get' otimizado do CRUD que carrega as relações.
        
        Levanta 404 se não for encontrada.
        """
        db_wo = self.crud_work_order.get(db, id=wo_id)
        if not db_wo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ordem de Serviço não encontrada",
            )
        return db_wo

    def get_work_orders(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[WorkOrder]:
        """
        Busca uma lista de Ordens de Serviço, aplicando filtros.
        Usa o método 'get_multi' otimizado do CRUD.
        """
        return self.crud_work_order.get_multi(
            db=db,
            skip=skip,
            limit=limit,
            is_active=None, # Ignora o filtro de soft-delete
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )

    def create_work_order(
        self, 
        db: Session, 
        *, 
        obj_in: WorkOrderCreate, 
        current_user: Usuario
    ) -> WorkOrder:
        """
        Cria uma nova Ordem de Serviço após validar as FKs.
        """
        # 1. Validação de Chaves Estrangeiras (Ativo, Técnico, Equipa)
        self._validate_foreign_keys(
            db,
            asset_id=obj_in.asset_id,
            technician_id=obj_in.assigned_to_technician_id,
            team_id=obj_in.assigned_to_team_id
        )

        # 2. Criação no banco (o CRUD lida com a geração do wo_number)
        return self.crud_work_order.create(
            db=db, 
            obj_in=obj_in, 
            created_by_user_id=current_user.id
        )

    def update_work_order(
        self, 
        db: Session, 
        *, 
        wo_id: uuid.UUID, 
        obj_in: WorkOrderUpdate
    ) -> WorkOrder:
        """
        Atualiza uma Ordem de Serviço existente.
        """
        # 1. Busca o objeto existente (já trata 404)
        db_wo = self.get_work_order(db, wo_id=wo_id)
        
        update_data = obj_in.model_dump(exclude_unset=True)

        # 2. Validação de Chaves Estrangeiras (se forem alteradas)
        self._validate_foreign_keys(
            db,
            asset_id=update_data.get("asset_id"),
            technician_id=update_data.get("assigned_to_technician_id"),
            team_id=update_data.get("assigned_to_team_id")
        )
        
        # 3. Lógica de Negócio: Atualização de Status
        if "status" in update_data:
            new_status = update_data["status"]
            
            if new_status == WorkOrderStatus.COMPLETED and not db_wo.completed_at:
                update_data["completed_at"] = datetime.now()
            
            elif new_status != WorkOrderStatus.COMPLETED and db_wo.completed_at:
                update_data["completed_at"] = None

        # 4. Atualização no banco
        return self.crud_work_order.update(db=db, db_obj=db_wo, obj_in=update_data)

    def delete_work_order(self, db: Session, *, wo_id: uuid.UUID) -> WorkOrder:
        """
        Remove uma Ordem de Serviço (Hard Delete).
        """
        db_wo = self.get_work_order(db, wo_id=wo_id) 

        if db_wo.status != WorkOrderStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Ordens de Serviço com status '{db_wo.status.value}' não podem ser eliminadas. "
                    "Para remover, por favor, altere o status para 'CANCELLED'."
                )
            )
        
        deleted_wo = self.crud_work_order.remove(db=db, id=wo_id)
        
        if not deleted_wo:
             raise HTTPException(status_code=404, detail="Erro ao remover a OS.")
             
        return deleted_wo 

    def _validate_foreign_keys(
        self,
        db: Session,
        *,
        asset_id: Optional[uuid.UUID] = None,
        technician_id: Optional[uuid.UUID] = None,
        team_id: Optional[uuid.UUID] = None
    ):
        """
        Método 'helper' privado para validar a existência e o status
        das chaves estrangeiras de uma OS.
        """
        
        if asset_id:
            asset = crud_asset.get(db, id=asset_id)
            if not asset:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ativo com ID {asset_id} não encontrado."
                )
            if asset.status == AssetStatus.DECOMMISSIONED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Não é possível criar OS para o Ativo '{asset.name}', pois ele está desativado (DECOMMISSIONED)."
                )

        if technician_id:
            # --- CORREÇÃO DE USO ---
            technician = technician_crud.get(db, id=technician_id)
            # --- FIM DA CORREÇÃO ---
            if not technician:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Técnico com ID {technician_id} não encontrado."
                )
            # (O 'get' do technician_crud já filtra por is_active=True)

        if team_id:
            # --- CORREÇÃO DE USO ---
            team = maintenance_team_crud.get(db, id=team_id)
            # --- FIM DA CORREÇÃO ---
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipa com ID {team_id} não encontrada."
                )
            # (O 'get' do maintenance_team_crud já filtra por is_active=True,
            #  embora o CRUDBase já faça isso, é uma boa prática)

# Instância única do serviço para ser usada pelos routers
work_order_service = WorkOrderService(crud_work_order)