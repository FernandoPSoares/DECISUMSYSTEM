# backend/app/modules/inventory/products/products_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from .... import models
from . import products_crud, products_schemas

class ProductStructureService:
    # --- GET ALL CATEGORIAS UDM ---
    def get_all_categorias_udm(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[models.CategoriaUdm]:
        kwargs = {"skip": skip, "limit": limit, "is_active": is_active, "search": search, "sort_by": sort_by, "sort_order": sort_order}
        return products_crud.categoria_udm_crud.get_multi(db, **kwargs)

    # --- CREATE CATEGORIA UDM ---
    def create_categoria_udm(self, db: Session, *, categoria_in: products_schemas.CategoriaUdmCreate) -> models.CategoriaUdm:
        if products_crud.categoria_udm_crud.get(db, id=categoria_in.id):
            raise HTTPException(status_code=400, detail=f"Categoria UDM com ID '{categoria_in.id}' já existe.")
        if products_crud.udm_crud.get(db, id=categoria_in.unidade_referencia_id):
            raise HTTPException(status_code=400, detail=f"UDM com ID '{categoria_in.unidade_referencia_id}' já existe.")
        try:
            db_categoria = models.CategoriaUdm(id=categoria_in.id, nome=categoria_in.nome)
            db.add(db_categoria)
            db.flush()
            db_udm_ref = models.Udm(id=categoria_in.unidade_referencia_id, nome=categoria_in.unidade_referencia_nome, proporcao_combinada=1.0, categoria_udm_id=db_categoria.id)
            db.add(db_udm_ref)
            db_categoria.unidade_referencia_id = db_udm_ref.id
            db.commit()
            db.refresh(db_categoria)
            return db_categoria
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado: {str(e)}")

    # --- UPDATE CATEGORIA UDM ---
    def update_categoria_udm(self, db: Session, *, id: str, obj_in: products_schemas.CategoriaUdmUpdate) -> models.CategoriaUdm:
        db_obj = products_crud.categoria_udm_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Categoria UDM não encontrada.")
        return products_crud.categoria_udm_crud.update(db, db_obj=db_obj, obj_in=obj_in)

    # --- CHANGE REFERENCE UDM ---
    def change_reference_udm(self, db: Session, *, category_id: str, new_ref_udm_id: str) -> models.CategoriaUdm:
        db_category = products_crud.categoria_udm_crud.get(db, id=category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Categoria UDM não encontrada.")
        new_ref_udm = products_crud.udm_crud.get(db, id=new_ref_udm_id)
        if not new_ref_udm or new_ref_udm.categoria_udm_id != category_id:
            raise HTTPException(status_code=400, detail="A nova UDM de referência não existe ou não pertence a esta categoria.")
        if not new_ref_udm.is_active:
            raise HTTPException(status_code=400, detail="A nova UDM de referência deve estar ativa.")
        if db_category.unidade_referencia_id == new_ref_udm_id:
            raise HTTPException(status_code=400, detail="Esta UDM já é a referência.")
        try:
            conversion_factor = new_ref_udm.proporcao_combinada
            for udm in db_category.udms:
                udm.proporcao_combinada = udm.proporcao_combinada / conversion_factor
            new_ref_udm.proporcao_combinada = 1.0
            db_category.unidade_referencia_id = new_ref_udm_id
            db.commit()
            db.refresh(db_category)
            return db_category
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao recalcular proporções: {str(e)}")

    # --- UPDATE CATEGORIA UDM STATUS ---
    def update_categoria_udm_status(self, db: Session, *, id: str, is_active: bool) -> models.CategoriaUdm:
        db_obj = products_crud.categoria_udm_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Categoria UDM não encontrada.")
        return products_crud.categoria_udm_crud.update_status(db, db_obj=db_obj, is_active=is_active)

    # --- GET ALL UDM ---
    def get_all_udm(self, db: Session, *, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None, search: Optional[str] = None, sort_by: Optional[str] = None, sort_order: str = "asc") -> List[models.Udm]:
        return products_crud.udm_crud.get_multi(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order)

    # --- CREATE UDM ---
    def create_udm(self, db: Session, *, udm_in: products_schemas.UdmCreate) -> models.Udm:
        if not products_crud.categoria_udm_crud.get(db, id=udm_in.categoria_udm_id):
            raise HTTPException(status_code=400, detail="Categoria UDM não encontrada.")
        if products_crud.udm_crud.get(db, id=udm_in.id):
             raise HTTPException(status_code=400, detail=f"UDM com ID '{udm_in.id}' já existe.")
        return products_crud.udm_crud.create(db, obj_in=udm_in)

    # --- UPDATE UDM ---
    def update_udm(self, db: Session, *, id: str, obj_in: products_schemas.UdmUpdate) -> models.Udm:
        db_udm = products_crud.udm_crud.get(db, id=id)
        if not db_udm:
            raise HTTPException(status_code=404, detail="UDM não encontrada.")

        is_changing_category = obj_in.categoria_udm_id and obj_in.categoria_udm_id != db_udm.categoria_udm_id
        
        if is_changing_category:
            if db_udm.categoria_udm and db_udm.categoria_udm.unidade_referencia_id == id:
                raise HTTPException(status_code=400, detail="Não é possível alterar a categoria de uma UDM de referência.")
            
            new_category = products_crud.categoria_udm_crud.get(db, id=obj_in.categoria_udm_id)
            if not new_category:
                raise HTTPException(status_code=404, detail=f"A nova categoria com ID '{obj_in.categoria_udm_id}' não foi encontrada.")

        return products_crud.udm_crud.update(db, db_obj=db_udm, obj_in=obj_in)

    # --- UPDATE UDM STATUS ---
    def update_udm_status(self, db: Session, *, udm_id: str, is_active: bool) -> models.Udm:
        db_udm = products_crud.udm_crud.get(db, id=udm_id)
        if not db_udm:
            raise HTTPException(status_code=404, detail="UDM não encontrada")
        
        if not is_active and db_udm.categoria_udm.unidade_referencia_id == udm_id:
            raise HTTPException(status_code=400, detail="Não é possível desativar uma UDM que é a referência de sua categoria.")

        return products_crud.udm_crud.update_status(db, db_obj=db_udm, is_active=is_active)

    # --- MÉTODOS PARA CATEGORIA DE PRODUTO ---
    def get_all_categorias_produto(self, db: Session, *, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None, search: Optional[str] = None, sort_by: Optional[str] = None, sort_order: str = "asc", exclude_id: Optional[str] = None):
        return products_crud.categoria_produto_crud.get_multi(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order, exclude_id=exclude_id)

    def create_categoria_produto(self, db: Session, *, obj_in: products_schemas.CategoriaProdutoCreate) -> models.CategoriaProduto:
        return products_crud.categoria_produto_crud.create(db, obj_in=obj_in)

    def update_categoria_produto(self, db: Session, *, id: str, obj_in: products_schemas.CategoriaProdutoUpdate) -> models.CategoriaProduto:
        db_obj = products_crud.categoria_produto_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Categoria de Produto não encontrada.")
        return products_crud.categoria_produto_crud.update(db, db_obj=db_obj, obj_in=obj_in)

    def update_categoria_produto_status(self, db: Session, *, id: str, is_active: bool) -> models.CategoriaProduto:
        db_obj = products_crud.categoria_produto_crud.get(db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Categoria de Produto não encontrada.")
        return products_crud.categoria_produto_crud.update_status(db, db_obj=db_obj, is_active=is_active)


product_structure_service = ProductStructureService()

