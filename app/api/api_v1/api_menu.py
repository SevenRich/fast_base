# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, RoleModel
from ...core.schemes import request, response
from ...core import crud
from ...config import settings


router = APIRouter()


@router.get(
    '/menus', 
    summary='菜单列表'
)
def index(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    pass


@router.post(
    '/menus', 
    summary='创建菜单标识', 
)
def store(
    *,
    identities: Optional[List[int]] = Query(..., ge=1),
    form_data: dict = Depends(request.MenuRequest),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    return {'form_data':form_data, 'identities':identities}
