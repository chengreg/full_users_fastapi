#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:42 
@Desc    ：
"""

import uuid
import datetime
from enum import Enum as pyEnum
from sqlalchemy import Enum as saEnum, Column, UniqueConstraint, String
from sqlmodel import SQLModel, Field
from typing import Optional
from .timestamps import Timestamps


class UsersStatusEnum(str, pyEnum):
    """ 用户状态枚举 """
    ACTIVE = "A"  # 活跃状态，表示用户或对象处于活跃状态，通常表示用户可以正常使用平台或功能。
    INACTIVE = "I"  # 非活跃状态，表示用户或对象处于非活跃状态，通常表示用户暂时无法使用平台或功能。
    DELETED = "D"  # 用户已删除，该用户信息将从系统中删除，不再可用。
    BLOCKED = "B"  # 被封禁状态，表示用户或对象的访问或权限已被系统管理员或监管机构暂时封禁，通常是因为违反了规则或政策
    LOCKED = "L"  # 已锁定状态，可能是指用户账户被临时锁定，通常需要解锁后才能继续使用。
    PENDING = "P"  # 待处理状态，通常用于表示用户或对象处于等待某种处理、验证或激活的状态。


class GenderEnum(str, pyEnum):
    """ 性别 """
    MALE = "M"  # 男
    FEMALE = "F"  # 女
    UNDISCLOSED = "U"  # 未公开


class SocialAccountStatus(str, pyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNBOUND = "unbound"  # 表示社交账号已解绑


class User(Timestamps, table=True):
    """ 用户模型 """
    __tablename__ = "users"

    id: str = Field(sa_column=Column("id", String(length=128), primary_key=True, unique=True, index=True, comment="ID"))
    username: Optional[str] = Field(index=True, unique=True, min_length=6, max_length=50, description="用户名")
    email: Optional[str] = Field(index=True, unique=True, description="邮箱")
    phone_number: Optional[str] = Field(index=True, min_length=1, max_length=20, description="手机号码")
    country_code: Optional[str] = Field(index=True, min_length=1, max_length=4, description="国际区号")
    hashed_password: Optional[str] = Field(description="哈希密码")
    # status: Optional[UsersStatusEnum] = Field(default=UsersStatusEnum.ACTIVE,
    #                                 sa_column=Column("status", saEnum(UsersStatusEnum), nullable=False,
    #                                                  comment="用户状态"))
    status: UsersStatusEnum = Field(default=UsersStatusEnum.ACTIVE, index=True, nullable=False, description="状态")

    # UniqueConstraint确保同一个国家代码和电话号码的组合是唯一的
    __table_args__ = (UniqueConstraint('country_code', 'phone_number', name='uq_countrycode_phonenumber'),)


class UserProfile(Timestamps, table=True):
    """ 用户资料模型 """
    __tablename__ = "user_profiles"

    id: Optional[int] = Field(default=None, primary_key=True, description="ID")
    user_id: str = Field(description="关联的用户ID", foreign_key="users.id")
    avatar_url: Optional[str] = Field(description="用户头像URL")
    nickname: Optional[str] = Field(max_length=50, description="用户昵称")
    gender: Optional[GenderEnum] = Field(default=GenderEnum.UNDISCLOSED, description="用户性别")
    country: Optional[str] = Field(max_length=100, description="用户所在国家")
    province: Optional[str] = Field(max_length=100, description="用户所在省份")
    city: Optional[str] = Field(max_length=100, description="用户所在城市")
    birth_date: Optional[datetime.date] = Field(default=None, description="出生日期")
    bio: Optional[str] = Field(max_length=255, description="用户简介")
    custom_status: Optional[str] = Field(max_length=255, description="用户定义的状态")

#
# class SocialAccount(Timestamps, table=True):
#     """ 社交账号模型 """
#     __tablename__ = "social_accounts"
#
#     id: Optional[int] = Field(default=None, primary_key=True, description="ID")
#     user_id: str = Field(foreign_key="users.id", description="用户ID")
#     platform: str = Field(description="社交平台名称")
#     platform_user_id: str = Field(description="平台上的用户标识符")
#     access_token: Optional[str] = Field(description="访问令牌")
#     status: str = Field(sa_column=Column(String, default=SocialAccountStatus.ACTIVE), description="社交账号状态")
#
#     class Config:
#         arbitrary_types_allowed = True
#
#
# class SocialUserInfo(Timestamps, table=True):
#     """ 社交平台用户信息模型 """
#     __tablename__ = "social_user_info"
#
#     id: Optional[int] = Field(default=None, primary_key=True, description="ID")
#     social_account_id: str = Field(foreign_key="social_accounts.id", description="社交账号ID")
#     username: Optional[str] = Field(description="平台用户名")
#     avatar_url: Optional[str] = Field(description="用户头像URL")
#     profile_url: Optional[str] = Field(description="社交平台上的用户主页URL")
#     location: Optional[str] = Field(description="位置")
#     bio: Optional[str] = Field(description="个人简介")
#     full_name: Optional[str] = Field(description="全名")
#     email: Optional[str] = Field(description="邮箱")
#     followers_count: Optional[int] = Field(default=None, description="关注者数量")
#     following_count: Optional[int] = Field(default=None, description="关注的用户数量")
#     posts_count: Optional[int] = Field(default=None, description="帖子数量")
#     registration_date: Optional[datetime.date] = Field(default=None, description="注册日期")
#     status: str = Field(sa_column=Column(String, default=SocialAccountStatus.ACTIVE), description="社交账号状态")
#
#     class Config:
#         arbitrary_types_allowed = True