# File: backend/app/modules/maintenance/router.py
from fastapi import APIRouter

# Importa os routers das "fatias" (slices)
from .teams.teams_router import router as teams_router
from .technicians.technicians_router import router as technicians_router
# --- NOVA IMPORTAÇÃO (Fatia 3: Fabricantes) ---
from .manufacturers.manufacturers_router import router as manufacturers_router
# --- FIM DA NOVA IMPORTAÇÃO ---


# Router principal do módulo de Manutenção
maintenance_router = APIRouter()

# Agrega as "fatias" (slices) do módulo de Manutenção
maintenance_router.include_router(teams_router)
maintenance_router.include_router(technicians_router)
# --- NOVA INCLUSÃO (Fatia 3: Fabricantes) ---
maintenance_router.include_router(manufacturers_router)
# --- FIM DA NOVA INCLUSÃO ---

# (Próximos passos incluirão: assets_router, work_orders_router, etc.)