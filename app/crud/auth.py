# -*- coding: utf-8 -*-
# @Time    : 2024/2/23 14:15
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : auth.py
# @Software: PyCharm

from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends
from app.core.config import settings
from app.core.redis_db import get_redis_pool
# from passlib.context import CryptContext
from app.core.deps import oauth2_scheme

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    redis = await get_redis_pool()  # 获取Redis连接池
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # 将令牌存储到Redis中，并设置过期时间
    await redis.setex(encoded_jwt, int(expires_delta.total_seconds()), 'true')

    return encoded_jwt


async def verify_token(token: str, credentials_exception) -> dict:
    redis = await get_redis_pool()  # 获取Redis连接池
    try:
        # 首先检查Redis中是否有令牌
        if not await redis.exists(token):
            raise credentials_exception
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise credentials_exception


async def revoke_token(token: str):
    redis = await get_redis_pool()  # 获取Redis连接池
    # 从Redis中删除令牌
    await redis.delete(token)

async def get_current_token(token: str = Depends(oauth2_scheme)) -> str:
    return token

async def check_token_exists(token: str):
    redis = await get_redis_pool()  # 获取Redis连接池
    exists = await redis.exists(token)
    return exists