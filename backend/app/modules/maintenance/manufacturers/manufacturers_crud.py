# File: backend/app/modules/maintenance/manufacturers/manufacturers_crud.py

from sqlalchemy.orm import Session
from typing import Optional

# Importa a base de CRUD que já existe no seu projeto
from app.core.crud_base import CRUDBase

# Importa o Modelo e os Schemas desta "fatia"
from app.models.maintenance.manufacturer_model import Manufacturer
from .manufacturers_schemas import ManufacturerCreate, ManufacturerUpdate


class CRUDManufacturer(CRUDBase[Manufacturer, ManufacturerCreate, ManufacturerUpdate]):
    """
    Classe de Acesso a Dados (CRUD) para o modelo Manufacturer.
    Herda as operações básicas (get, get_multi, create, update, remove)
    de CRUDBase, que já lidam com o 'soft delete' (is_active).
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[Manufacturer]:
        """
        Obtém um fabricante pelo seu nome exato (ativo OU inativo).
        
        Esta verificação é usada pelo serviço para garantir a unicidade do nome
        (UNIQUE constraint) antes de criar ou atualizar um registo.
        """
        # Procura em TODOS os registos, ignorando 'is_active', para
        # garantir que o nome é verdadeiramente único na base de dados.
        return db.query(self.model).filter(self.model.name == name).first()

# Cria uma instância única (singleton) do CRUD para ser usada pelos serviços
manufacturer_crud = CRUDManufacturer(Manufacturer)