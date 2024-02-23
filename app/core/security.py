#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:52 
@Desc    ：
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    if not password:  # 检查密码是否为None或空字符串
        return None
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码与哈希密码是否匹配。

    :param plain_password: 用户输入的明文密码。
    :param hashed_password: 数据库中存储的哈希密码。
    :return: 布尔值，如果密码匹配返回True，否则返回False。
    """
    return pwd_context.verify(plain_password, hashed_password)
