# File: backend/app/modules/maintenance/router.py
from fastapi import APIRouter

# Importa os routers das "fatias" (slices)
from .teams.teams_router import router as teams_router
from .technicians.technicians_router import router as technicians_router
from .manufacturers.manufacturers_router import router as manufacturers_router
from .asset_categories.asset_categories_router import router as asset_categories_router
# --- NOVA IMPORTAÇÃO (Fatia 4: Ativos) ---
from .assets.assets_router import router as assets_router
from .work_orders.work_orders_router import router as work_orders_router
# --- FIM DA NOVA IMPORTAÇÃO ---
from .failure_analysis.failure_analysis_router import router as rca_router

# Router principal do módulo de Manutenção
maintenance_router = APIRouter()

# Agrega as "fatias" (slices) do módulo de Manutenção
maintenance_router.include_router(teams_router)
maintenance_router.include_router(technicians_router)
maintenance_router.include_router(manufacturers_router)
maintenance_router.include_router(asset_categories_router)
# --- NOVA INCLUSÃO (Fatia 4: Ativos) ---
maintenance_router.include_router(assets_router)
maintenance_router.include_router(work_orders_router)
# --- FIM DA NOVA INCLUSÃO ---
maintenance_router.include_router(rca_router)

# (Próximos passos incluirão: work_orders_router, pm_plans_router, etc.)