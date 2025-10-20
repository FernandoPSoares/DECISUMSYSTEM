# backend/app/modules/production/work_centers/work_centers_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from .... import models
from . import work_centers_crud, work_centers_schemas

class CentroTrabalhoService:
    def get_by_id(self, db: Session, centro_trabalho_id: str) -> models.CentroTrabalho:
        """Obtém um centro de trabalho pelo ID, tratando o caso de não encontrar."""
        db_centro = work_centers_crud.centro_trabalho_crud.get(db, id=centro_trabalho_id)
        if not db_centro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de trabalho não encontrado")
        return db_centro

    def get_all(self, db: Session, skip: int, limit: int, active_only: bool) -> List[models.CentroTrabalho]:
        """Obtém todos os centros de trabalho."""
        return work_centers_crud.centro_trabalho_crud.get_multi(db, skip=skip, limit=limit, active_only=active_only)

    def create(self, db: Session, centro_trabalho_in: work_centers_schemas.CentroTrabalhoCreate) -> models.CentroTrabalho:
        """Cria um novo centro de trabalho."""
        db_centro_by_id = work_centers_crud.centro_trabalho_crud.get(db, id=centro_trabalho_in.id)
        if db_centro_by_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de centro de trabalho já registado")
        return work_centers_crud.centro_trabalho_crud.create(db=db, obj_in=centro_trabalho_in)

    def update(self, db: Session, centro_trabalho_id: str, centro_trabalho_in: work_centers_schemas.CentroTrabalhoUpdate) -> models.CentroTrabalho:
        """Atualiza um centro de trabalho."""
        db_centro = self.get_by_id(db, centro_trabalho_id)
        return work_centers_crud.centro_trabalho_crud.update(db=db, db_obj=db_centro, obj_in=centro_trabalho_in)

    def update_status(self, db: Session, centro_trabalho_id: str, is_active: bool) -> models.CentroTrabalho:
        """Ativa ou desativa um centro de trabalho."""
        db_centro = self.get_by_id(db, centro_trabalho_id)
        return work_centers_crud.centro_trabalho_crud.update_status(db, db_obj=db_centro, is_active=is_active)

centro_trabalho_service = CentroTrabalhoService()
