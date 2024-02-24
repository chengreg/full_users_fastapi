#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 02:37 
@Desc    ：
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
import jwt
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings
from app.db.redis_db import get_redis_pool
from app.crud.user.user import UserCRUD
from app.db.postgresql_db import engine
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")

# 创建异步session
session = async_sessionmaker(bind=engine, expire_on_commit=False)
db = UserCRUD(User)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 检查Redis中是否存在令牌
    redis = await get_redis_pool()
    token_exists = await redis.exists(token)
    if not token_exists:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = await db.get_by_username(session, username)
        if not user:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return user
