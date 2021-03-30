from fastapi import APIRouter

from .api_v1 import (
    api_default, 
    api_login, 
    api_users,
    api_roles,
    api_identities,
    api_menu,
    api_equipments,
    api_companies,
    api_orders
)

api_v1_router = APIRouter()
# 默认路由
api_v1_router.include_router(api_default.router, tags=["Default"])
# v1 login
api_v1_router.include_router(api_login.router, tags=["Login"])
# v1 Users
api_v1_router.include_router(api_users.router, tags=["Users"])
# v1 Roles
api_v1_router.include_router(api_roles.router, tags=["Roles"])
# v1 Identities
api_v1_router.include_router(api_identities.router, tags=["Identities"])
# v1 Menus
api_v1_router.include_router(api_menu.router, tags=["Menus"])
# v1 Equipments
api_v1_router.include_router(api_equipments.router, tags=["Equipments"])
# v1 Companies
api_v1_router.include_router(api_companies.router, tags=["Companies"])
# v1 Orders
api_v1_router.include_router(api_orders.router, tags=["Orders"])

