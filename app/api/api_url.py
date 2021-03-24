from fastapi import APIRouter

from .api_v1 import (
    default as api_v1_default, 
    login as api_v1_login, 
    api_users as api_v1_users,
    api_roles as api_v1_roles,
    identities as api_v1_identities,
    api_menu as api_v1_menu
)

api_v1_router = APIRouter()
# 默认路由
api_v1_router.include_router(api_v1_default.router, tags=["Default"])
# v1 login
api_v1_router.include_router(api_v1_login.router, prefix="/api/v1", tags=["Login"])
# v1 Users
api_v1_router.include_router(api_v1_users.router, prefix="/api/v1", tags=["Users"])
# v1 Roles
api_v1_router.include_router(api_v1_roles.router, prefix="/api/v1", tags=["Roles"])
# v1 Identities
api_v1_router.include_router(api_v1_identities.router, prefix="/api/v1", tags=["Identities"])
# v1 Menus
api_v1_router.include_router(api_v1_menu.router, prefix="/api/v1", tags=["Menus"])
