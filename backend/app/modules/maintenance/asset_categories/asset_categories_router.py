# File: backend/app/modules/maintenance/asset_categories/asset_categories_router.py

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.maintenance.asset_category_model import AssetCategory
from .asset_categories_crud import asset_category_crud
from .asset_categories_schemas import AssetCategoryCreate, AssetCategoryRead, AssetCategoryUpdate

router = APIRouter(
    prefix="/maintenance/asset-categories",
    tags=["Maintenance - Asset Categories"],
)

@router.post("/", response_model=AssetCategoryRead, status_code=status.HTTP_201_CREATED)
def create_asset_category(
    category_in: AssetCategoryCreate, 
    db: Session = Depends(get_db)
) -> AssetCategory:
    """
    Cria uma nova categoria de ativo.
    """
    # Validação: Verifica se já existe uma categoria com o mesmo nome
    db_category = asset_category_crud.get_by_name(db, name=category_in.name)
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria de ativo com o nome '{category_in.name}' já existe.",
        )
    return asset_category_crud.create(db=db, obj_in=category_in)

@router.get("/", response_model=List[AssetCategoryRead])
def read_asset_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = "name",
    sort_order: str = "asc",
) -> List[AssetCategory]:
    """
    Retorna uma lista de categorias de ativos.
    """
    return asset_category_crud.get_multi(
        db, skip=skip, limit=limit, search=search, sort_by=sort_by, sort_order=sort_order
    )

@router.get("/{category_id}", response_model=AssetCategoryRead)
def read_asset_category(
    category_id: uuid.UUID, 
    db: Session = Depends(get_db)
) -> AssetCategory:
    """
    Retorna uma categoria de ativo específica pelo ID.
    """
    db_category = asset_category_crud.get(db, id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Categoria de ativo não encontrada"
        )
    return db_category

@router.put("/{category_id}", response_model=AssetCategoryRead)
def update_asset_category(
    category_id: uuid.UUID,
    category_in: AssetCategoryUpdate,
    db: Session = Depends(get_db),
) -> AssetCategory:
    """
    Atualiza uma categoria de ativo.
    """
    db_category = asset_category_crud.get(db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria de ativo não encontrada",
        )
    
    # Validação: Verifica se o novo nome já está em uso por outra categoria
    if category_in.name:
        existing_category = asset_category_crud.get_by_name(db, name=category_in.name)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoria de ativo com o nome '{category_in.name}' já existe.",
            )
            
    return asset_category_crud.update(db=db, db_obj=db_category, obj_in=category_in)

@router.delete("/{category_id}", response_model=AssetCategoryRead)
def delete_asset_category(
    category_id: uuid.UUID, 
    db: Session = Depends(get_db)
) -> AssetCategory:
    """
    Deleta uma categoria de ativo.
    """
    db_category = asset_category_crud.get(db, id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria de ativo não encontrada",
        )

    # Lógica de negócio: não permitir exclusão se houver ativos associados
    if db_category.assets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar a categoria, pois existem ativos associados a ela.",
        )

    return asset_category_crud.remove(db=db, id=category_id)
