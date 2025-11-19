# File: backend/app/modules/maintenance/assets/assets_service.py

import uuid
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.maintenance.asset_model import Asset
from .assets_crud import crud_asset, CRUDAsset
from .assets_schemas import AssetCreate, AssetUpdate

# Importamos os CRUDS de outras fatias para validar as Chaves Estrangeiras (FKs)
from app.modules.inventory.locations.locations_crud import local_crud
from app.modules.maintenance.manufacturers.manufacturers_crud import manufacturer_crud
from app.modules.maintenance.asset_categories.asset_categories_crud import asset_category_crud

class AssetService:
    """
    Camada de Serviço (Lógica de Negócio) para Ativos.
    
    Esta camada aplica validações antes de interagir com
    a camada de acesso a dados (CRUD).
    """
    
    def __init__(self, crud_asset_instance: CRUDAsset):
        self.crud_asset = crud_asset_instance

    def get_asset(self, db: Session, asset_id: uuid.UUID) -> Asset:
        """
        Busca um ativo específico pelo ID.
        
        Levanta 404 se não for encontrado.
        """
        db_asset = self.crud_asset.get(db, id=asset_id)
        if not db_asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ativo não encontrado",
            )
        return db_asset

    def get_assets(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[Asset]:
        """
        Busca uma lista de ativos, aplicando filtros de paginação e busca.
        """
        # O `is_active` foi removido do get_multi do crud_asset, então removemos daqui também.
        return self.crud_asset.get_multi(
            db=db, 
            skip=skip, 
            limit=limit, 
            search=search, 
            sort_by=sort_by, 
            sort_order=sort_order
        )

    def create_asset(self, db: Session, *, obj_in: AssetCreate) -> Asset:
        """
        Cria um novo ativo após validar os dados de entrada.
        """
        # 1. Validação de campos únicos (TAG Interna e Serial)
        db_asset_tag = self.crud_asset.get_by_internal_tag(db, internal_tag=obj_in.internal_tag)
        if db_asset_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um ativo com a TAG Interna '{obj_in.internal_tag}'."
            )
        
        if obj_in.serial_number:
            db_asset_serial = self.crud_asset.get_by_serial_number(db, serial_number=obj_in.serial_number)
            if db_asset_serial:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um ativo com o Número de Série '{obj_in.serial_number}'."
                )
        
        # 2. Validação de Chaves Estrangeiras (FKs)
        self._validate_foreign_keys(db, 
                                    manufacturer_id=obj_in.manufacturer_id,
                                    location_id=obj_in.location_id,
                                    category_id=obj_in.category_id,
                                    parent_asset_id=obj_in.parent_asset_id)
        
        # 3. Criação no banco
        return self.crud_asset.create(db=db, obj_in=obj_in)

    def update_asset(self, db: Session, *, asset_id: uuid.UUID, obj_in: AssetUpdate) -> Asset:
        """
        Atualiza um ativo existente após validar os dados de entrada.
        """
        # 1. Busca o objeto existente
        db_asset = self.get_asset(db, asset_id=asset_id) # (Já trata 404)
        
        update_data = obj_in.model_dump(exclude_unset=True)

        # 2. Validação de campos únicos (se forem alterados)
        if "internal_tag" in update_data:
            db_asset_tag = self.crud_asset.get_by_internal_tag(db, internal_tag=update_data["internal_tag"])
            if db_asset_tag and db_asset_tag.id != asset_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um ativo com a TAG Interna '{update_data['internal_tag']}'."
                )
        
        if "serial_number" in update_data and update_data["serial_number"]:
            db_asset_serial = self.crud_asset.get_by_serial_number(db, serial_number=update_data["serial_number"])
            if db_asset_serial and db_asset_serial.id != asset_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um ativo com o Número de Série '{update_data['serial_number']}'."
                )
        
        # 3. Validação de Chaves Estrangeiras e Hierarquia (se forem alterados)
        self._validate_foreign_keys(db,
                                    manufacturer_id=update_data.get("manufacturer_id"),
                                    location_id=update_data.get("location_id"),
                                    category_id=update_data.get("category_id"),
                                    parent_asset_id=update_data.get("parent_asset_id"),
                                    current_asset_id=asset_id) # Passa o ID atual para evitar auto-referência
        
        # 4. Atualização no banco
        return self.crud_asset.update(db=db, db_obj=db_asset, obj_in=update_data)

    def delete_asset(self, db: Session, *, asset_id: uuid.UUID) -> Asset:
        """
        Remove um ativo.
        """
        db_asset = self.crud_asset.get(db, id=asset_id) 
        
        if not db_asset:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ativo não encontrado",
            )

        # --- LÓGICA DE NEGÓCIO CRÍTICA (Proteção de Exclusão) ---
        
        if db_asset.work_orders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível eliminar o ativo. Ele possui Ordens de Serviço associadas."
            )

        if db_asset.child_assets:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível eliminar o ativo. Ele possui sub-ativos (ativos filhos) associados. Mova os sub-ativos primeiro."
            )
        
        if db_asset.pm_plans:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível eliminar o ativo. Ele está associado a Planos de Manutenção Preventiva."
            )
        
        deleted_asset = self.crud_asset.remove(db=db, id=asset_id)
        if not deleted_asset:
            raise HTTPException(status_code=404, detail="Ativo não encontrado para remoção.")
            
        return deleted_asset

    def _validate_foreign_keys(
        self, 
        db: Session, 
        *,
        manufacturer_id: Optional[uuid.UUID] = None,
        location_id: Optional[str] = None,
        category_id: Optional[uuid.UUID] = None,
        parent_asset_id: Optional[uuid.UUID] = None,
        current_asset_id: Optional[uuid.UUID] = None
    ):
        """
        Método 'helper' privado para validar a existência de chaves 
        estrangeiras (FKs) antes de criar ou atualizar um Ativo.
        """
        
        if manufacturer_id:
            manufacturer = manufacturer_crud.get(db, id=manufacturer_id)
            if not manufacturer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Fabricante com ID {manufacturer_id} não encontrado."
                )
        
        if category_id:
            category = asset_category_crud.get(db, id=category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoria de Ativo com ID {category_id} não encontrada."
                )

        if location_id:
            location = local_crud.get(db, id=location_id)
            if not location:
                 raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Local com ID {location_id} não encontrado."
                )
        
        if parent_asset_id:
            if current_asset_id and parent_asset_id == current_asset_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Um ativo não pode ser pai de si mesmo."
                )
            
            parent = self.crud_asset.get(db, id=parent_asset_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ativo Pai (parent) com ID {parent_asset_id} não encontrado."
                )

# Instância única do serviço para ser usada pelos routers
asset_service = AssetService(crud_asset)