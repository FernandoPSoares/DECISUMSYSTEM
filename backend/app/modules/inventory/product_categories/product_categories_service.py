# backend/app/modules/inventory/product_categories/product_categories_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from .... import models
from . import product_categories_crud, product_categories_schemas

class ProductCategoryService:
    def get_all(self, db: Session, *, skip: int, limit: int, is_active: Optional[bool], search: Optional[str], sort_by: Optional[str], sort_order: str, exclude_id: Optional[str]) -> List[models.CategoriaProduto]:
        return product_categories_crud.categoria_produto_crud.get_multi(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order, exclude_id=exclude_id)

    def create(self, db: Session, *, obj_in: product_categories_schemas.CategoriaProdutoCreate) -> models.CategoriaProduto:
        return product_categories_crud.categoria_produto_crud.create(db, obj_in=obj_in)

    def update(self, db: Session, *, id: str, obj_in: product_categories_schemas.CategoriaProdutoUpdate) -> models.CategoriaProduto:
        db_obj = product_categories_crud.categoria_produto_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria de Produto não encontrada.")
        return product_categories_crud.categoria_produto_crud.update(db, db_obj=db_obj, obj_in=obj_in)

    def update_status(self, db: Session, *, id: str, is_active: bool) -> models.CategoriaProduto:
        db_obj = product_categories_crud.categoria_produto_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria de Produto não encontrada.")
        return product_categories_crud.categoria_produto_crud.update_status(db, db_obj=db_obj, is_active=is_active)

product_category_service = ProductCategoryService()
