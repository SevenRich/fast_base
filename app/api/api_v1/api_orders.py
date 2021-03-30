# _*_ coding:utf-8 _*_

from datetime import timedelta
from typing import Any, List

from fastapi import (
    APIRouter, Body, Depends, HTTPException, Response, BackgroundTasks
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...utils import deps, security, common
from ...utils.common import (
    common_parameters
)
from ...models import UserModel, CodeOrderModel
from ...core.schemes import request, response
from ...core import crud
from ...core.jobs import code
from ...config import settings


router = APIRouter()


@router.get(
    '/orders', 
    response_model=List[response.Order], 
    summary='生码订单列表'
)
def index(
    commons: dict = Depends(common_parameters),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    生码订单列表 - ID 降序
    """
    orders = db.query(CodeOrderModel).order_by(desc('id'))[commons['skip'] : commons['skip'] + commons['limit']]
    
    return orders


@router.post(
    '/orders', 
    summary='创建生码订单', 
    # response_model=response.Order
)
def store(
    form_data: response.OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建生码订单

    生码批次规则：
    <pre>
    a00000 => 10485760 ffffff => 16777215 == 批次量 6291455  [默认6位批次码]
    </pre>
    
    relevance_type 关联 before 1 前关联 after 2 后关联 <br/>
    code_type 码类型 standard 1 标准码 group 2 套标 <br/>
    status 生码状态 wait 0 等待 begin 1 开始 done 2 完成 cancel 3 取消 fail 4 失败
    """
    
    obj = crud.order.create(db, obj_in=form_data)
    background_tasks.add_task(code.generator_standard_code, obj)
    return obj


@router.get(
    '/orders/{order_id}', 
    summary='生码订单详情', 
    response_model=response.Equipment
)
def show(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    obj_info = crud.equipment.get(db, id=order_id)
    if obj_info is None:
        raise HTTPException(400, 'Not Found!')
    return obj_info


@router.put(
    '/orders/{order_id}', 
    summary='更新生码订单', 
    response_model=response.Equipment
)
def update(
    order_id: int,
    form_data: request.EquipmentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_Equipment = crud.equipment.get(db, id=order_id)
    if existing_Equipment is None:
        raise HTTPException(400, 'Not Found!')
    
    return crud.equipment.update(db, db_obj=existing_Equipment, obj_in=form_data)


@router.delete(
    '/orders/{order_id}', 
    status_code=204,
    response_class=Response,
    summary='删除生码订单'
)
def delete(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
) -> Any:
    existing_info = crud.equipment.get(db, id=order_id)
    if existing_info is not None:
        crud.equipment.remove(db, id=order_id)
    return 