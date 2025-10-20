# backend/app/modules/purchasing/suppliers/suppliers_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
from .... import models
from . import suppliers_crud, suppliers_schemas

class FornecedorService:
    def get_by_id(self, db: Session, fornecedor_id: str) -> models.Fornecedor:
        """Obtém um fornecedor pelo ID, tratando o caso de não encontrar."""
        db_fornecedor = suppliers_crud.fornecedor_crud.get(db, id=fornecedor_id)
        if not db_fornecedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado")
        return db_fornecedor

    def get_all(self, db: Session, skip: int, limit: int, active_only: bool) -> List[models.Fornecedor]:
        """Obtém todos os fornecedores."""
        return suppliers_crud.fornecedor_crud.get_multi(db, skip=skip, limit=limit, active_only=active_only)

    def create(self, db: Session, fornecedor_in: suppliers_schemas.FornecedorCreate) -> models.Fornecedor:
        """Cria um novo fornecedor."""
        db_fornecedor_by_id = suppliers_crud.fornecedor_crud.get(db, id=fornecedor_in.id)
        if db_fornecedor_by_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de fornecedor já registado")
        return suppliers_crud.fornecedor_crud.create(db=db, obj_in=fornecedor_in)

    def update(self, db: Session, fornecedor_id: str, fornecedor_in: suppliers_schemas.FornecedorUpdate) -> models.Fornecedor:
        """Atualiza um fornecedor."""
        db_fornecedor = self.get_by_id(db, fornecedor_id)
        return suppliers_crud.fornecedor_crud.update(db=db, db_obj=db_fornecedor, obj_in=fornecedor_in)

    def update_status(self, db: Session, fornecedor_id: str, is_active: bool) -> models.Fornecedor:
        """Ativa ou desativa um fornecedor."""
        db_fornecedor = self.get_by_id(db, fornecedor_id)
        return suppliers_crud.fornecedor_crud.update_status(db, db_obj=db_fornecedor, is_active=is_active)

fornecedor_service = FornecedorService()
