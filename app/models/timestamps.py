#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:06 
@Desc    ：
"""
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, DateTime
from sqlmodel import Field


class Timestamps(BaseModel):
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.now), description="创建时间")
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False), description="修改时间")

