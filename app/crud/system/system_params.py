# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 19:02
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : system_params.py
# @Software: PyCharm


from app.crud.base_crud import BaseCRUD
from app.models.system.system_params import SystemParams
from app.schemas.system import SystemParamsSchemas
from sqlmodel import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class SystemParamsCRUD(BaseCRUD[SystemParams]):
    async def get_system_params(self, async_session: async_sessionmaker[AsyncSession], params_name: str) -> SystemParams:
        async with async_session() as session:
            # 使用 params_name 而不是 id 作为查询条件
            query = select(self.model).where(self.model.params_name == params_name)
            result = await session.execute(query)
            return result.scalars().first()

    async def add_system_params(self, async_session, system_params: SystemParamsSchemas):
        # 检查参数名称是否已存在
        existing_param = await self.get_system_params(async_session, system_params.params_name)
        if existing_param:
            raise ValueError(f"参数 {system_params.params_name} 已存在。")

        # 创建 SystemParams 实例
        new_system_param = SystemParams(
            params_name=system_params.params_name,
            params_value=system_params.params_value
        )

        # 添加到数据库
        return await self.add(async_session, new_system_param)

