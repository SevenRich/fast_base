from fastapi import APIRouter

from .api_v1 import (
    default, 
    login, 
    users,
    roles,
    identities
)

api_v1_router = APIRouter()
# 默认路由
api_v1_router.include_router(default.router, tags=["Default"])
# v1 login
api_v1_router.include_router(login.router, prefix="/api/v1", tags=["Login"])
# v1 Users
api_v1_router.include_router(users.router, prefix="/api/v1", tags=["Users"])
# v1 Roles
api_v1_router.include_router(roles.router, prefix="/api/v1", tags=["Roles"])
# v1 Identities
api_v1_router.include_router(identities.router, prefix="/api/v1", tags=["Identities"])
# v1 Menus

