#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:53 
@Desc    ：
"""
# crud/crud_user.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from uuid import uuid4


# 创建用户
def create_user(db: Session, user_in: UserCreate):
    hashed_password = get_password_hash(user_in.password)

    user = User(
        id=str(uuid4()),
        username=user_in.username,
        email=user_in.email,
        phone_number=user_in.phone_number,
        country_code=user_in.country_code,
        hashed_password=hashed_password,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("The username or email is already registered.")


# 检查用户名、邮箱、手机号+国际号码是否存在
def check_existence(db: Session, username: str = None, email: str = None, phone_number: str = None, country_code: str = None) -> dict:
    existence = {
        "username_exists": db.query(db.query(User).filter(User.username == username).exists()).scalar() if username else False,
        "email_exists": db.query(db.query(User).filter(User.email == email).exists()).scalar() if email else False,
        "phone_exists": db.query(db.query(User).filter(User.phone_number == phone_number, User.country_code == country_code).exists()).scalar() if phone_number and country_code else False,
    }
    return existence


# 获取用户信息
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()