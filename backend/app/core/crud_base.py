# backend/app/core/crud_base.py

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, inspect, String, Text, func
from .. import models

ModelType = TypeVar("ModelType", bound=models.Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

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
    ) -> List[ModelType]:
        query = db.query(self.model)

        # Filtro de Atividade
        if hasattr(self.model, "is_active") and is_active is not None:
            query = query.filter(self.model.is_active == is_active)

        # Lógica de Pesquisa (já era case-insensitive com ILIKE)
        if search:
            searchable_columns = [c for c in inspect(self.model).columns if isinstance(c.type, (String, Text))]
            search_filters = [column.ilike(f"%{search}%") for column in searchable_columns]
            if search_filters:
                query = query.filter(or_(*search_filters))

        # --- 2. LÓGICA DE ORDENAÇÃO CORRIGIDA PARA SER CASE-INSENSITIVE ---
        if sort_by:
            sort_column = None
            if '.' in sort_by:
                try:
                    relation_name, column_name = sort_by.split('.')
                    relation_attr = getattr(self.model, relation_name)
                    query = query.join(relation_attr)
                    related_model = relation_attr.property.mapper.class_
                    sort_column = getattr(related_model, column_name)
                except Exception:
                    sort_column = None
            else:
                if hasattr(self.model, sort_by):
                    sort_column = getattr(self.model, sort_by)

            if sort_column is not None:
                # Prepara a expressão de ordenação
                order_expression = sort_column
                # Se a coluna for do tipo texto, aplica a função LOWER()
                if isinstance(sort_column.type, (String, Text)):
                    order_expression = func.lower(sort_column)

                # Aplica a direção da ordenação à expressão
                if sort_order.lower() == "desc":
                    query = query.order_by(desc(order_expression))
                else:
                    query = query.order_by(asc(order_expression))
        
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Método genérico para criar um novo registo.
        """
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
                
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

