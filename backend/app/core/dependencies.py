# backend/app/core/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import security, database
from .. import models
from ..modules.administration.users import users_crud 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Usuario:
    """Dependência para obter o utilizador atual a partir de um token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = security.get_username_from_token(token)
    
    if not username:
        raise credentials_exception
    
    user = users_crud.usuario_crud.get_by_usuario(db, usuario_name=username)
    
    if not user:
        raise credentials_exception
    return user

def get_current_active_user(current_user: models.Usuario = Depends(get_current_user)) -> models.Usuario:
    """Dependência que, com base no utilizador atual, verifica se ele está ativo."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Utilizador inativo")
    return current_user

def require_permission(permission_id: str):
    """
    Fábrica de dependências ("segurança"). Retorna uma função que verifica
    se o utilizador ativo atual tem a permissão necessária.
    """
    def _permission_checker(current_user: models.Usuario = Depends(get_current_active_user)) -> models.Usuario:
        user_permissions = {p.id for p in current_user.role.permissions}
        if permission_id not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não tem permissão para executar esta ação.",
            )
        return current_user

    return _permission_checker

