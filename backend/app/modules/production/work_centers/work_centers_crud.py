# backend/app/modules/production/work_centers/work_centers_crud.py

from sqlalchemy.orm import Session
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from ....core.crud_base import CRUDBase
from .... import models
from . import work_centers_schemas

class CRUDCentroTrabalho(CRUDBase[models.CentroTrabalho, work_centers_schemas.CentroTrabalhoCreate, work_centers_schemas.CentroTrabalhoUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[models.CentroTrabalho]:
        """Sobrescreve o método get_multi para filtrar por centros de trabalho ativos."""
        query = db.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.CentroTrabalho, is_active: bool) -> models.CentroTrabalho:
        """Método específico para ativar ou desativar um centro de trabalho."""
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

centro_trabalho_crud = CRUDCentroTrabalho(models.CentroTrabalho)
