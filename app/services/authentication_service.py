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


async def generate_token_response(user_identifier: str) -> TokenResponseSchema:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user_identifier},
        expires_delta=access_token_expires
    )

    return TokenResponseSchema(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.total_seconds()
    )