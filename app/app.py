#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:05 
@Desc    ：
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.event import startup, shutdown
from .api.v1.routes import v1_router
from .core.config import settings


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        docs_url="/",
        description=settings.PROJECT_DESC)

    # 注册事件
    app.add_event_handler("startup", startup(app))
    app.add_event_handler("shutdown", shutdown(app))

    # 注册v1_router路由
    app.include_router(v1_router)

    return app
