# backend/app/modules/inventory/locations/locations_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from .... import models
from . import locations_crud, locations_schemas

class LocalService:
    # --- Métodos para Tipo de Local ---
    def get_tipo_local_by_id(self, db: Session, tipo_local_id: str) -> models.TipoLocal:
        db_tipo_local = locations_crud.tipo_local_crud.get(db, id=tipo_local_id)
        if not db_tipo_local:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de local não encontrado")
        return db_tipo_local

    def get_all_tipos_local(self, db: Session, skip: int, limit: int, active_only: bool) -> List[models.TipoLocal]:
        return locations_crud.tipo_local_crud.get_multi(db, skip=skip, limit=limit, active_only=active_only)

    def create_tipo_local(self, db: Session, tipo_local_in: locations_schemas.TipoLocalCreate) -> models.TipoLocal:
        db_tipo_local = locations_crud.tipo_local_crud.get(db, id=tipo_local_in.id)
        if db_tipo_local:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tipo de local já registado")
        return locations_crud.tipo_local_crud.create(db=db, obj_in=tipo_local_in)

    def update_tipo_local(self, db: Session, tipo_local_id: str, tipo_local_in: locations_schemas.TipoLocalUpdate) -> models.TipoLocal:
        db_tipo_local = self.get_tipo_local_by_id(db, tipo_local_id)
        return locations_crud.tipo_local_crud.update(db=db, db_obj=db_tipo_local, obj_in=tipo_local_in)

    def update_tipo_local_status(self, db: Session, tipo_local_id: str, is_active: bool) -> models.TipoLocal:
        db_tipo_local = self.get_tipo_local_by_id(db, tipo_local_id)
        return locations_crud.tipo_local_crud.update_status(db, db_obj=db_tipo_local, is_active=is_active)

    # --- Métodos para Local ---
    def get_local_by_id(self, db: Session, local_id: str) -> models.Local:
        db_local = locations_crud.local_crud.get(db, id=local_id)
        if not db_local:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Local não encontrado")
        return db_local

    def get_all_locais(self, db: Session, skip: int, limit: int, active_only: bool) -> List[models.Local]:
        return locations_crud.local_crud.get_multi(db, skip=skip, limit=limit, active_only=active_only)

    def create_local(self, db: Session, local_in: locations_schemas.LocalCreate) -> models.Local:
        db_local = locations_crud.local_crud.get(db, id=local_in.id)
        if db_local:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de local já registado")
        self.get_tipo_local_by_id(db, tipo_local_id=local_in.tipo_local_id)
        return locations_crud.local_crud.create(db=db, obj_in=local_in)

    def update_local(self, db: Session, local_id: str, local_in: locations_schemas.LocalUpdate) -> models.Local:
        db_local = self.get_local_by_id(db, local_id)
        return locations_crud.local_crud.update(db=db, db_obj=db_local, obj_in=local_in)

    def update_local_status(self, db: Session, local_id: str, is_active: bool) -> models.Local:
        db_local = self.get_local_by_id(db, local_id)
        return locations_crud.local_crud.update_status(db, db_obj=db_local, is_active=is_active)

# Cria uma instância do serviço para ser usada pelo resto da aplicação
local_service = LocalService()
