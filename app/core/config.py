#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:28 
@Desc    ：
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 项目名称
    PROJECT_NAME: str = "FastAPI完整的用户系统"
    # 项目版本
    PROJECT_VERSION: str = "0.0.1"
    # 项目描述
    PROJECT_DESC: str = "一个完整的fastapi项目，包含用户登录、注册、权限管理等功能"
    # 项目作者
    PROJECT_AUTHOR: str = "Chen GangQiang"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 数据库配置
    MYSQL_URL: str
    REDIS_URL: str

    APP_ENV: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # extra = "ignore"  # 或 "allow" 以允许额外的字段


settings = Settings()


