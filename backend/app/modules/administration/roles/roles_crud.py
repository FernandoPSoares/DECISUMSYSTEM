# backend/app/modules/administration/roles/roles_crud.py

from sqlalchemy.orm import Session
from typing import List

from ....core.crud_base import CRUDBase
from .... import models
from . import roles_schemas

class CRUDRole(CRUDBase[models.Role, roles_schemas.RoleCreate, roles_schemas.RoleUpdate]):
    # O método get_multi foi REMOVIDO daqui. Agora, ele irá usar a versão corrigida da CRUDBase.
    
    def update_status(self, db: Session, *, db_obj: models.Role, is_active: bool) -> models.Role:
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def assign_permissions(self, db: Session, *, db_obj: models.Role, permission_ids: List[str]) -> models.Role:
        permissions = db.query(models.Permission).filter(models.Permission.id.in_(permission_ids)).all()
        db_obj.permissions = permissions
        db.commit()
        db.refresh(db_obj)
        return db_obj

class CRUDPermission(CRUDBase[models.Permission, None, None]):
    pass

role_crud = CRUDRole(models.Role)
permission_crud = CRUDPermission(models.Permission)

