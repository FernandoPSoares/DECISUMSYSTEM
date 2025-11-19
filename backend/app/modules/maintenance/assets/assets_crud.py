# File: backend/app/modules/maintenance/assets/assets_crud.py

from typing import Optional, List, Any
import uuid
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, func, asc, desc

from app.core.crud_base import CRUDBase
from app.models.maintenance.asset_model import Asset
from .assets_schemas import AssetCreate, AssetUpdate

class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    """Classe CRUD específica para o modelo Asset."""

    def get(self, db: Session, id: Any) -> Optional[Asset]:
        """
        Obtém um único ativo pelo ID, otimizando o carregamento
        dos relacionamentos principais (Eager Loading).
        """
        statement = select(self.model).where(self.model.id == id).options(
            joinedload(self.model.manufacturer),
            joinedload(self.model.location),
            joinedload(self.model.category),
            joinedload(self.model.parent_asset),
            # Usamos selectinload para listas (relacionamento one-to-many)
            selectinload(self.model.child_assets) 
        )
        return db.scalars(statement).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> List[Asset]:
        """
        Obtém múltiplos ativos com otimização de carregamento (Eager Loading)
        e funcionalidades de pesquisa e ordenação.
        """
        statement = select(self.model)

        # Filtro de pesquisa (no campo 'name' e 'internal_tag')
        if search:
            statement = statement.where(
                func.lower(self.model.name).contains(func.lower(search)) |
                func.lower(self.model.internal_tag).contains(func.lower(search))
            )

        # Ordenação
        if sort_by and hasattr(self.model, sort_by):
            order_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                statement = statement.order_by(desc(order_column))
            else:
                statement = statement.order_by(asc(order_column))
        else:
            # Ordenação padrão se não especificada
            statement = statement.order_by(self.model.name)

        # Paginação
        statement = statement.offset(skip).limit(limit)
        
        # Eager Loading para otimizar relacionamentos
        statement = statement.options(
            joinedload(self.model.manufacturer),
            joinedload(self.model.location),
            joinedload(self.model.category),
            joinedload(self.model.parent_asset)
            # Não carregamos 'child_assets' na lista para evitar sobrecarga.
            # Eles podem ser carregados quando um ativo específico é selecionado.
        )

        result = db.scalars(statement).all()
        return list(result)

    def get_by_internal_tag(self, db: Session, *, internal_tag: str) -> Optional[Asset]:
        """
        Busca um ativo pela sua 'internal_tag' (case-insensitive).
        Útil para validação de duplicados.
        """
        statement = select(self.model).where(
            func.lower(self.model.internal_tag) == func.lower(internal_tag)
        )
        return db.scalars(statement).first()

    def get_by_serial_number(self, db: Session, *, serial_number: str) -> Optional[Asset]:
        """
        Busca um ativo pelo seu 'serial_number' (case-insensitive),
        ignorando valores nulos ou vazios.
        Útil para validação de duplicados.
        """
        if not serial_number:
            return None
            
        statement = select(self.model).where(
            func.lower(self.model.serial_number) == func.lower(serial_number)
        )
        return db.scalars(statement).first()

# Instância única da classe CRUD para ser usada nos services e routers
crud_asset = CRUDAsset(Asset)