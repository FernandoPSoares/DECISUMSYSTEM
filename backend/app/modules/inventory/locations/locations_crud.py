# backend/app/modules/inventory/locations/locations_crud.py

from sqlalchemy.orm import Session
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from ....core.crud_base import CRUDBase
from .... import models
from . import locations_schemas

class CRUDTipoLocal(CRUDBase[models.TipoLocal, locations_schemas.TipoLocalCreate, locations_schemas.TipoLocalUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[models.TipoLocal]:
        query = db.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.TipoLocal, is_active: bool) -> models.TipoLocal:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDLocal(CRUDBase[models.Local, locations_schemas.LocalCreate, locations_schemas.LocalUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[models.Local]:
        query = db.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.Local, is_active: bool) -> models.Local:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Cria os objetos de CRUD para serem usados pelo serviço
tipo_local_crud = CRUDTipoLocal(models.TipoLocal)
local_crud = CRUDLocal(models.Local)
