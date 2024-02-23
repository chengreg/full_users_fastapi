#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:50 
@Desc    ：
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ..models.user import UsersStatusEnum, GenderEnum
import datetime


class UserCreate(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="电子邮件")
    phone_number: Optional[str] = Field(None, min_length=1, max_length=20, description="手机号码")
    country_code: Optional[str] = Field(None, min_length=1, max_length=4, description="国际区号")
    password: Optional[str] = Field(None, min_length=6, max_length=20, description="密码")


class UserResponse(BaseModel):
    id: str
    username: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    country_code: Optional[str]
    status: UsersStatusEnum

class RegisterRequest(BaseModel):
    username: Optional[str] = Field(None, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    phone_number: Optional[str] = Field(None, description="手机号码")
    country_code: Optional[str] = Field(None, description="国际区号")
    password: str


class UpdateUserProfileModel(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, min_length=1, max_length=20)
    country_code: Optional[str] = Field(None, min_length=1, max_length=4)
    # UserProfile相关字段
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[GenderEnum] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = Field(description="用户所在城市")
    birth_date: Optional[datetime.date] = Field(default=None, description="出生日期")
    bio: Optional[str] = Field(max_length=255, description="用户简介")
    custom_status: Optional[str] = Field(max_length=255, description="用户定义的状态")
