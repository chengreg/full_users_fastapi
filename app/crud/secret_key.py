#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 03:20 
@Desc    ：
"""
from typing import List

from sqlalchemy.orm import Session
from ..models.secret_key import SecretKey
from app.core.utils import generate_secret_key


def create_secret_key(db: Session, secret_key_data: dict, user_id: str) -> SecretKey:
    # 生成一个安全的随机字符串作为secret_key
    generated_secret_key = generate_secret_key("sk-", 50)

    # 创建SecretKey实例，包含生成的secret_key和其他提供的数据
    db_secret_key = SecretKey(**secret_key_data, secret_key=generated_secret_key, user_id=user_id)

    db.add(db_secret_key)
    db.commit()
    db.refresh(db_secret_key)
    return db_secret_key


def get_user_secret_keys(db: Session, user_id: str) -> List[SecretKey]:
    return db.query(SecretKey).filter(SecretKey.user_id == user_id).all()