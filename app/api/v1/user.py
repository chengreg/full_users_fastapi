#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:00 
@Desc    ：
"""
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.mysql_db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, check_existence
from app.core.deps import get_current_user


# 创建user路由
user_router = APIRouter(prefix="/user", tags=["用户管理"])


@user_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="用户注册")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db=db, user_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@user_router.get("/check-existence/", response_model=dict, summary="检查用户名、邮箱、手机号+国际号码是否存在")
def check_user_existence(username: str = None, email: str = None, phone_number: str = None, country_code: str = None, db: Session = Depends(get_db)):
    existence = check_existence(db, username=username, email=email, phone_number=phone_number, country_code=country_code)
    return existence


@user_router.get("/users/me", summary="获取当前用户信息")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user