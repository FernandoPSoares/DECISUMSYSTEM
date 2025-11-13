# File: backend/app/modules/maintenance/manufacturers/manufacturers_router.py

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importa as dependências centrais (sessão da BD e autenticação)
from app.core.dependencies import get_db, get_current_active_user

# Importa os Schemas (Contratos) e o Serviço (Lógica de Negócio) desta fatia
from .manufacturers_schemas import (
    ManufacturerRead, 
    ManufacturerCreate, 
    ManufacturerUpdate
)
from .manufacturers_service import manufacturer_service

# Cria o router específico para esta fatia
router = APIRouter(
    prefix="/manufacturers",
    tags=["Manutenção - Fabricantes"],
    # Aplica a dependência de autenticação a TODOS os endpoints abaixo
    dependencies=[Depends(get_current_active_user)]
)

@router.post(
    "/", 
    response_model=ManufacturerRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo fabricante"
)
def create_manufacturer(
    manufacturer_in: ManufacturerCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria um novo fabricante de equipamento.
    
    A lógica de negócio no serviço (manufacturer_service) irá:
    - Verificar se um fabricante com o mesmo nome já existe.
    - Se existir e estiver inativo (soft-deleted), irá reativá-lo.
    - Se existir e estiver ativo, lançará um erro 400.
    - Se não existir, criará um novo.
    """
    return manufacturer_service.create_manufacturer(db, manufacturer_in=manufacturer_in)

@router.get(
    "/", 
    response_model=List[ManufacturerRead],
    summary="Listar todos os fabricantes ativos"
)
def get_all_manufacturers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Obtém uma lista paginada de todos os fabricantes ATIVOS.
    A filtragem de 'is_active' é tratada automaticamente pela CRUDBase.
    """
    return manufacturer_service.get_all_manufacturers(db, skip=skip, limit=limit)

@router.get(
    "/{manufacturer_id}", 
    response_model=ManufacturerRead,
    summary="Obter um fabricante por ID"
)
def get_manufacturer_by_id(
    manufacturer_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """
    Obtém um fabricante específico pelo seu ID.
    O serviço lançará um erro 404 se o fabricante não for encontrado
    ou se estiver inativo (soft-deleted).
    """
    return manufacturer_service.get_manufacturer_by_id(db, manufacturer_id=manufacturer_id)

@router.put(
    "/{manufacturer_id}", 
    response_model=ManufacturerRead,
    summary="Atualizar um fabricante"
)
def update_manufacturer(
    manufacturer_id: uuid.UUID,
    manufacturer_in: ManufacturerUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza as informações de um fabricante existente.
    
    A lógica de negócio no serviço (manufacturer_service) irá:
    - Verificar se o fabricante existe e está ativo.
    - Se o nome for alterado, verificar se o novo nome já está em uso
      por OUTRO fabricante (ativo ou inativo).
    """
    return manufacturer_service.update_manufacturer(
        db, manufacturer_id=manufacturer_id, manufacturer_in=manufacturer_in
    )

@router.delete(
    "/{manufacturer_id}", 
    response_model=ManufacturerRead,
    summary="Desativar (soft delete) um fabricante"
)
def delete_manufacturer(
    manufacturer_id: uuid.UUID, 
    db: Session = Depends(get_db)
):
    """
    Desativa (soft delete) um fabricante.
    
    O fabricante não é permanentemente apagado da base de dados.
    O seu campo 'is_active' é definido como 'False'.
    
    O serviço lançará um erro 404 se o fabricante já não for encontrado
    ou se já estiver inativo.
    """
    return manufacturer_service.delete_manufacturer(db, manufacturer_id=manufacturer_id)