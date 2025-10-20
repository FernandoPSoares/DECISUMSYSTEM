# backend/app/modules/inventory/products/products_crud.py

from sqlalchemy.orm import Session, joinedload, aliased, selectinload, with_loader_criteria
from sqlalchemy import or_, asc, desc, func, inspect, String, Text, and_
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
        Sobrescreve o get_multi para lidar com a lógica complexa de carregamento
        para a vista de Ativos e Arquivo.
        """
        
        # --- Lógica para a VISTA DE ARQUIVO (is_active = False) ---
        if is_active is False:
            # Query A: Busca todas as categorias inativas. Para estas, carrega TODAS as suas UDMs (ativas ou inativas).
            inactive_cats_q = db.query(self.model).filter(self.model.is_active == False).options(
                selectinload(self.model.udms),
                joinedload(self.model.unidade_referencia)
            ).all()

            # Query B: Busca categorias ATIVAS que têm PELO MENOS UMA UDM inativa.
            active_cats_with_inactive_udms_q = db.query(self.model).filter(
                and_(
                    self.model.is_active == True,
                    self.model.udms.any(models.Udm.is_active == False)
                )
            ).options(
                # Para estas categorias, carrega APENAS as suas UDMs inativas.
                with_loader_criteria(models.Udm, lambda cls: cls.is_active == False),
                joinedload(self.model.unidade_referencia)
            ).all()
            
            # Junta os resultados em memória, garantindo unicidade
            all_archived = {cat.id: cat for cat in inactive_cats_q}
            for cat in active_cats_with_inactive_udms_q:
                if cat.id not in all_archived:
                    all_archived[cat.id] = cat
            
            # Ordena e aplica paginação
            sorted_list = sorted(list(all_archived.values()), key=lambda c: c.id)
            return sorted_list[skip: skip + limit]

        # --- Lógica para a VISTA DE ATIVOS (is_active = True) ou VISTA SEM FILTRO (is_active = None) ---
        query = db.query(self.model)
        options = [joinedload(self.model.unidade_referencia)]

        if is_active is True:
            query = query.filter(self.model.is_active == True)
            # Carrega apenas as UDMs que também estão ativas
            options.append(with_loader_criteria(models.Udm, lambda cls: cls.is_active == True))
        else: # is_active is None
            # Carrega todas as UDMs
            options.append(selectinload(self.model.udms))

        query = query.options(*options)
        
        # Lógica de Pesquisa
        if search:
            search_filters = [c.ilike(f"%{search}%") for c in inspect(self.model).columns if isinstance(c.type, (String, Text))]
            if search_filters:
                query = query.filter(or_(*search_filters))
        
        # Lógica de Ordenação
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
        query = db.query(self.model).options(joinedload(self.model.categoria_udm))
        
        if is_active is not None:
            query = query.filter(self.model.is_active == is_active)

        if search:
            search_filters = [c.ilike(f"%{search}%") for c in inspect(self.model).columns if isinstance(c.type, (String, Text))]
            if search_filters:
                query = query.filter(or_(*search_filters))

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

categoria_udm_crud = CRUDCategoriaUdm(models.CategoriaUdm)
udm_crud = CRUDUdm(models.Udm)
categoria_produto_crud = CRUDCategoriaProduto(models.CategoriaProduto)

