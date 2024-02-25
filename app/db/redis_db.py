# -*- coding: utf-8 -*-
# @Time    : 2024/2/23 14:06
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : redis_db.py
# @Software: PyCharm

import aioredis
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取数据库连接 URL
REDIS_URL = os.getenv("REDIS_URL")

# 全局变量用于存储Redis连接池
redis_pool = None


async def get_redis_pool():
    global redis_pool
    if redis_pool is None:
        REDIS_URL = os.getenv("REDIS_URL")
        redis_pool = await aioredis.create_redis_pool(REDIS_URL, encoding="utf-8")
    return redis_pool
