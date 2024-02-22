#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:50 
@Desc    ：
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ..models.user import UsersStatusEnum


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
