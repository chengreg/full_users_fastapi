# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 19:15
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : system.py
# @Software: PyCharm


from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.postgresql_db import engine
from app.models.system.system_params import SystemParams
from app.crud.system.system_params import SystemParamsCRUD
from app.schemas.system import SystemParamsSchemas

system_router = APIRouter(prefix="/system", tags=["系统接口"])

system_router.get("/system/params")

# 创建异步session
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
db = SystemParamsCRUD(SystemParams)


@system_router.get("/system/params", summary="获取系统参数")
async def get_system_params(params_name: str):
    result = await db.get_system_params(async_session, params_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"参数 {params_name} 未找到。")
    return result


@system_router.post("/system/params", summary="新增系统参数")
async def add_system_params(system_params: SystemParamsSchemas):
    result = await db.add_system_params(async_session, system_params)

    return result