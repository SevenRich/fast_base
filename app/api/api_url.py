from fastapi import APIRouter

from .api_v1 import (
    api_default as api_v1_default, 
    api_login as api_v1_login, 
    api_users as api_v1_users,
    api_roles as api_v1_roles,
    api_identities as api_v1_identities,
    api_menu as api_v1_menu,
    api_equipments as api_v1_equipments
)

api_v1_router = APIRouter()
# 默认路由
api_v1_router.include_router(api_v1_default.router, tags=["Default"])
# v1 login
api_v1_router.include_router(api_v1_login.router, tags=["Login"])
# v1 Users
api_v1_router.include_router(api_v1_users.router, tags=["Users"])
# v1 Roles
api_v1_router.include_router(api_v1_roles.router, tags=["Roles"])
# v1 Identities
api_v1_router.include_router(api_v1_identities.router, tags=["Identities"])
# v1 Menus
api_v1_router.include_router(api_v1_menu.router, tags=["Menus"])
# v1 Equipments
api_v1_router.include_router(api_v1_equipments.router, tags=["Equipments"])
