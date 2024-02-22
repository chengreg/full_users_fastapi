#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 02:14 
@Desc    ：
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token

from datetime import timedelta

auth_router = APIRouter(prefix="/auth", tags=["认证管理"])


@auth_router.post("/token", summary="获取token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 这里应该验证用户名和密码
    # 暂时假设任何用户都是有效的
    user = {"username": form_data.username}
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



