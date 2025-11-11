# File: backend/app/models/maintenance/manufacturer_model.py
import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Manufacturer(Base):
    """
    Modelo da Tabela para Fabricantes (Manufacturer).
    Armazena informações sobre os fabricantes dos ativos (equipamentos).
    """
    __tablename__ = "maintenance_manufacturers"

    # Chave primária UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Nome do fabricante (ex: "Siemens", "WEG")
    # Deve ser único e indexado para buscas rápidas.
    name = Column(String(100), nullable=False, unique=True, index=True)
    
    # Informações de contacto opcionais
    contact_person = Column(String(100), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    contact_email = Column(String(100), nullable=True)

    # --- Relacionamentos ---

    # Relacionamento One-to-Many: Um fabricante para muitos ativos
    # O 'back_populates' aponta para o atributo 'manufacturer' no modelo 'Asset'
    # que criaremos a seguir.
    assets = relationship(
        "Asset", 
        back_populates="manufacturer"
    )