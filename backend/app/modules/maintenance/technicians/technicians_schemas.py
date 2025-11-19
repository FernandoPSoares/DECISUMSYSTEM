# File: backend/app/modules/maintenance/technicians/technicians_schemas.py

import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional

# --- Schemas Internos (para nested reads) ---
# Usamos schemas mínimos para exibir informações de modelos relacionados
# (Usuario e MaintenanceTeam) sem criar dependências de importação complexas
# entre as "fatias".

class _UserReadSimple(BaseModel):
    """Schema mínimo para exibir dados do usuário aninhado."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    usuario: str
    email: str
    is_active: bool

class _TeamReadSimple(BaseModel):
    """Schema mínimo para exibir dados da equipa aninhada."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str

# --- Schemas Principais (Technician) ---

class TechnicianBase(BaseModel):
    """Schema base para Técnico (campos comuns de criação e atualização)."""
    user_id: uuid.UUID
    team_id: Optional[uuid.UUID] = None

class TechnicianCreate(TechnicianBase):
    """Schema para criar um novo Técnico."""
    # O user_id é obrigatório para ligar a um Usuario existente.
    # O team_id é opcional (um técnico pode estar temporariamente sem equipa).
    pass

class TechnicianUpdate(BaseModel):
    """
    Schema para atualizar um Técnico.
    O único campo atualizável é a equipa a que ele pertence.
    O user_id (a ligação ao Usuario) não deve ser alterado.
    """
    team_id: Optional[uuid.UUID] = None

class TechnicianRead(TechnicianBase):
    """Schema completo para ler os dados de um Técnico, incluindo dados aninhados."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    # Carrega os dados do utilizador (nome, email, etc.)
    user: _UserReadSimple
    # Carrega os dados da equipa (se houver uma)
    team: Optional[_TeamReadSimple] = None