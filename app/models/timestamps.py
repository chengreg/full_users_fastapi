#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:06 
@Desc    ：
"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class Timestamps(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), description="创建时间")
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}, description="更新时间")

