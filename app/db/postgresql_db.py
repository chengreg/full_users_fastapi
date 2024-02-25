#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 00:04 
@Desc    ：
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

# Base = declarative_base()

POSTGRES_URL = os.getenv('POSTGRES_URL')

engine = create_async_engine(url=POSTGRES_URL, echo=True)
