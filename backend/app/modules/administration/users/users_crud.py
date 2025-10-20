# backend/app/modules/administration/users/users_crud.py

from sqlalchemy.orm import Session

# --- IMPORTAÇÕES CORRIGIDAS ---
from ....core.crud_base import CRUDBase
from .... import models
from . import users_schemas
from ....core.security import get_password_hash
from sqlalchemy import or_

class CRUDUsuario(CRUDBase[models.Usuario, users_schemas.UsuarioCreate, users_schemas.UsuarioUpdate]):
    
    def get_by_username_or_email(self, db: Session, *, identifier: str) -> models.Usuario:
        """
        Busca um utilizador pelo seu nome de utilizador OU pelo seu e-mail.
        """
        return db.query(self.model).filter(
            or_(self.model.usuario == identifier, self.model.email == identifier)
        ).first()

    def get_by_usuario(self, db: Session, *, usuario_name: str) -> models.Usuario:
        """Método específico para buscar um utilizador pelo nome de utilizador."""
        return db.query(self.model).filter(self.model.usuario == usuario_name).first()

    def create(self, db: Session, *, obj_in: users_schemas.UsuarioCreate) -> models.Usuario:
        """Sobrescreve o método create para encriptar a senha antes de guardar."""
        hashed_password = get_password_hash(obj_in.senha)
        db_obj = self.model(
            id=obj_in.id,
            usuario=obj_in.usuario,
            email=obj_in.email,
            senha_hash=hashed_password,
            role_id=obj_in.role_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_status(self, db: Session, *, db_obj: models.Usuario, is_active: bool) -> models.Usuario:
        """Método específico para ativar ou desativar um utilizador."""
        db_obj.is_active = is_active
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Renomeado para maior clareza dentro do módulo
usuario_crud = CRUDUsuario(models.Usuario)

