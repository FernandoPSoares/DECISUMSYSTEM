# backend/app/modules/inventory/brands/brands_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from .... import models
from . import brands_crud, brands_schemas

class MarcaService:
    """Camada de serviço para a lógica de negócio das Marcas."""

    def get_by_id(self, db: Session, marca_id: str) -> models.Marca:
        """Obtém uma marca pelo ID, tratando o caso de não encontrar."""
        db_marca = brands_crud.marca_crud.get(db, id=marca_id)
        if not db_marca:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca não encontrada")
        return db_marca

    def get_all(
        self,
        db: Session,
        skip: int,
        limit: int,
        is_active: Optional[bool],
        search: Optional[str],
        sort_by: Optional[str],
        sort_order: str
    ) -> List[models.Marca]:
        """Obtém todas as marcas, passando os filtros para a camada de CRUD."""
        return brands_crud.marca_crud.get_multi(
            db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order
        )

    def create(self, db: Session, marca_in: brands_schemas.MarcaCreate) -> models.Marca:
        """Cria uma nova marca, verificando se o ID já existe."""
        db_marca = brands_crud.marca_crud.get(db, id=marca_in.id)
        if db_marca:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de marca já registado")
        return brands_crud.marca_crud.create(db=db, obj_in=marca_in)

    def update(self, db: Session, marca_id: str, marca_in: brands_schemas.MarcaUpdate) -> models.Marca:
        """Atualiza uma marca."""
        db_marca = self.get_by_id(db, marca_id)
        return brands_crud.marca_crud.update(db=db, db_obj=db_marca, obj_in=marca_in)

    def update_status(self, db: Session, marca_id: str, is_active: bool) -> models.Marca:
        """Ativa ou desativa uma marca."""
        db_marca = self.get_by_id(db, marca_id)
        return brands_crud.marca_crud.update_status(db, db_obj=db_marca, is_active=is_active)

# Instância única do serviço
marca_service = MarcaService()
