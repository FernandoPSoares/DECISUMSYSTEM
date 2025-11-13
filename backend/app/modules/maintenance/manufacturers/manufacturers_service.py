# File: backend/app/modules/maintenance/manufacturers/manufacturers_service.py

import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

# Importa o CRUD (Operário) e os Schemas (Contratos)
from .manufacturers_crud import manufacturer_crud
from .manufacturers_schemas import ManufacturerCreate, ManufacturerUpdate

# Importa o Modelo (para type hinting e lógica de reativação)
from app.models.maintenance.manufacturer_model import Manufacturer


class ManufacturerService:
    """
    Serviço para a lógica de negócio dos Fabricantes (Manufacturers).
    Orquestra as operações de CRUD e aplica as regras de negócio
    alinhadas com o "Pacto do Soft Delete".
    """

    def get_manufacturer_by_id(self, db: Session, manufacturer_id: uuid.UUID) -> Manufacturer:
        """
        Obtém um único fabricante pelo seu ID.
        Lança HTTPException 404 se não for encontrado ou se estiver inativo.
        """
        manufacturer = manufacturer_crud.get(db, id=manufacturer_id)
        
        # Regra de Negócio: Por defeito, 'get_by_id' não deve
        # encontrar registos inativos (apagados).
        if not manufacturer or not manufacturer.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fabricante com o ID {manufacturer_id} não encontrado.",
            )
        return manufacturer

    def get_all_manufacturers(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Manufacturer]:
        """
        Obtém uma lista paginada de todos os fabricantes ATIVOS.
        A lógica de 'is_active=True' já é tratada por defeito
        pela nossa CRUDBase "inteligente".
        """
        return manufacturer_crud.get_multi(db, skip=skip, limit=limit)

    def create_manufacturer(self, db: Session, *, manufacturer_in: ManufacturerCreate) -> Manufacturer:
        """
        Cria um novo fabricante.
        
        Regra de Negócio:
        1. Se o nome já existir e estiver ATIVO, lança um erro 400.
        2. Se o nome já existir e estiver INATIVO, reativa-o e atualiza-o.
        3. Se não existir, cria um novo.
        """
        # Verifica se o nome já existe (get_by_name procura em ATIVOS e INATIVOS)
        existing_manufacturer = manufacturer_crud.get_by_name(db, name=manufacturer_in.name)
        
        if existing_manufacturer:
            if existing_manufacturer.is_active:
                # Regra 1: Conflito de nome ativo
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Um fabricante com o nome '{manufacturer_in.name}' já existe.",
                )
            else:
                # Regra 2: Reativar um fabricante inativo
                update_data = manufacturer_in.model_dump(exclude_unset=True)
                update_data['is_active'] = True # Reativa o fabricante
                return manufacturer_crud.update(db, db_obj=existing_manufacturer, obj_in=update_data)
        
        # Regra 3: Criar novo
        return manufacturer_crud.create(db, obj_in=manufacturer_in)

    def update_manufacturer(
        self, db: Session, *, manufacturer_id: uuid.UUID, manufacturer_in: ManufacturerUpdate
    ) -> Manufacturer:
        """
        Atualiza um fabricante.
        
        Regra de Negócio:
        1. Garante que o fabricante que está a ser atualizado está ativo.
        2. Se o nome for alterado, verifica se o novo nome já está em uso
           por OUTRO fabricante (ativo ou inativo).
        """
        # Regra 1: Garante que o fabricante existe e está ativo
        manufacturer_db = self.get_manufacturer_by_id(db, manufacturer_id=manufacturer_id)
        
        # Regra 2: Verifica conflito de nome na atualização
        if manufacturer_in.name and manufacturer_in.name != manufacturer_db.name:
            existing = manufacturer_crud.get_by_name(db, name=manufacturer_in.name)
            if existing and existing.id != manufacturer_db.id:
                # O nome já está em uso por OUTRO fabricante
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"O nome '{manufacturer_in.name}' já está em uso por outro fabricante.",
                )
        
        # Se todas as regras passarem, atualiza
        return manufacturer_crud.update(db, db_obj=manufacturer_db, obj_in=manufacturer_in)

    def delete_manufacturer(self, db: Session, *, manufacturer_id: uuid.UUID) -> Manufacturer:
        """
        Desativa (soft delete) um fabricante.
        
        Garante que o fabricante existe e está ativo antes de o desativar.
        """
        # 1. Garante que o fabricante existe e está ativo
        manufacturer_to_delete = self.get_manufacturer_by_id(db, manufacturer_id=manufacturer_id)
        
        # (Regra Futura: Não permitir desativar se o fabricante estiver
        # ligado a Ativos que não estão desativados (DECOMMISSIONED))
        
        # 2. Chama o 'remove' inteligente da CRUDBase, que fará o SOFT DELETE
        # (definindo is_active = False)
        return manufacturer_crud.remove(db, id=manufacturer_id)

# Cria uma instância única (singleton) do serviço
manufacturer_service = ManufacturerService()