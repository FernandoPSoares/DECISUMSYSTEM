# backend/app/modules/administration/users/users_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from .... import models
from . import users_crud, users_schemas

class UsuarioService:
    def get_by_id(self, db: Session, usuario_id: str) -> models.Usuario:
        db_user = users_crud.usuario_crud.get(db, id=usuario_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilizador não encontrado")
        return db_user

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
        return users_crud.usuario_crud.get_multi(
            db, 
            skip=skip, 
            limit=limit, 
            is_active=is_active,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )

    def create(self, db: Session, usuario_in: users_schemas.UsuarioCreate) -> models.Usuario:
        db_user_by_name = users_crud.usuario_crud.get_by_usuario(db, usuario_name=usuario_in.usuario)
        if db_user_by_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de utilizador já registado")
        
        db_user_by_id = users_crud.usuario_crud.get(db, id=usuario_in.id)
        if db_user_by_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de utilizador já registado")
        
        return users_crud.usuario_crud.create(db=db, obj_in=usuario_in)

    def update(self, db: Session, usuario_id: str, usuario_in: users_schemas.UsuarioUpdate) -> models.Usuario:
        db_user = self.get_by_id(db, usuario_id)
        return users_crud.usuario_crud.update(db=db, db_obj=db_user, obj_in=usuario_in)

    def update_status(self, db: Session, usuario_id: str, is_active: bool) -> models.Usuario:
        db_user = self.get_by_id(db, usuario_id)
        return users_crud.usuario_crud.update_status(db, db_obj=db_user, is_active=is_active)

    def change_own_password(self, db: Session, *, user_obj: models.Usuario, password_in: users_schemas.UsuarioPasswordChange) -> None:
        is_correct_password = security.verify_password(
            plain_password=password_in.senha_antiga,
            hashed_password=user_obj.senha_hash
        )
        if not is_correct_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha antiga incorreta")
            
        new_hashed_password = security.get_password_hash(password_in.senha_nova)
        update_data = {"senha_hash": new_hashed_password}
        users_crud.usuario_crud.update(db=db, db_obj=user_obj, obj_in=update_data)

    def set_user_password(self, db: Session, *, user_obj: models.Usuario, password_in: users_schemas.UsuarioAdminPasswordSet) -> None:
        new_hashed_password = security.get_password_hash(password_in.senha_nova)
        update_data = {"senha_hash": new_hashed_password}
        users_crud.usuario_crud.update(db=db, db_obj=user_obj, obj_in=update_data)

usuario_service = UsuarioService()

