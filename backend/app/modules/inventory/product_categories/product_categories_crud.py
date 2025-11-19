# backend/app/modules/inventory/product_categories/product_categories_crud.py

from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, asc, desc
from typing import List, Optional

from ....core.crud_base import CRUDBase
from .... import models
from . import product_categories_schemas

class CRUDCategoriaProduto(CRUDBase[models.CategoriaProduto, product_categories_schemas.CategoriaProdutoCreate, product_categories_schemas.CategoriaProdutoUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        exclude_id: Optional[str] = None
    ) -> List[models.CategoriaProduto]:
        query = db.query(self.model)

        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)
        
        if search:
            query = query.filter(self.model.nome.ilike(f"%{search}%"))
        
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)

        if sort_by == 'categoria_pai.nome':
            ParentCategory = aliased(models.CategoriaProduto)
            query = query.outerjoin(ParentCategory, self.model.categoria_pai_id == ParentCategory.id)
            order_expression = func.lower(ParentCategory.nome)
            
            if sort_order.lower() == "desc":
                query = query.order_by(desc(order_expression))
            else:
                query = query.order_by(asc(order_expression))
        else:
            # Reutiliza a lógica de ordenação da CRUDBase para outras colunas
            return super().get_multi(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order)

        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.CategoriaProduto, is_active: bool) -> models.CategoriaProduto:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

categoria_produto_crud = CRUDCategoriaProduto(models.CategoriaProduto)
