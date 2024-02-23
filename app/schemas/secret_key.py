#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 03:23 
@Desc    ：
"""

from pydantic import BaseModel


class SecretKeyCreate(BaseModel):
    name: str
    tracking: bool = False
    permissions: str
