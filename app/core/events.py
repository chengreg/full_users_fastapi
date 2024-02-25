#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:06 
@Desc    ：
"""

from typing import Callable
from fastapi import FastAPI
from app.core.custom_logger import logger
from app.db.redis_db import get_redis_pool

# from app.core.logging_config import setup_logger


def startup(app: FastAPI) -> Callable:
    async def app_startup() -> None:
        # 在应用启动时配置日志
        # setup_logger()
        logger.info("项目开始运行...")
        global redis_pool
        redis_pool = await get_redis_pool()

    return app_startup


def shutdown(app: FastAPI) -> Callable:
    async def app_shutdown() -> None:
        global redis_pool
        if redis_pool:
            redis_pool.close()
            await redis_pool.wait_closed()
            redis_pool = None

        logger.info("项目停止运行...")

    return app_shutdown
