#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:42 
@Desc    ：
"""

import uuid
from enum import Enum as pyEnum
from sqlalchemy import Enum as saEnum, Column, UniqueConstraint, String
from sqlmodel import SQLModel, Field
from typing import Optional
from .timestamps import Timestamps


class UsersStatusEnum(str, pyEnum):
    ACTIVE = "A"  # 活跃状态，表示用户或对象处于活跃状态，通常表示用户可以正常使用平台或功能。
    INACTIVE = "I"  # 非活跃状态，表示用户或对象处于非活跃状态，通常表示用户暂时无法使用平台或功能。
    DELETED = "D"  # 用户已删除，该用户信息将从系统中删除，不再可用。
    BLOCKED = "B"  # 被封禁状态，表示用户或对象的访问或权限已被系统管理员或监管机构暂时封禁，通常是因为违反了规则或政策
    LOCKED = "L"  # 已锁定状态，可能是指用户账户被临时锁定，通常需要解锁后才能继续使用。
    PENDING = "P"  # 待处理状态，通常用于表示用户或对象处于等待某种处理、验证或激活的状态。


class User(SQLModel, Timestamps, table=True):
    __tablename__ = "users"

    id: str = Field(sa_column=Column("id", String(length=128), primary_key=True, unique=True, index=True, comment="ID"))
    username: Optional[str] = Field(index=True, unique=True, min_length=6, max_length=50, description="用户名")
    email: Optional[str] = Field(index=True, unique=True, description="邮箱")
    phone_number: Optional[str] = Field(min_length=1, max_length=20, description="手机号码")
    country_code: Optional[str] = Field(min_length=1, max_length=4, description="国际区号")
    hashed_password: Optional[str] = Field(description="哈希密码")
    status: UsersStatusEnum = Field(default=UsersStatusEnum.ACTIVE,
                                    sa_column=Column("status", saEnum(UsersStatusEnum), nullable=False,
                                                     comment="用户状态"))

    # UniqueConstraint确保同一个国家代码和电话号码的组合是唯一的
    __table_args__ = (UniqueConstraint('country_code', 'phone_number', name='uq_countrycode_phonenumber'),)


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    id: Optional[int] = Field(default=None, primary_key=True, description="ID")
    user_id: Optional[uuid.UUID] = Field(description="关联的用户UUID")
    nickname: Optional[str] = Field(max_length=50, description="用户昵称")
    gender: Optional[str] = Field(description="用户性别")
    location: Optional[str] = Field(description="用户所在地")

    # 设置外键关联
    user_id: str = Field(description="关联的用户ID", foreign_key="users.id")
