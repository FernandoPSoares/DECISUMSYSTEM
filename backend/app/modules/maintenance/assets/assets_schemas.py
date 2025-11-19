# File: backend/app/modules/maintenance/assets/assets_schemas.py

import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# Importa Enums diretamente dos models para consistência
from app.models.maintenance.asset_model import AssetStatus
from app.models.maintenance.work_order_model import WorkOrderStatus
from app.models.maintenance.pm_plan_model import PMTriggerType

# --- CORREÇÃO DE IMPORTAÇÃO ---
# O schema de leitura chama-se 'Local' e não 'LocalRead'.
# Importamos 'as LocalRead' para manter a clareza no resto do ficheiro.
from app.modules.inventory.locations.locations_schemas import Local as LocalRead
# --- FIM DA CORREÇÃO ---

from app.modules.maintenance.manufacturers.manufacturers_schemas import ManufacturerRead

# --- Schemas Mínimos para Relacionamentos ---
# (Para evitar importações circulares e sobrecarga de dados)

class AssetCategoryReadMinimal(BaseModel):
    """Schema mínimo para exibir a categoria do ativo."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str

class AssetReadMinimal(BaseModel):
    """Schema mínimo para exibir informações de hierarquia (pai/filho)."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    internal_tag: str
    status: AssetStatus

class WorkOrderReadMinimal(BaseModel):
    """Schema mínimo para listar Ordens de Serviço associadas."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    wo_number: str
    title: str
    status: WorkOrderStatus

class PMPlanReadMinimal(BaseModel):
    """Schema mínimo para listar Planos de PM associados."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    plan_number: str
    title: str
    is_active: bool
    trigger_type: PMTriggerType

class AssetMeterReadMinimal(BaseModel):
    """Schema mínimo para listar Medidores associados."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    meter_name: str
    last_reading: Optional[float] = None
    last_reading_date: Optional[datetime] = None
    # (Futuramente incluirá udm_name quando o schema de UDM estiver pronto)

class AssetSparePartReadMinimal(BaseModel):
    """Schema mínimo para listar Peças Sobressalentes associadas."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    product_id: uuid.UUID # (Eventualmente será um ProductReadMinimal)
    quantity_required: float
    # (Futuramente incluirá product_name e product_code)


# --- Schemas Principais do Ativo (Asset) ---

class AssetBase(BaseModel):
    """Schema base com campos comuns para criação e atualização."""
    name: str
    description: Optional[str] = None
    serial_number: Optional[str] = None
    internal_tag: str
    status: AssetStatus = AssetStatus.OPERATIONAL
    is_critical: bool = False
    
    purchase_date: Optional[datetime] = None
    installation_date: Optional[datetime] = None
    warranty_expiry_date: Optional[datetime] = None

    # Chaves estrangeiras (IDs)
    manufacturer_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    
    # --- CORREÇÃO DE TIPO DE DADO ---
    # O ID de Local é String(36) e não UUID
    location_id: Optional[str] = None 
    # --- FIM DA CORREÇÃO ---
    
    parent_asset_id: Optional[uuid.UUID] = None

class AssetCreate(AssetBase):
    """Schema usado para criar um novo Ativo."""
    # name e internal_tag são obrigatórios e já definidos no AssetBase
    pass

class AssetUpdate(AssetBase):
    """
    Schema usado para atualizar um Ativo.
    Todos os campos são opcionais.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    serial_number: Optional[str] = None
    internal_tag: Optional[str] = None
    status: Optional[AssetStatus] = None
    is_critical: Optional[bool] = None
    
    purchase_date: Optional[datetime] = None
    installation_date: Optional[datetime] = None
    warranty_expiry_date: Optional[datetime] = None
    
    manufacturer_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    
    # --- CORREÇÃO DE TIPO DE DADO ---
    location_id: Optional[str] = None
    # --- FIM DA CORREÇÃO ---
    
    parent_asset_id: Optional[uuid.UUID] = None

class AssetRead(AssetBase):
    """Schema completo para leitura (retorno da API) de um Ativo."""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    # --- Relacionamentos ---
    
    # Relacionamentos que já possuem schemas
    manufacturer: Optional[ManufacturerRead] = None
    category: Optional[AssetCategoryReadMinimal] = None
    location: Optional[LocalRead] = None # (Agora usa o 'Local as LocalRead')
    
    # Hierarquia (Pai/Filho)
    parent_asset: Optional[AssetReadMinimal] = None
    child_assets: List[AssetReadMinimal] = []
    
    # Listas de componentes do Ativo (BOM, Medidores)
    spare_parts: List[AssetSparePartReadMinimal] = []
    meters: List[AssetMeterReadMinimal] = []

    # Histórico e Planeamento
    work_orders: List[WorkOrderReadMinimal] = []
    pm_plans: List[PMPlanReadMinimal] = []