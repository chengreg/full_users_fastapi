#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 22:59 
@Desc    ：
"""
from fastapi import APIRouter
from .user import user_router
from .auth import auth_router

# 创建v1版本的路由
v1_router = APIRouter(prefix="/v1")

# 将user_router注册到v1_router中
v1_router.include_router(user_router)
v1_router.include_router(auth_router)
