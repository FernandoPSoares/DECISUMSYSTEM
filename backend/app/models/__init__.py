# backend/app/models/__init__.py

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
from .purchasing.purchase_order_model import OrdemDeCompra

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

