# backend/app/modules/inventory/brands/brands_crud.py

from sqlalchemy.orm import Session
from typing import List

from ....core.crud_base import CRUDBase
from .... import models
from . import brands_schemas

class CRUDMarca(CRUDBase[models.Marca, brands_schemas.MarcaCreate, brands_schemas.MarcaUpdate]):
    """
    Camada de acesso a dados para Marcas.
    Herda a funcionalidade genérica de CRUDBase e pode ser estendida
    com métodos específicos para a entidade Marca, se necessário.
    """
    def update_status(self, db: Session, *, db_obj: models.Marca, is_active: bool) -> models.Marca:
        """Método específico para ativar ou desativar uma marca."""
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Instância única para ser usada em toda a aplicação
marca_crud = CRUDMarca(models.Marca)
