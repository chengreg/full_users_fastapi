#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 02:05 
@Desc    ：
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
import jwt
from sqlmodel import Session

from .mysql_db import get_db
from .config import settings
from ..crud.user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = get_user_by_username(db, username)
        if not user:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return user