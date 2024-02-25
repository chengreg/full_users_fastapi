#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/25 20:50 
@Desc    ：
"""
from pydantic import BaseModel
from sqlmodel import Field


class SystemParamsSchemas(BaseModel):
    params_name: str = Field(..., description="名称")
    params_value: dict = Field(..., description="参数值")
