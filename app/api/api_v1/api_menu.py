# _*_ coding:utf-8 _*_

from app.models.menu import Menu
from datetime import timedelta
from typing import Any, List, Optional, Union

from fastapi import (
    APIRouter, Body, Depends, HTTPException, Query
)
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, MenuModel
from ...core.schemes import request, response
from ...core import crud
from ...config import settings


router = APIRouter()


@router.get(
    '/menus', 
    summary='菜单列表',
    response_model=List[response.Menu]
)
def index(
    *,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    菜单列表 - 树状列表 目前最多两层
    """
    menus = db.query(MenuModel).filter_by(parent_id=None)
    menus_dict = []
    for menu in menus:
        menu.children
        menus_dict.append(menu)
    return menus_dict


@router.post(
    '/menus', 
    summary='创建菜单标识', 
    response_model=response.Menu
)
def store(
    *,
    identity_ids: Optional[List[int]] = Query(..., ge=1),
    form_data: dict = Depends(request.MenuRequest),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing = crud.menu.get_by_name(db, name=form_data.name)
    if existing is not None:
        raise HTTPException(400, 'Menu name is exist')
    create_info = crud.menu.create(db, obj_in=form_data)
    # 分配权限
    [create_info.identity.append(crud.identity.get(db, id=identity_id)) for identity_id in identity_ids]
    db.commit()
    return crud.menu.get_by_name(db, name=form_data.name)


@router.get(
    '/menus/{menu_id}', 
    summary='菜单详情', 
    response_model=response.Menu
)
def show(
    menu_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    obj_info = crud.menu.get(db, id=menu_id)
    if obj_info is None:
        raise HTTPException(400, 'Not Found!')
    return obj_info



@router.put(
    '/menus/{menu_id}', 
    summary='更新菜单', 
    response_model=response.Menu
)
def update(
    menu_id: int,
    form_data: dict = Depends(request.RoleUpdate),
    identity_ids: Optional[List[int]] = Query(..., ge=1),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    更新菜单信息，并删除旧权限，重新分配新权限
    """
    existing_info = crud.menu.get(db, id=menu_id)
    if existing_info is None:
        raise HTTPException(400, 'Role Not Found!')
    existing = crud.menu.get_by_name(db, name=form_data.name)
    if existing is not None and existing.id != existing_info.id:
        raise HTTPException(400, 'Menu name is exist')
    obj_info = crud.menu.update(db, db_obj=existing_info, obj_in=form_data)
    # 清空旧权限
    [obj_info.identity.remove(menu_identity) for menu_identity in obj_info.identity]
    # 分配权限
    [obj_info.identity.append(crud.identity.get(db, id=identity_id)) for identity_id in identity_ids]
    db.commit()
    return crud.menu.get(db, id=menu_id)


@router.delete(
    '/menus/{menu_id}', 
    status_code=204, 
    summary='删除菜单'
)
def delete(
    menu_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    删除菜单
    """
    existing_info = crud.menu.get(db, id=menu_id)
    if existing_info is not None:
        crud.menu.remove(db, id=menu_id)
    
