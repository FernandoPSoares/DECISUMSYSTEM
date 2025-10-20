# backend/app/models/administration/user_model.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
# --- 1. IMPORTAÇÕES ADICIONAIS ---
# Importamos o tipo UUID do PostgreSQL e a biblioteca uuid do Python.
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    # --- 2. COLUNA 'id' ATUALIZADA ---
    # A chave primária agora é um UUID, com um valor padrão gerado automaticamente.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # --- 3. NOVA COLUNA 'external_id' ADICIONADA ---
    # Para a integração com o sistema antigo. É opcional, mas se existir, tem de ser único.
    external_id = Column(String(50), unique=True, index=True, nullable=True)

    usuario = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    role_id = Column(String(50), ForeignKey('roles.id'), nullable=False)
    role = relationship("Role", back_populates="users")

class PasswordResetToken(Base):
    """Armazena os tokens de uso único para a recuperação de senhas."""
    __tablename__ = 'password_reset_tokens'
    token = Column(String(255), primary_key=True, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False) # <-- ATUALIZADO para corresponder ao novo tipo de ID
    user = relationship("Usuario")
