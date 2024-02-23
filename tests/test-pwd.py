#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 21:32 
@Desc    ：
"""

from app.core.security import verify_password, get_password_hash

pwd = "chengang"

hashed_pwd = get_password_hash(pwd)
print(hashed_pwd)

ha = "$2b$12$8vOxBfL74igB1dBAvopeQOV.zYvkoGzBUqUSEBar35NJfBgkz0.3W"
print(verify_password("chengang", ha))

# $2b$12$tCvMDpdNCzvZPT6LoZvIUO5y8mUVOv/S9WrAWQb/rzasA8ZTg17Au
# $2b$12$SUKKsgCpkFyAuHwoscOY7e88HYkp/86pbW5MXOf61CLJOj/nuydbm