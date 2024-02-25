# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 19:15
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : system.py
# @Software: PyCharm


from fastapi import APIRouter
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.postgresql_db import engine
from app.models.system.system_params import SystemParams
from app.crud.system.system_params import SystemParamsCRUD

system_router = APIRouter(prefix="/system", tags=["系统接口"])

system_router.get("/system/params")

# 创建异步session
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
db = SystemParamsCRUD(SystemParams)


@system_router.get("/system/params", summary="获取系统参数")
async def get_system_params(params_name: str):
    return {"system_params": "system_params"}
