# backend/app/modules/administration/users/users_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

# Importamos os schemas deste módulo e o serviço
from . import users_schemas, users_service
# Importamos as dependências do nosso core e os modelos da raiz
from ....core.dependencies import get_db, require_permission, get_current_active_user
from .... import models

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=users_schemas.Usuario, summary="Criar um novo utilizador")
def create_usuario_endpoint(
    usuario_in: users_schemas.UsuarioCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("usuarios:criar"))
):
    """Cria um novo utilizador. Requer a permissão 'usuarios:criar'."""
    return users_service.usuario_service.create(db=db, usuario_in=usuario_in)

@router.get("/", response_model=List[users_schemas.Usuario], summary="Listar utilizadores")
def read_usuarios_endpoint(
    is_active: Optional[bool] = None, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc", 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("usuarios:ler"))
):
    """Lista utilizadores. Requer a permissão 'usuarios:ler'."""
    return users_service.usuario_service.get_all(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order)

@router.get("/{usuario_id}", response_model=users_schemas.Usuario, summary="Obter um utilizador por ID")
def read_usuario_endpoint(
    usuario_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("usuarios:ler"))
):
    """Obtém um utilizador pelo seu ID. Requer a permissão 'usuarios:ler'."""
    return users_service.usuario_service.get_by_id(db, usuario_id=usuario_id)

@router.put("/{usuario_id}", response_model=users_schemas.Usuario, summary="Atualizar um utilizador")
def update_usuario_endpoint(
    usuario_id: str, 
    usuario_in: users_schemas.UsuarioUpdate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("usuarios:editar"))
):
    """Atualiza os dados de um utilizador. Requer a permissão 'usuarios:editar'."""
    return users_service.usuario_service.update(db, usuario_id=usuario_id, usuario_in=usuario_in)

@router.put("/me/change-password", status_code=204, summary="Alterar a própria senha")
def change_own_password_endpoint(
    password_in: users_schemas.UsuarioPasswordChange,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    """Permite que o utilizador autenticado altere a sua própria senha."""
    users_service.usuario_service.change_own_password(
        db=db, user_obj=current_user, password_in=password_in
    )
    return

@router.put("/{usuario_id}/set-password", status_code=204, summary="Definir a senha de um utilizador (Admin)")
def set_user_password_endpoint(
    usuario_id: str,
    password_in: users_schemas.UsuarioAdminPasswordSet,
    db: Session = Depends(get_db),
    current_admin: models.Usuario = Depends(require_permission("usuarios:definir_senha"))
):
    """Permite que um administrador defina uma nova senha para qualquer utilizador."""
    target_user = users_service.usuario_service.get_by_id(db, usuario_id)
    users_service.usuario_service.set_user_password(
        db=db, user_obj=target_user, password_in=password_in
    )
    return

@router.put("/{usuario_id}/deactivate", response_model=users_schemas.Usuario, summary="Desativar um utilizador")
def deactivate_usuario_endpoint(
    usuario_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("usuarios:ativar_desativar"))
):
    """Desativa um utilizador. Requer a permissão 'usuarios:ativar_desativar'."""
    return users_service.usuario_service.update_status(db, usuario_id=usuario_id, is_active=False)

@router.put("/{usuario_id}/activate", response_model=users_schemas.Usuario, summary="Reativar um utilizador")
def activate_usuario_endpoint(
    usuario_id: str, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("usuarios:ativar_desativar"))
):
    """Reativa um utilizador. Requer a permissão 'usuarios:ativar_desativar'."""
    return users_service.usuario_service.update_status(db, usuario_id=usuario_id, is_active=True)

