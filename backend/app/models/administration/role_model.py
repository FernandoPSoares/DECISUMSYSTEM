# backend/app/models/administration/role_model.py

from sqlalchemy import Column, String, ForeignKey, Boolean, Table, DateTime, func
from sqlalchemy.orm import relationship

# Importa a Base partilhada a partir do nosso core
from ...core.database import Base

# Tabela de associação que liga Funções a Permissões
role_permissions = Table('role_permissions', Base.metadata,
    Column('role_id', String(50), ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', String(50), ForeignKey('permissions.id'), primary_key=True)
)

class Role(Base):
    """Armazena as funções (cargos) que os utilizadores podem ter."""
    __tablename__ = 'roles'
    id = Column(String(50), primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    # --- MELHORIAS DE ARQUITETURA ---
    is_system_role = Column(Boolean, nullable=False, default=False, comment="Funções de sistema não podem ser apagadas ou ter permissões alteradas por utilizadores normais.")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("Usuario", back_populates="role")

class Permission(Base):
    """Armazena as ações granulares que podem ser controladas no sistema."""
    __tablename__ = 'permissions'
    id = Column(String(50), primary_key=True)
    descricao = Column(String(255), nullable=False)
    
    # --- MELHORIAS DE ARQUITETURA ---
    module = Column(String(50), nullable=False, index=True, comment="O módulo de negócio a que a permissão pertence (ex: 'administration', 'inventory').")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

