# backend/app/modules/administration/roles/roles_schemas.py

from pydantic import BaseModel
from typing import Optional, List

# --- Schemas de Permissão (Permission) ---
class Permission(BaseModel):
    id: str
    descricao: str

    class Config:
        from_attributes = True

# --- Schemas de Função (Role) ---

class RoleBase(BaseModel):
    id: str
    nome: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    nome: Optional[str] = None

class Role(RoleBase):
    is_active: bool
    permissions: List[Permission] = []

    class Config:
        from_attributes = True

# Schema especial para a atualização de permissões de uma função
class RolePermissionsUpdate(BaseModel):
    permission_ids: List[str]
