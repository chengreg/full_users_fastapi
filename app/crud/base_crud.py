#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 00:02 
@Desc    ：
"""

from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select
from sqlmodel import SQLModel

# 定义一个泛型变量T，它必须是SQLModel的子类
T = TypeVar('T', bound=SQLModel)


class BaseCRUD(Generic[T]):
    def __init__(self, model: Type[T]):
        """
        初始化时指定CRUD操作的模型类。
        """
        self.model = model

    async def get_all(self, async_session: async_sessionmaker[AsyncSession]) -> List[T]:
        async with async_session() as session:
            statement = select(self.model).order_by(self.model.id)
            result = await session.execute(statement)
            return result.scalars().all()

    async def add(self, async_session: async_sessionmaker[AsyncSession], obj: T) -> T:
        async with async_session() as session:
            session.add(obj)
            await session.commit()
            return obj

    async def get_by_id(self, async_session: async_sessionmaker[AsyncSession], obj_id: str) -> Optional[T]:
        async with async_session() as session:
            statement = select(self.model).filter(self.model.id == obj_id)
            result = await session.execute(statement)
            return result.scalars().first()

    async def update(self, async_session: async_sessionmaker[AsyncSession], obj_id: str, data: dict) -> Optional[T]:
        async with async_session() as session:
            obj = await self.get_by_id(async_session, obj_id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                await session.commit()
            return obj

    async def delete(self, async_session: async_sessionmaker[AsyncSession], obj_id: str) -> bool:
        async with async_session() as session:
            obj = await self.get_by_id(async_session, obj_id)
            if obj:
                await session.delete(obj)
                await session.commit()
                return True
            return False
