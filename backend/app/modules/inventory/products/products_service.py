# backend/app/modules/inventory/products/products_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
import uuid

from .... import models
from . import products_crud, products_schemas

# Importa os cruds necessários para validação
from ..udms import udms_crud
from ..product_categories import product_categories_crud
from ..brands import brands_crud

class ProductService:
    def get_by_id(self, db: Session, produto_id: uuid.UUID) -> models.Produto:
        db_produto = products_crud.produto_crud.get(db, id=produto_id)
        if not db_produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return db_produto
    
    def get_all(self, db: Session, *, skip: int, limit: int, is_active: Optional[bool], search: Optional[str], sort_by: Optional[str], sort_order: str) -> List[models.Produto]:
        return products_crud.produto_crud.get_multi(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order)

    def create(self, db: Session, *, obj_in: products_schemas.ProdutoCreate) -> models.Produto:
        # Validações de chaves estrangeiras
        if not udms_crud.udm_crud.get(db, id=obj_in.udm_id):
            raise HTTPException(status_code=400, detail=f"UDM com id '{obj_in.udm_id}' não encontrada.")
        if not product_categories_crud.categoria_produto_crud.get(db, id=obj_in.categoria_produto_id):
            raise HTTPException(status_code=400, detail=f"Categoria de Produto com id '{obj_in.categoria_produto_id}' não encontrada.")
        if obj_in.marca_id and not brands_crud.marca_crud.get(db, id=obj_in.marca_id):
            raise HTTPException(status_code=400, detail=f"Marca com id '{obj_in.marca_id}' não encontrada.")
            
        return products_crud.produto_crud.create(db, obj_in=obj_in)

    def update(self, db: Session, *, produto_id: uuid.UUID, obj_in: products_schemas.ProdutoUpdate) -> models.Produto:
        db_produto = self.get_by_id(db, produto_id)
        # Validações de chaves estrangeiras, se forem alteradas
        if obj_in.udm_id and not udms_crud.udm_crud.get(db, id=obj_in.udm_id):
            raise HTTPException(status_code=400, detail=f"UDM com id '{obj_in.udm_id}' não encontrada.")
        if obj_in.categoria_produto_id and not product_categories_crud.categoria_produto_crud.get(db, id=obj_in.categoria_produto_id):
            raise HTTPException(status_code=400, detail=f"Categoria de Produto com id '{obj_in.categoria_produto_id}' não encontrada.")
        if obj_in.marca_id and not brands_crud.marca_crud.get(db, id=obj_in.marca_id):
            raise HTTPException(status_code=400, detail=f"Marca com id '{obj_in.marca_id}' não encontrada.")

        return products_crud.produto_crud.update(db, db_obj=db_produto, obj_in=obj_in)

    def update_status(self, db: Session, *, produto_id: uuid.UUID, is_active: bool) -> models.Produto:
        db_produto = self.get_by_id(db, produto_id)
        return products_crud.produto_crud.update_status(db, db_obj=db_produto, is_active=is_active)

product_service = ProductService()

