# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 13:16
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : authentication_service.py
# @Software: PyCharm


from datetime import timedelta
from app.core.config import settings
from app.schemas.user import TokenResponseSchema
from app.crud.auth import create_access_token
from app.db.redis_db import get_redis_pool


async def generate_token_response(user_identifier: str) -> TokenResponseSchema:
    """ 用于注册和登录成功后生成token并返回TokenResponseSchema，同时将token存储到Redis中"""
    # 生成token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user_identifier},
        expires_delta=access_token_expires
    )

    # 将token存储到Redis中
    redis = await get_redis_pool()
    await redis.setex(f"token:{user_identifier}", int(access_token_expires.total_seconds()), access_token)

    return TokenResponseSchema(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.total_seconds()
    )


async def check_token_exists_in_redis(user_identifier: str) -> bool:
    # 获取Redis连接池
    redis = await get_redis_pool()

    # 检查token是否存在
    token_exists = await redis.exists(f"token:{user_identifier}")

    return bool(token_exists)


async def delete_token_from_redis(user_identifier: str) -> None:
    print("获取的数据：",user_identifier)
    # 获取Redis连接池
    redis = await get_redis_pool()

    # 删除token
    await redis.delete(f"token:{user_identifier}")
