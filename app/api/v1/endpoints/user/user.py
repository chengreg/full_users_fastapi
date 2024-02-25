#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:00 
@Desc    ：
"""
from datetime import timedelta
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from starlette import status

from app.core.config import settings
from app.models.user import User
from app.crud.user.user import UserCRUD
from app.db.postgresql_db import engine
from app.schemas.user import UpdateUserSchema, UserCreateByEmailSchema, UserCreateByPhoneSchema, TokenResponseSchema
from app.crud.auth import create_access_token
from app.core.security import get_password_hash
from app.api.deps import get_current_user
from app.schemas.form_models import OAuth2PasswordRequestFormEmail, OAuth2PasswordRequestFormPhone
from app.services.authentication_service import generate_token_response

# 创建user路由
user_router = APIRouter(prefix="/user", tags=["用户管理"])

# 创建异步session
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
db = UserCRUD(User)


@user_router.post("/register_by_phone", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED,
                  summary="手机号注册")
async def register_by_phone(userIn: UserCreateByPhoneSchema):
    if userIn.phone_number and userIn.country_code:
        """处理手机号码注册逻辑"""
        if await db.get_by_phone_number(async_session, userIn.phone_number, userIn.country_code):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    # 验证手机验证码
    # if not await verify_sms_code(userIn.phone_number, userIn.sms_code):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")

    # 创建用户
    new_user = User(
        id=str(uuid4()),
        phone_number=userIn.phone_number,
        country_code=userIn.country_code,
        hashed_password=get_password_hash(userIn.password)
    )
    user = await db.create_user(async_session, new_user)

    return await generate_token_response(user.country_code+"_"+user.phone_number)


@user_router.post("/register_by_email", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED,
                  summary="邮箱地址注册")
async def register_by_email(userIn: UserCreateByEmailSchema):
    """邮箱注册"""
    # 验证邮箱是否存在
    if userIn.email:
        if await db.get_by_email(async_session, userIn.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    # 创建用户
    new_user = User(
        id=str(uuid4()),
        email=userIn.email,
        hashed_password=get_password_hash(userIn.password)
    )
    user = await db.create_user(async_session, new_user)

    return await generate_token_response(user.email)


@user_router.post("/login_by_email", response_model=TokenResponseSchema, summary="邮箱地址登录")
async def login_by_email(form_data: OAuth2PasswordRequestFormEmail = Depends()):
    # 尝试使用用户名、邮箱或手机号码登录
    user = await db.authenticate_user_by_email(async_session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await generate_token_response(user.email)


@user_router.post("/login_by_phone", response_model=TokenResponseSchema, summary="手机号登录")
async def login_by_phone(form_data: OAuth2PasswordRequestFormPhone = Depends()):
    """ 手机号码登录 """
    # check user
    user = await db.authenticate_user_by_phone_number(async_session, form_data.phone_number, form_data.country_code,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await generate_token_response(user.country_code+"_"+user.phone_number)


@user_router.get("/me", summary="获取当前用户信息")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@user_router.patch("/profile", summary="更新用户信息")
async def update_user_profile_route(
        update_model: UpdateUserSchema = Body(...),
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
            await db.update_user(async_session, user_id, user_update_data)
        if profile_update_data:
            # 更新UserProfile相关信息
            await db.update_user_profile(async_session, user_id, profile_update_data)
    except HTTPException as e:
        raise e

    return {"message": "User and profile updated successfully."}

# @user_router.patch("/profile", summary="更新用户信息")
# async def update_user_profile_route(
#         update_model: UpdateUserProfileModel = Body(...),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     user_id = current_user.id
#     # 由于nickname, avatar_url, gender, country, province, city, birth_date, bio, custom_status是UserProfile的字段，需要从user_update_data中排除
#     user_update_data = update_model.dict(
#         exclude={"nickname", "avatar_url", "gender", "country", "province", "city", "birth_date", "bio",
#                  "custom_status"}, exclude_unset=True)
#     # 包含UserProfile的字段
#     profile_update_data = update_model.dict(
#         include={"nickname", "avatar_url", "gender", "country", "province", "city", "birth_date", "bio",
#                  "custom_status"}, exclude_unset=True)
#
#     try:
#         if user_update_data:
#             # 更新User相关信息
#             update_user(db, user_id, user_update_data)
#         if profile_update_data:
#             # 更新UserProfile相关信息
#             update_user_profile(db, user_id, profile_update_data)
#     except HTTPException as e:
#         raise e
#
#     return {"message": "User and profile updated successfully."}

#
#
# @user_router.put("/password", summary="更新用户密码")
# def update_password(password_update: PasswordUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if not verify_password(password_update.old_password, current_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect password")
#
#     success = update_user_password(db, current_user.id, password_update.new_password)
#     if not success:
#         raise HTTPException(status_code=500, detail="Password update failed")
#
#     return {"message": "Password updated successfully"}
#
#
# @user_router.get("/check-existence/", response_model=dict, summary="检查用户名、邮箱、手机号+国际号码是否存在")
# def check_user_existence(username: str = None, email: str = None, phone_number: str = None, country_code: str = None,
#                          db: Session = Depends(get_db)):
#     existence = check_existence(db, username=username, email=email, phone_number=phone_number,
#                                 country_code=country_code)
#     return existence
#
#

#
#
# @user_router.patch("/profile", summary="更新用户信息")
# async def update_user_profile_route(
#         update_model: UpdateUserProfileModel = Body(...),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     user_id = current_user.id
#     # 由于nickname, avatar_url, gender, country, province, city, birth_date, bio, custom_status是UserProfile的字段，需要从user_update_data中排除
#     user_update_data = update_model.dict(
#         exclude={"nickname", "avatar_url", "gender", "country", "province", "city", "birth_date", "bio",
#                  "custom_status"}, exclude_unset=True)
#     # 包含UserProfile的字段
#     profile_update_data = update_model.dict(
#         include={"nickname", "avatar_url", "gender", "country", "province", "city", "birth_date", "bio",
#                  "custom_status"}, exclude_unset=True)
#
#     try:
#         if user_update_data:
#             # 更新User相关信息
#             update_user(db, user_id, user_update_data)
#         if profile_update_data:
#             # 更新UserProfile相关信息
#             update_user_profile(db, user_id, profile_update_data)
#     except HTTPException as e:
#         raise e
#
#     return {"message": "User and profile updated successfully."}
#
#
# @user_router.get("/status", response_model=UsersStatusEnum, summary="获取用户状态")
# def read_user_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return current_user.status
#
#
# @user_router.patch("/status", response_model=User, summary="修改用户状态")
# def change_user_status(status: UsersStatusEnum, current_user: User = Depends(get_current_user),
#                        db: Session = Depends(get_db)):
#     return update_user_status(db, current_user.id, status)
#
#
# @user_router.post("/deactivate", response_model=User, summary="注销用户")
# async def deactivate_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     if not current_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     # 更新用户状态为DELETED
#     update_user_status(db, current_user.id, UsersStatusEnum.DELETED)
#     return {"message": "注销成功"}
