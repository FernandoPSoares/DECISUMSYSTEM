# File: backend/app/modules/maintenance/asset_categories/asset_categories_crud.py

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Optional

from app.core.crud_base import CRUDBase
from app.models.maintenance.asset_category_model import AssetCategory
from .asset_categories_schemas import AssetCategoryCreate, AssetCategoryUpdate

class CRUDAssetCategory(CRUDBase[AssetCategory, AssetCategoryCreate, AssetCategoryUpdate]):
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[AssetCategory]:
        """
        Busca uma categoria de ativo pelo nome (case-insensitive).
        """
        statement = select(self.model).where(func.lower(self.model.name) == func.lower(name))
        return db.scalars(statement).first()

asset_category_crud = CRUDAssetCategory(AssetCategory)
