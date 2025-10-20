# backend/app/modules/inventory/products/products_crud.py

from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import or_, asc, desc, func, inspect, String, Text
from typing import List, Optional

from ....core.crud_base import CRUDBase
from .... import models
from . import products_schemas

class CRUDCategoriaUdm(CRUDBase[models.CategoriaUdm, products_schemas.CategoriaUdmCreate, products_schemas.CategoriaUdmUpdate]):
    def get_multi(
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
        """
        Sobrescreve o get_multi para otimizar o carregamento das relações 'udms' e 'unidade_referencia',
        mantendo toda a lógica de filtragem e ordenação da CRUDBase.
        """
        query = db.query(self.model).options(
            joinedload(self.model.udms),
            joinedload(self.model.unidade_referencia)
        )
        
        # Reaplica a lógica de filtragem e ordenação da CRUDBase
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)

        if search:
            search_filters = [c.ilike(f"%{search}%") for c in inspect(self.model).columns if isinstance(c.type, (String, Text))]
            if search_filters:
                query = query.filter(or_(*search_filters))
        
        if sort_by and hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            order_expression = func.lower(sort_column) if isinstance(sort_column.type, (String, Text)) else sort_column
            query = query.order_by(desc(order_expression) if sort_order.lower() == "desc" else asc(order_expression))

        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.CategoriaUdm, is_active: bool) -> models.CategoriaUdm:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDUdm(CRUDBase[models.Udm, products_schemas.UdmCreate, products_schemas.UdmUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[models.Udm]:
        """
        Sobrescreve o get_multi para otimizar o carregamento da relação 'categoria_udm'.
        """
        query = db.query(self.model).options(joinedload(self.model.categoria_udm))
        
        # Reaplica a lógica de filtragem e ordenação da CRUDBase
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)

        if search:
            search_filters = [c.ilike(f"%{search}%") for c in inspect(self.model).columns if isinstance(c.type, (String, Text))]
            if search_filters:
                query = query.filter(or_(*search_filters))

        # Lógica de ordenação especializada para a relação
        if sort_by == 'categoria_udm.nome':
            query = query.join(models.CategoriaUdm)
            order_expression = func.lower(models.CategoriaUdm.nome)
            query = query.order_by(desc(order_expression) if sort_order.lower() == "desc" else asc(order_expression))
        elif sort_by and hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            order_expression = func.lower(sort_column) if isinstance(sort_column.type, (String, Text)) else sort_column
            query = query.order_by(desc(order_expression) if sort_order.lower() == "desc" else asc(order_expression))

        return query.offset(skip).limit(limit).all()


    def update_status(self, db: Session, *, db_obj: models.Udm, is_active: bool) -> models.Udm:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDCategoriaProduto(CRUDBase[models.CategoriaProduto, products_schemas.CategoriaProdutoCreate, products_schemas.CategoriaProdutoUpdate]):
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
        exclude_id: Optional[str] = None # Parâmetro para o formulário
    ) -> List[models.CategoriaProduto]:
        """
        Sobrescreve o get_multi para lidar com a ordenação especial e o filtro de exclusão.
        """
        query = db.query(self.model)

        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)
        
        if search:
            query = query.filter(self.model.nome.ilike(f"%{search}%"))
        
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)

        # Lógica de ordenação especializada para a relação auto-referencial
        if sort_by == 'categoria_pai.nome':
            ParentCategory = aliased(models.CategoriaProduto)
            query = query.outerjoin(ParentCategory, self.model.categoria_pai_id == ParentCategory.id)
            order_expression = func.lower(ParentCategory.nome)
            
            if sort_order.lower() == "desc":
                query = query.order_by(desc(order_expression))
            else:
                query = query.order_by(asc(order_expression))
        else:
            # Se não for para ordenar pela categoria-pai, usa a lógica genérica da classe-pai
            # que já foi definida no início desta função (sem chamar super()).
            if sort_by and hasattr(self.model, sort_by):
                sort_column = getattr(self.model, sort_by)
                order_expression = func.lower(sort_column) if isinstance(sort_column.type, (String, Text)) else sort_column
                query = query.order_by(desc(order_expression) if sort_order.lower() == "desc" else asc(order_expression))

        return query.offset(skip).limit(limit).all()

    def update_status(self, db: Session, *, db_obj: models.CategoriaProduto, is_active: bool) -> models.CategoriaProduto:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Cria os objetos de CRUD para serem usados pelo serviço
categoria_udm_crud = CRUDCategoriaUdm(models.CategoriaUdm)
udm_crud = CRUDUdm(models.Udm)
categoria_produto_crud = CRUDCategoriaProduto(models.CategoriaProduto)

