# backend/app/modules/inventory/udms/udms_crud.py

from sqlalchemy.orm import Session, joinedload, with_loader_criteria, selectinload
from sqlalchemy import or_, asc, desc, func, inspect, String, Text, and_
from typing import List, Optional

from ....core.crud_base import CRUDBase
from .... import models
from . import udms_schemas

class CRUDCategoriaUdm(CRUDBase[models.CategoriaUdm, udms_schemas.CategoriaUdmCreate, udms_schemas.CategoriaUdmUpdate]):
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
        if is_active is False:
            inactive_cats_q = db.query(self.model).filter(self.model.is_active == False).options(
                selectinload(self.model.udms),
                joinedload(self.model.unidade_referencia)
            ).all()
            active_cats_with_inactive_udms_q = db.query(self.model).filter(
                and_(
                    self.model.is_active == True,
                    self.model.udms.any(models.Udm.is_active == False)
                )
            ).options(
                with_loader_criteria(models.Udm, lambda cls: cls.is_active == False),
                joinedload(self.model.unidade_referencia)
            ).all()
            all_archived = {cat.id: cat for cat in inactive_cats_q}
            for cat in active_cats_with_inactive_udms_q:
                if cat.id not in all_archived:
                    all_archived[cat.id] = cat
            sorted_list = sorted(list(all_archived.values()), key=lambda c: c.id)
            return sorted_list[skip: skip + limit]

        query = db.query(self.model)
        options = [joinedload(self.model.unidade_referencia)]

        if is_active is True:
            query = query.filter(self.model.is_active == True)
            options.append(with_loader_criteria(models.Udm, lambda cls: cls.is_active == True))
        else:
            options.append(selectinload(self.model.udms))

        query = query.options(*options)
        
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

class CRUDUdm(CRUDBase[models.Udm, udms_schemas.UdmCreate, udms_schemas.UdmUpdate]):
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

categoria_udm_crud = CRUDCategoriaUdm(models.CategoriaUdm)
udm_crud = CRUDUdm(models.Udm)
