# File: backend/app/modules/maintenance/teams/teams_schemas.py

import uuid
from pydantic import BaseModel, Field
from typing import Optional, List

# --- Schema Base Comum ---
# Define a configuração Padrão para todos os schemas
# Habilita o 'from_attributes=True' para que os schemas
# possam ser criados a partir dos modelos SQLAlchemy.
class SchemaBase(BaseModel):
    class ConfigDict:
        from_attributes = True

# --- Schemas para MaintenanceTeam ---

# 1. MaintenanceTeamBase: Campos partilhados
# Contém os campos que são comuns à criação e leitura.
class MaintenanceTeamBase(SchemaBase):
    name: str = Field(
        ...,  # ... (elipses) significa que o campo é obrigatório
        max_length=100, 
        examples=["Equipa Mecânica A"]
    )

# 2. MaintenanceTeamCreate: Schema para Criação
# Usado no endpoint POST. É o que o frontend envia.
class MaintenanceTeamCreate(MaintenanceTeamBase):
    # Por agora, idêntico ao Base.
    pass

# 3. MaintenanceTeamUpdate: Schema para Atualização
# Usado no endpoint PUT/PATCH. Todos os campos são opcionais.
class MaintenanceTeamUpdate(SchemaBase):
    name: Optional[str] = Field(
        None, # 'None' torna o campo opcional
        max_length=100, 
        examples=["Equipa Elétrica B"]
    )

# 4. MaintenanceTeamReadSimple: Schema de Leitura (Leve)
# Usado para listas, dropdowns, ou quando não queremos
# carregar todos os relacionamentos pesados (como técnicos, OSs).
class MaintenanceTeamReadSimple(MaintenanceTeamBase):
    id: uuid.UUID

# 5. MaintenanceTeamRead: Schema de Leitura (Completo)
# Usado para ver os detalhes de UMA equipa.
# Herda do ReadSimple e, no futuro, adicionará os relacionamentos.
class MaintenanceTeamRead(MaintenanceTeamReadSimple):
    
    # --- Relacionamentos Futuros ---
    # Quando tivermos os schemas de Técnicos e OSs, poderemos
    # descomentar e adicionar estas linhas para mostrar dados relacionados.
    
    # technicians: List["TechnicianReadSimple"] = []
    # assigned_work_orders_count: int = 0
    
    pass