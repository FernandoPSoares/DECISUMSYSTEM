# File: backend/app/modules/api_router.py

from fastapi import APIRouter

# --- Imports por Módulo ---

# Auth
from .auth.auth_router import router as auth_router

# Administration
from .administration.users.users_router import router as users_router
from .administration.roles.roles_router import router_roles, router_permissions

# Purchasing
from .purchasing.suppliers.suppliers_router import router as suppliers_router

# Production
from .production.work_centers.work_centers_router import router as work_centers_router

# Inventory (com a nova estrutura verticalizada)
from .inventory.locations.locations_router import router_locais, router_tipos_local
from .inventory.brands.brands_router import router as brands_router
from .inventory.udms.udms_router import router_categorias_udm, router_udm
from .inventory.product_categories.product_categories_router import router as product_categories_router
from .inventory.products.products_router import router as products_router

# --- NOVO: Módulo de Manutenção ---
from .maintenance.router import maintenance_router
# --- FIM DA ALTERAÇÃO ---


# Cria o router de agregação principal
api_router = APIRouter()

# --- Inclusão dos Routers por Módulo ---

# Módulo de Autenticação
api_router.include_router(auth_router)

# Módulo de Administração
api_router.include_router(users_router)
api_router.include_router(router_roles)
api_router.include_router(router_permissions)

# Módulo de Compras
api_router.include_router(suppliers_router)

# Módulo de Produção
api_router.include_router(work_centers_router)

# Módulo de Inventário
api_router.include_router(router_tipos_local)
api_router.include_router(router_locais)
api_router.include_router(brands_router)
api_router.include_router(router_categorias_udm)
api_router.include_router(router_udm)
api_router.include_router(product_categories_router)
api_router.include_router(products_router)

# --- NOVO: Módulo de Manutenção ---
# Adiciona todos os endpoints de manutenção sob o prefixo /maintenance
api_router.include_router(maintenance_router, prefix="/maintenance")
# --- FIM DA ALTERAÇÃO ---