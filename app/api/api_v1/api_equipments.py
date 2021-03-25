# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List

from fastapi import (
    APIRouter, Body, Depends, HTTPException
)
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, EquipmentModel
from ...core.schemes import request, response
from ...core import crud
from ...config import settings


router = APIRouter()


@router.get(
    '/equipments', 
    response_model=List[response.Equipment], 
    summary='设备列表'
)
def index(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    设备列表 - ID 降序
    """
    equipments = db.query(EquipmentModel).order_by(desc('id'))[commons['skip'] : commons['skip'] + commons['limit']]
    
    return equipments


@router.post(
    '/equipments', 
    summary='创建设备', 
    response_model=response.Equipment
)
def store(
    form_data: dict = Depends(request.EquipmentCreate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建设备
    """
    existing_code = crud.equipment.get_by_code(db, code=form_data.equipment_code)
    if existing_code is not None:
        raise HTTPException(400, 'Equipment code is exist')
    existing_name = crud.equipment.get_by_name(db, name=form_data.equipment_name)
    if existing_name is not None:
        raise HTTPException(400, 'Equipment name is exist')
    
    return crud.equipment.create(db, obj_in=form_data)


@router.get(
    '/equipments/{equipment_id}', 
    summary='设备详情', 
    response_model=response.Equipment
)
def show(
    equipment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    obj_info = crud.equipment.get(db, id=equipment_id)
    if obj_info is None:
        raise HTTPException(400, 'Not Found!')
    return obj_info


@router.put(
    '/equipments/{equipment_id}', 
    summary='更新设备', 
    response_model=response.Equipment
)
def update(
    equipment_id: int,
    form_data: dict = Depends(request.EquipmentUpdate),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_Equipment = crud.equipment.get(db, id=equipment_id)
    if existing_Equipment is None:
        raise HTTPException(400, 'Not Found!')
    
    return crud.equipment.update(db, db_obj=existing_Equipment, obj_in=form_data)


@router.delete(
    '/equipments/{equipment_id}', 
    status_code=204, 
    summary='删除设备'
)
def delete(
    equipment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_info = crud.equipment.get(db, id=equipment_id)
    if existing_info is not None:
        crud.equipment.remove(db, id=equipment_id)
    