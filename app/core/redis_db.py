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


async def get_redis_pool():
    pool = await aioredis.create_redis_pool(REDIS_URL, encoding="utf-8")
    return pool
