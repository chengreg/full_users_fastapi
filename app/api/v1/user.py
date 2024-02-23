#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:00 
@Desc    ：
"""
from fastapi import APIRouter, Body
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.mysql_db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UpdateUserProfileModel
from app.crud.user import create_user, check_existence, update_user, update_user_profile
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


@user_router.get("/me", summary="获取当前用户信息")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@user_router.put("/user/profile", summary="更新用户信息")
async def update_user_profile_route(
    update_model: UpdateUserProfileModel = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    user_update_data = update_model.dict(exclude={"nickname", "gender", "location"}, exclude_unset=True)
    profile_update_data = update_model.dict(include={"nickname", "gender", "location"}, exclude_unset=True)

    try:
        if user_update_data:
            update_user(db, user_id, user_update_data)
        if profile_update_data:
            update_user_profile(db, user_id, profile_update_data)
    except HTTPException as e:
        return {"detail": e.detail}, e.status_code

    return {"message": "User and profile updated successfully."}