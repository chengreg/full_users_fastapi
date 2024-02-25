# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 18:55
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : system_params.py
# @Software: PyCharm


from app.models.base_model import Base
from sqlmodel import Field
from sqlalchemy.dialects.postgresql import JSON


class SystemParams(Base):
    __tablename__ = "system_params"

    params_name: str = Field(unique=True, max_length=255, description="参数名称")
    params_value: JSON = Field(sa_type=JSON,description="参数值")

    class Config:
        arbitrary_types_allowed = True
