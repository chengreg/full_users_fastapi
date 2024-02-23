#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 03:18 
@Desc    ：
"""

from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class SecretKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    name: str
    secret_key: str
    tracking: bool = Field(default=False)
    created: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    permissions: str
