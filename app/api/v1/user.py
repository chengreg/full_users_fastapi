#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:00 
@Desc    ：
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.core.mysql_db import get_db
from app.crud.auth import create_access_token
from app.models.user import User, UsersStatusEnum
from app.schemas.user import RegisterRequest, UserResponse, UpdateUserProfileModel
from app.crud.user import get_user_by_username, check_existence, update_user, update_user_profile, authenticate_user, \
    update_user_status, get_user_by_email, get_user_by_phone, create_user
from app.core.deps import get_current_user
from app.core.config import settings

# 创建user路由
user_router = APIRouter(prefix="/user", tags=["用户管理"])


@user_router.post("/register", status_code=status.HTTP_201_CREATED, summary="用户注册")
async def register(userIn: RegisterRequest, db: Session = Depends(get_db)):
    if userIn.username:
        """处理用户名注册逻辑"""
        # 判断用户名是否已存在
        if get_user_by_username(db, userIn.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    elif userIn.email:
        """处理邮箱注册逻辑"""
        if get_user_by_email(db, userIn.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    elif userIn.phone_number and userIn.country_code:
        """处理手机号码注册逻辑"""
        if get_user_by_phone(db, userIn.phone_number, userIn.country_code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    # 创建用户
    user = create_user(db, userIn)

    # 创建jwt token
    # 生成access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username},  # 使用用户名作为subject
        expires_delta=access_token_expires
    )

    # 返回token和其他信息
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds(),
    }




@user_router.post("/login", summary="用户登录")
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    # 尝试使用用户名、邮箱或手机号码登录
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username},  # 使用用户名作为subject
        expires_delta=access_token_expires
    )

    # 返回token和其他信息
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds(),
    }


@user_router.get("/check-existence/", response_model=dict, summary="检查用户名、邮箱、手机号+国际号码是否存在")
def check_user_existence(username: str = None, email: str = None, phone_number: str = None, country_code: str = None,
                         db: Session = Depends(get_db)):
    existence = check_existence(db, username=username, email=email, phone_number=phone_number,
                                country_code=country_code)
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
    # 由于nickname, avatar_url, gender, country, province, city, birth_date, bio, custom_status是UserProfile的字段，需要从user_update_data中排除
    user_update_data = update_model.dict(
        exclude={"nickname", "avatar_url", "gender", "country", "province", "city", "birth_date", "bio",
                 "custom_status"}, exclude_unset=True)
    # 包含UserProfile的字段
    profile_update_data = update_model.dict(
        include={"nickname", "avatar_url", "gender", "country", "province", "city", "birth_date", "bio",
                 "custom_status"}, exclude_unset=True)

    try:
        if user_update_data:
            # 更新User相关信息
            update_user(db, user_id, user_update_data)
        if profile_update_data:
            # 更新UserProfile相关信息
            update_user_profile(db, user_id, profile_update_data)
    except HTTPException as e:
        raise e

    return {"message": "User and profile updated successfully."}


@user_router.get("/user/status", response_model=UsersStatusEnum)
def read_user_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.status


@user_router.patch("/user/status", response_model=User)
def change_user_status(status: UsersStatusEnum, current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return update_user_status(db, current_user.id, status)


@user_router.post("/user/deactivate", response_model=User)
async def deactivate_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # 更新用户状态为DELETED
    update_user_status(db, current_user.id, UsersStatusEnum.DELETED)
    return {"message": "注销成功"}
