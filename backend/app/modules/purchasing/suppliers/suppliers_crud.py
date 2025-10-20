# backend/app/modules/purchasing/suppliers/suppliers_crud.py

from sqlalchemy.orm import Session
from typing import List

# --- IMPORTAÇÕES CORRIGIDAS ---
# Subimos 3 níveis para chegar a 'app/' e depois descemos para 'core'.
from ....core.crud_base import CRUDBase
from .... import models
from . import suppliers_schemas

class CRUDFornecedor(CRUDBase[models.Fornecedor, suppliers_schemas.FornecedorCreate, suppliers_schemas.FornecedorUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[models.Fornecedor]:
        """Sobrescreve o método get_multi para filtrar por fornecedores ativos."""
        query = db.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.Fornecedor, is_active: bool) -> models.Fornecedor:
        """Método específico para ativar ou desativar um fornecedor."""
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

fornecedor_crud = CRUDFornecedor(models.Fornecedor)
