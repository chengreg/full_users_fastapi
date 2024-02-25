# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 19:02
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : system_params.py
# @Software: PyCharm


from app.crud.base_crud import BaseCRUD
from app.models.system.system_params import SystemParams


class SystemParamsCRUD(BaseCRUD[SystemParams]):
    pass

