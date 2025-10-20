# backend/app/modules/administration/roles/roles_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

# --- IMPORTAÇÕES CORRIGIDAS ---
from .... import models
from . import roles_crud, roles_schemas

class RolePermissionService:
    # --- Métodos para Roles ---
    def get_role_by_id(self, db: Session, role_id: str) -> models.Role:
        db_role = roles_crud.role_crud.get(db, id=role_id)
        if not db_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Função não encontrada")
        return db_role

    def get_all(
        self, 
        db: Session, 
        skip: int, 
        limit: int, 
        is_active: Optional[bool],
        search: Optional[str],
        sort_by: Optional[str],
        sort_order: str
    ) -> List[models.Usuario]:
        """
        Obtém todos os utilizadores, passando todos os filtros para a camada de CRUD.
        """
        return roles_crud.role_crud.get_multi(
            db, 
            skip=skip, 
            limit=limit, 
            is_active=is_active,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )

    def create_role(self, db: Session, role_in: roles_schemas.RoleCreate) -> models.Role:
        db_role_by_id = roles_crud.role_crud.get(db, id=role_in.id)
        if db_role_by_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID da função já registado")
        return roles_crud.role_crud.create(db=db, obj_in=role_in)

    def update_role(self, db: Session, role_id: str, role_in: roles_schemas.RoleUpdate) -> models.Role:
        """Atualiza os dados de uma função (ex: o nome)."""
        db_role = self.get_role_by_id(db, role_id)
        return roles_crud.role_crud.update(db=db, db_obj=db_role, obj_in=role_in)

    def update_role_status(self, db: Session, role_id: str, is_active: bool) -> models.Role:
        db_role = self.get_role_by_id(db, role_id)
        return roles_crud.role_crud.update_status(db, db_obj=db_role, is_active=is_active)

    def assign_permissions(self, db: Session, role_id: str, permission_ids: List[str]) -> models.Role:
        db_role = self.get_role_by_id(db, role_id)
        return roles_crud.role_crud.assign_permissions(db, db_obj=db_role, permission_ids=permission_ids)

    # --- Métodos para Permissions ---
    def get_all_permissions(self, db: Session, skip: int, limit: int) -> List[models.Permission]:
        return roles_crud.permission_crud.get_multi(db, skip=skip, limit=limit)

role_permission_service = RolePermissionService()

