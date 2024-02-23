#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:06 
@Desc    ：
"""

from typing import Callable
from fastapi import FastAPI
from .mysql_db import init_db
from app.models.user import User, UserProfile
from app.models.secret_key import SecretKey


def startup(app: FastAPI) -> Callable:
    async def app_startup() -> None:
        print("项目启动...")
        init_db()

    return app_startup


def shutdown(app: FastAPI) -> Callable:
    async def app_shutdown() -> None:
        print("项目结束...")

    return app_shutdown
