#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 01:52 
@Desc    ：
"""
from typing import Optional
from sqlalchemy import UniqueConstraint
from sqlmodel import Field
from app.models.user.user_enum import UsersStatusEnum
from app.models.base_model import Base


class User(Base, table=True):
    """ 用户模型 """
    __tablename__ = "users"

    username: Optional[str] = Field(index=True, unique=True, min_length=6, max_length=50, description="用户名")
    email: Optional[str] = Field(index=True, unique=True, description="邮箱")
    phone_number: Optional[str] = Field(index=True, min_length=1, max_length=20, description="手机号码")
    country_code: Optional[str] = Field(index=True, min_length=1, max_length=4, description="国际区号")
    hashed_password: Optional[str] = Field(description="哈希密码")
    status: UsersStatusEnum = Field(default=UsersStatusEnum.ACTIVE, index=True, nullable=False, description="状态")
    __table_args__ = (UniqueConstraint('country_code', 'phone_number', name='uq_countrycode_phonenumber'),)
