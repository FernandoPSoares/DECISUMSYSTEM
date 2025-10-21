# backend/app/modules/api_router.py

from fastapi import APIRouter

# Importa os routers de cada um dos nossos módulos funcionais
from .auth.auth_router import router as auth_router
from .administration.users.users_router import router as users_router
from .administration.roles.roles_router import router_roles, router_permissions
from .purchasing.suppliers.suppliers_router import router as suppliers_router
from .production.work_centers.work_centers_router import router as work_centers_router
from .inventory.locations.locations_router import router_locais, router_tipos_local
from .inventory.products.products_router import router_categorias_udm, router_udm, router_categorias_produto
from .inventory.brands.brands_router import router as brands_router 

# Cria o nosso router de agregação principal
api_router = APIRouter()

# Inclui todos os routers importados no router principal
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(suppliers_router)
api_router.include_router(work_centers_router)
api_router.include_router(router_roles)
api_router.include_router(router_permissions)
api_router.include_router(router_tipos_local)
api_router.include_router(router_locais)
api_router.include_router(router_categorias_udm)
api_router.include_router(router_udm)
api_router.include_router(router_categorias_produto)
api_router.include_router(brands_router) 
