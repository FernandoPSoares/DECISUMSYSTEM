# backend/app/modules/administration/roles/roles_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

# --- IMPORTAÇÕES CORRIGIDAS ---
from . import roles_schemas, roles_service
from ....core.dependencies import get_db, require_permission
from .... import models

# Roteador para Roles
router_roles = APIRouter(
    prefix="/roles",
    tags=["Roles e Permissões"]
)

@router_roles.post("/", response_model=roles_schemas.Role, summary="Criar uma nova função (role)")
def create_role_endpoint(
    role_in: roles_schemas.RoleCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:criar"))
):
    return roles_service.role_permission_service.create_role(db=db, role_in=role_in)

@router_roles.get("/", response_model=List[roles_schemas.Role], summary="Listar todas as funções")
def read_roles_endpoint(
    # --- MUDANÇA CRÍTICA AQUI ---
    # O nome do parâmetro agora é 'is_active' e pode ser nulo (None).
    # Isto irá corresponder ao que o serviço e o CRUD esperam.
    is_active: Optional[bool] = None, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:ler"))
):
    # A chamada ao serviço agora passa o parâmetro correto 'is_active'
    return roles_service.role_permission_service.get_all(db, skip=skip, limit=limit, is_active=is_active, search=search, sort_by=sort_by, sort_order=sort_order)

@router_roles.put("/{role_id}", response_model=roles_schemas.Role, summary="Atualizar dados de uma função")
def update_role_endpoint(
    role_id: str,
    role_in: roles_schemas.RoleUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:editar"))
):
    """
    Atualiza os dados de uma função, como o seu nome.
    """
    return roles_service.role_permission_service.update_role(db, role_id=role_id, role_in=role_in)

@router_roles.put("/{role_id}/permissions", response_model=roles_schemas.Role, summary="Definir permissões para uma função")
def set_role_permissions_endpoint(
    role_id: str, permissions: roles_schemas.RolePermissionsUpdate, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:editar_permissoes"))
):
    return roles_service.role_permission_service.assign_permissions(db, role_id=role_id, permission_ids=permissions.permission_ids)

@router_roles.put("/{role_id}/deactivate", response_model=roles_schemas.Role, summary="Desativar uma função")
def deactivate_role_endpoint(
    role_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:ativar_desativar"))
):
    return roles_service.role_permission_service.update_role_status(db, role_id=role_id, is_active=False)

@router_roles.put("/{role_id}/activate", response_model=roles_schemas.Role, summary="Reativar uma função")
def activate_role_endpoint(
    role_id: str, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:ativar_desativar"))
):
    return roles_service.role_permission_service.update_role_status(db, role_id=role_id, is_active=True)

# Roteador para Permissions (apenas leitura)
router_permissions = APIRouter(
    prefix="/permissions",
    tags=["Roles e Permissões"]
)

@router_permissions.get("/", response_model=List[roles_schemas.Permission], summary="Listar todas as permissões disponíveis")
def read_permissions_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(require_permission("roles:ler"))
):
    return roles_service.role_permission_service.get_all_permissions(db, skip=skip, limit=limit)

