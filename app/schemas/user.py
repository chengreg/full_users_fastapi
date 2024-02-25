#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:50 
@Desc    ：
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from ..models.user import UsersStatusEnum, GenderEnum
import datetime


class UserCreateByEmailSchema(BaseModel):
    email: Optional[EmailStr] = Field(None, description="电子邮件")
    password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码", example="yourpassword")


class UserCreateByPhoneSchema(BaseModel):
    country_code: Optional[str] = Field(None, min_length=1, max_length=4, description="国际区号", example="+86")
    phone_number: Optional[str] = Field(None, min_length=1, max_length=20, description="手机号码", example="13800000000")
    password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码", example="yourpassword")
    # 验证码
    sms_code: Optional[str] = Field(None, min_length=6, max_length=6, description="验证码", example="123456")


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    expires_in: float


#
# class UserCreateSchema(BaseModel):
#     username: Optional[str] = Field(None, min_length=6, max_length=50, description="用户名")
#     email: Optional[EmailStr] = Field(None, description="电子邮件")
#     phone_number: Optional[str] = Field(None, min_length=1, max_length=20, description="手机号码")
#     country_code: Optional[str] = Field(None, min_length=1, max_length=4, description="国际区号")
#     password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码")
#
#
#
#
# class UserResponse(BaseModel):
#     id: str
#     username: Optional[str]
#     email: Optional[EmailStr]
#     phone_number: Optional[str]
#     country_code: Optional[str]
#     status: UsersStatusEnum
#
# class RegisterRequest(BaseModel):
#     username: Optional[str] = Field(None, description="用户名")
#     email: Optional[EmailStr] = Field(None, description="邮箱地址")
#     phone_number: Optional[str] = Field(None, description="手机号码")
#     country_code: Optional[str] = Field(None, description="国际区号")
#     password: str
#
#
class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=1, max_length=20)
    country_code: Optional[str] = Field(None, min_length=1, max_length=4)
    # UserProfile相关字段
    nickname: Optional[str] = Field(None, max_length=50)
    avatar_url: Optional[str] = None
    gender: Optional[GenderEnum] = None
    country: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[datetime.date] = None,
    bio: Optional[str] = Field(None, max_length=255)
    custom_status: Optional[str] = Field(None, max_length=255)
#
#
# class PasswordUpdateRequest(BaseModel):
#     old_password: str = Field(..., description="The current password of the user")
#     new_password: str = Field(..., min_length=8, description="The new password for the user")
#
#     @field_validator('new_password')
#     def password_strength(cls, value: str):
#         # 示例: 确保密码长度至少为6
#         if len(value) < 6:
#             raise ValueError('Password must be at least 6 characters long')
#         # 可以添加更多的密码强度验证逻辑
#         return value
