#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 03:21 
@Desc    ：
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from fastapi.encoders import jsonable_encoder

from app.core.deps import get_current_user
from app.core.mysql_db import get_db
from app.crud.secret_key import create_secret_key, get_user_secret_keys
from app.models.secret_key import SecretKey
from app.models.user import User
from app.schemas.secret_key import SecretKeyCreate
from typing import List
from app.core.utils import hide_secret_key

secret_key_router = APIRouter(prefix="/secret_key", tags=["Secret Keys管理"])


@secret_key_router.post("/secret-keys/", response_model=SecretKey, summary="创建Secret Key",
                        status_code=status.HTTP_201_CREATED, )
def create_secret_key_api(
        secret_key_data: SecretKeyCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 将Pydantic模型转换为字典，排除未设置的字段
    secret_key_data_dict = secret_key_data.dict(exclude_unset=True)
    secret_key_instance = create_secret_key(db=db, secret_key_data=secret_key_data_dict, user_id=current_user.id)
    return secret_key_instance


@secret_key_router.get("/get_user_secret-keys/", response_model=List[SecretKey], summary="获取用户所有的Secret Keys")
def read_user_secret_keys(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    secret_keys = get_user_secret_keys(db, user_id=current_user.id)
    # 修改secret_keys中的每个secret_key值, 隐藏secret_key的中间的值
    for secret_key in secret_keys:
        secret_key.secret_key = hide_secret_key(secret_key.secret_key)
    # 确保响应是可json化的
    return jsonable_encoder(secret_keys)
