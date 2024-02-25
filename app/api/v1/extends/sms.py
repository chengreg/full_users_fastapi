#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 21:35 
@Desc    ：
"""
import random
import os
import json
from fastapi import APIRouter, Request, Query, HTTPException
from starlette.responses import JSONResponse
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.crud.extends.tencent_sms import send_sms, verify_sms_code_in_redis
from app.db.postgresql_db import engine
from app.db.redis_db import get_redis_pool

sms_router = APIRouter(prefix="/user")

# 创建异步session
# async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
# db = SystemParamsCRUD(SystemParams)

load_dotenv()


@sms_router.get("/send_sms_code", summary="发送短信验证码", tags=["用户管理"])
async def send_sms_code(country_code: str=Query(..., regex="^\+\d{1,4}$"), phone_number: str = Query(..., regex="^1[34567890]\\d{9}$")):
    # 获取Redis连接池
    redis = await get_redis_pool()
    # 检查手机号是否已发送过验证码
    expire = os.getenv('TENCENT_SMS_EXPIRE')
    is_sms_code_exists = await redis.exists(f"code_{country_code}_{phone_number}")
    if is_sms_code_exists:
        raise HTTPException(status_code=400,
                            detail=f"手机号 {phone_number} 已发送过验证码，若未收到短信，请{expire}分钟后重试!")

    # 生成随机验证码
    verify_code = "".join([str(random.randint(0, 9)) for _ in range(6)])

    print(f"verify_code: {verify_code}")

    # 发送短信验证码
    response = send_sms(phone_nubmer=phone_number, verify_code=verify_code, time_out=expire, country_code=country_code)

    # 检查短信发送是否成功
    is_ok = json.loads(response.to_json_string())["SendStatusSet"][0]["Code"]
    if is_ok != "Ok":
        raise HTTPException(status_code=400, detail="Failed to send SMS")

    # 将手机号码和短信验证码保存到Redis
    await redis.setex(f"code_{country_code}_{phone_number}", int(os.getenv("TENCENT_SMS_EXPIRE")) * 60, verify_code)

    return JSONResponse(status_code=200,
                        content={"message": f"短信已经发送，{expire} 分钟内有效。",
                                 "expire_in_seconds": int(expire) * 60})


@sms_router.get("/verify_sms_code", summary="验证短信验证码", tags=["用户管理"])
async def verify_sms_code(country_code: str = Query(..., regex="^\+\d{1,4}$"),
                          phone_number: str = Query(..., regex="^1[34567890]\\d{9}$"),
                          verify_code: str = Query(..., regex="^\d{6}$")):
    is_valid = await verify_sms_code_in_redis(country_code, phone_number, verify_code)
    if not is_valid:
        raise HTTPException(status_code=400, detail="验证码错误")
    return JSONResponse(status_code=200, content={"message": "验证码正确"})
