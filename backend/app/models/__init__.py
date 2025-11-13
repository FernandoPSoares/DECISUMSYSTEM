# File: backend/app/models/__init__.py

# Importa a nossa Base partilhada a partir do core da aplicação
from ..core.database import Base

# --- IMPORTAÇÃO FINAL DE TODOS OS MÓDULOS ---
# Este ficheiro agora serve como o "ponto de encontro" central para que
# o SQLAlchemy e o Alembic consigam descobrir todas as nossas tabelas e relações.

# Módulo de Administração
from .administration.role_model import Role, Permission, role_permissions
from .administration.user_model import Usuario, PasswordResetToken

# Módulo de Compras
from .purchasing.supplier_model import Fornecedor
# (Nota: Faltava OrdemDeCompra no seu ficheiro, mas estava no seu histórico - adicionei)
from .purchasing.purchase_order_model import OrdemDeCompra, OrdemDeCompraLinha

# Módulo de Inventário
from .inventory.udm_model import CategoriaUdm, Udm
from .inventory.product_model import CategoriaProduto, Produto, VarianteProduto
from .inventory.lot_model import Lote
from .inventory.location_model import TipoLocal, Local
from .inventory.transfer_type_model import TipoTransferencia
from .inventory.transfer_model import Transferencia
from .inventory.stock_movement_model import MovimentacaoLivroRazao
from .inventory.stock_count_model import ContagemInventario, ContagemInventarioLinha
from .inventory.brand_model import Marca

# Módulo de Produção
from .production.operation_type_model import TipoOperacao
from .production.work_center_model import CentroTrabalho
from .production.bom_model import Bom, BomComponente
from .production.production_order_model import OrdemProducao

# --- Módulo de Manutenção (CMMS) - VERSÃO COMPLETA ---

# Domínio 1: Pessoas
from .maintenance.maintenance_team_model import MaintenanceTeam
from .maintenance.technician_model import Technician

# Domínio 2: Ativos
from .maintenance.manufacturer_model import Manufacturer
from .maintenance.asset_model import Asset
from .maintenance.asset_spare_parts_model import AssetSparePart
from .maintenance.asset_meter_model import AssetMeter, AssetMeterReading
from .maintenance.asset_failure_mode_model import (
    MaintenanceFailureSymptom,
    MaintenanceFailureMode,
    MaintenanceFailureCause
)

# Domínio 3: Ordens de Serviço (Work Orders)
from .maintenance.work_order_model import (
    WorkOrder,
    wo_failure_symptoms_association,
    wo_failure_modes_association,
    wo_failure_causes_association
)
from .maintenance.work_order_labor_log_model import WorkOrderLaborLog
from .maintenance.work_order_parts_model import WorkOrderPartUsage
from .maintenance.work_order_task_model import WorkOrderTask
from .maintenance.work_order_log_model import WorkOrderLog

# Domínio 4: Manutenção Preventiva (PMs)
from .maintenance.pm_plan_model import PMPlan
from .maintenance.pm_task_list_model import PMTask
from .maintenance.pm_parts_list_model import PMRequiredPart

# --- FIM DAS IMPORTAÇÕES ---