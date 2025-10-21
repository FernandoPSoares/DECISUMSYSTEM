# backend/app/modules/inventory/products/products_crud.py

from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from ....core.crud_base import CRUDBase
from .... import models
from . import products_schemas

class CRUDProduto(CRUDBase[models.Produto, products_schemas.ProdutoCreate, products_schemas.ProdutoUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None, search: Optional[str] = None, sort_by: Optional[str] = None, sort_order: str = "asc") -> List[models.Produto]:
        # Sobrescreve para carregar as relações (eager loading)
        query = db.query(self.model).options(
            joinedload(self.model.udm),
            joinedload(self.model.categoria_produto),
            joinedload(self.model.marca)
        )
        # Filtra por atividade se especificado
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)
        
        # Chama a implementação da CRUDBase, que já lida com pesquisa e ordenação
        # mas passa a query já com os joins
        return super().get_multi(db, query=query, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order)

    def update_status(self, db: Session, *, db_obj: models.Produto, is_active: bool) -> models.Produto:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

produto_crud = CRUDProduto(models.Produto)

