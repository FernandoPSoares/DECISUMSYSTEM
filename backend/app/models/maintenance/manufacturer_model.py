# File: backend/app/models/maintenance/manufacturer_model.py
import uuid
# --- ATUALIZAÇÃO DE IMPORTAÇÕES ---
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
# --- FIM DA ATUALIZAÇÃO ---
from app.core.database import Base

class Manufacturer(Base):
    """
    Modelo da Tabela para Fabricantes (Manufacturer).
    Armazena informações sobre os fabricantes dos ativos (equipamentos).
    """
    __tablename__ = "maintenance_manufacturers"

    # --- SINTAXE MODERNIZADA ---
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Informações de contacto opcionais
    contact_person: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # --- NOVO CAMPO (PACTO DO SOFT DELETE) ---
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True, 
        nullable=False, 
        index=True, 
        comment="Indica se o fabricante está ativo (True) ou 'apagado' (False)."
    )
    # --- FIM DO NOVO CAMPO ---

    # --- Relacionamentos (Modernizados) ---
    assets: Mapped[List["Asset"]] = relationship(
        "Asset", 
        back_populates="manufacturer"
    )
    # --- FIM DA MODERNIZAÇÃO ---