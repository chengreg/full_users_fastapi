#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:32 
@Desc    ：
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取数据库连接 URL
DATABASE_URL = os.getenv("MYSQL_URL")

# SQLModel 配置
engine = create_engine(DATABASE_URL)

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 初始化数据库
def init_db():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database initialized")
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database initialization error")


# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
