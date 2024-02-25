#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 02:14 
@Desc    ：
"""

# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from starlette import status
#
# # from app.core.security import create_access_token_token
# from app.crud.auth import create_access_token, get_current_token, revoke_token, check_token_exists
#
# from datetime import timedelta
#
# auth_router = APIRouter(prefix="/auth", tags=["认证管理"])
#
#
# @auth_router.post("/token", summary="获取token并存储到Redis中")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     # 这里应该验证用户名和密码
#     # 暂时假设任何用户都是有效的
#     user = {"username": form_data.username}
#     access_token_expires = timedelta(minutes=30)
#     access_token = await create_access_token(
#         data={"sub": user["username"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @auth_router.post("/logout", summary="登出并从Redis中删除token")
# async def logout(token: str = Depends(get_current_token)):
#     try:
#         # 检查Redis中是否存在该令牌
#         if not await check_token_exists(token):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
#
#         # 如果令牌存在，则进行登出并从Redis中删除该令牌
#         await revoke_token(token)
#         return {"message": "Logged out successfully."}
#     except HTTPException as e:
#         # 如果令牌不存在或有其他HTTP异常，直接抛出
#         raise e
#     except Exception as e:
#         # 对于非HTTP异常，返回500错误
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

