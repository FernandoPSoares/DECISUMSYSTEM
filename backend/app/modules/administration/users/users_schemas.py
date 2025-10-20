# backend/app/modules/administration/users/users_schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uuid # <-- 1. IMPORTAMOS A BIBLIOTECA UUID

# ... (Schemas de Permission e Role, sem alterações) ...
# --- Schemas de Apoio (Role e Permission) ---
class Permission(BaseModel):
    id: str
    descricao: str
    class Config: from_attributes = True

class Role(BaseModel):
    id: str
    nome: str
    is_active: bool 
    permissions: List[Permission] = []
    class Config: from_attributes = True


# --- Schemas de Usuário ---

class UsuarioBase(BaseModel):
    usuario: str
    email: EmailStr
    role_id: str

class UsuarioCreate(UsuarioBase):
    senha: str
    # Opcional: Adicionamos external_id para a criação
    external_id: Optional[str] = None

class UsuarioUpdate(BaseModel):
    usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    role_id: Optional[str] = None
    is_active: Optional[bool] = None

class Usuario(UsuarioBase):
    """
    Schema para a leitura de um utilizador (respostas da API).
    """
    # --- 2. MUDANÇA CRÍTICA AQUI ---
    # O 'id' agora é do tipo UUID para corresponder ao modelo da base de dados.
    # O Pydantic irá automaticamente converter o objeto UUID para uma string no JSON final.
    id: uuid.UUID
    is_active: bool
    role: Role 

    class Config:
        from_attributes = True

# --- Schemas para Alteração de Senha ---

class UsuarioPasswordChange(BaseModel):
    senha_antiga: str
    senha_nova: str

class UsuarioAdminPasswordSet(BaseModel):
    senha_nova: str

