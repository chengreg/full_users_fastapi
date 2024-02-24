#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 02:07 
@Desc    ：
"""
from typing import Optional

from sqlmodel import Field

from app.models.base_model import Base
from app.models.user.user_enum import GenderEnum
from datetime import date


class UserProfile(Base, table=True):
    """ 用户资料模型 """
    __tablename__ = "user_profiles"

    user_id: str = Field(description="关联的用户ID", foreign_key="users.id")
    avatar_url: Optional[str] = Field(description="用户头像URL")
    nickname: Optional[str] = Field(max_length=50, description="用户昵称")
    gender: Optional[GenderEnum] = Field(default=GenderEnum.UNDISCLOSED, description="用户性别")
    country: Optional[str] = Field(max_length=100, description="用户所在国家")
    province: Optional[str] = Field(max_length=100, description="用户所在省份")
    city: Optional[str] = Field(max_length=100, description="用户所在城市")
    birth_date: Optional[date] = Field(default=None, description="出生日期")
    bio: Optional[str] = Field(max_length=255, description="用户简介")
    custom_status: Optional[str] = Field(max_length=255, description="用户定义的状态")
