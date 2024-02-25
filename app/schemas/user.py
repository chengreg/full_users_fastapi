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
    """ 通过电子邮件注册用户的Schema """
    email: Optional[EmailStr] = Field(None, description="电子邮件")
    password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码", example="yourpassword")


class UserCreateByUsernameSchema(BaseModel):
    """ 通过用户名注册用户的Schema """
    username: Optional[str] = Field(None, description="用户名", example="yourusername")
    password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码", example="yourpassword")


class UserCreateByPhoneSchema(BaseModel):
    """ 通过手机号码注册用户的Schema """
    country_code: Optional[str] = Field(None, min_length=1, max_length=4, description="国际区号", example="+86")
    phone_number: Optional[str] = Field(None, min_length=1, max_length=20, description="手机号码",
                                        example="13800000000")
    password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码", example="yourpassword")
    # 验证码
    sms_code: Optional[str] = Field(None, min_length=6, max_length=6, description="验证码", example="123456")


class TokenResponseSchema(BaseModel):
    """ Token响应Schema """
    access_token: str
    token_type: str
    expires_in: float


class UpdateUserSchema(BaseModel):
    """ 更新用户信息的Schema """
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


