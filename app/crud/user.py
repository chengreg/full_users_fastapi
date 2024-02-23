#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 00:53 
@Desc    ：
"""
# crud/crud_user.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models.user import User, UserProfile, UsersStatusEnum
from app.schemas.user import RegisterRequest
# # from .auth import verify_password, get_password_hash
# from app.core.security import get_password_hash, verify_password
from app.core.security import get_password_hash, verify_password
from uuid import uuid4
from fastapi import HTTPException


# 创建用户
def create_user(db: Session, user_in: RegisterRequest):
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
def check_existence(db: Session, username: str = None, email: str = None, phone_number: str = None,
                    country_code: str = None) -> dict:
    existence = {
        "username_exists": db.query(
            db.query(User).filter(User.username == username).exists()).scalar() if username else False,
        "email_exists": db.query(db.query(User).filter(User.email == email).exists()).scalar() if email else False,
        "phone_exists": db.query(db.query(User).filter(User.phone_number == phone_number,
                                                       User.country_code == country_code).exists()).scalar() if phone_number and country_code else False,
    }
    return existence


# 获取用户信息
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# 检查用户是否存在
def check_user_existence(db: Session, username: str = None, email: str = None, phone_number: str = None,
                         country_code: str = None) -> list:
    existing_fields = []

    if username and db.query(db.query(User).filter(User.username == username).exists()).scalar():
        existing_fields.append("username")

    if email and db.query(db.query(User).filter(User.email == email).exists()).scalar():
        existing_fields.append("email")

    if phone_number and country_code and db.query(db.query(User).filter(User.phone_number == phone_number,
                                                                        User.country_code == country_code).exists()).scalar():
        existing_fields.append("phone number and country code")

    return existing_fields


def update_user(db: Session, user_id: str, user_update: dict):
    existing_fields = check_user_existence(
        db,
        username=user_update.get("username"),
        email=user_update.get("email"),
        phone_number=user_update.get("phone_number"),
        country_code=user_update.get("country_code")
    )

    if existing_fields:
        fields_str = ", ".join(existing_fields)
        raise HTTPException(status_code=400, detail=f"{fields_str} already exists.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def update_user_profile(db: Session, user_id: str, profile_update: dict):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
    for key, value in profile_update.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(User).filter(User.email == email).first()


def get_user_by_phone(db_session: Session, country_code: str, phone_number: str):
    return db_session.query(User).filter(User.country_code == country_code, User.phone_number == phone_number).first()


def authenticate_user(db_session: Session, identifier: str, password: str):
    user = None
    # 尝试通过用户名获取用户
    if not user:
        user = get_user_by_username(db_session, identifier)
    # 尝试通过邮箱获取用户
    if not user:
        user = get_user_by_email(db_session, identifier)
    # 尝试通过国际区号和手机号获取用户
    if not user and '@' not in identifier and len(identifier.split('-')) == 2:
        international_code, phone = identifier.split('-')
        user = get_user_by_phone(db_session, international_code, phone)

    if user and verify_password(password, user.hashed_password):
        return user
    return False


def get_user_status(db_session: Session, user_id: str) -> UsersStatusEnum:
    try:
        user = db_session.query(User).filter(User.id == user_id).one()
        return user.status
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


def update_user_status(db_session: Session, user_id: str, new_status: UsersStatusEnum):
    try:
        user = db_session.query(User).filter(User.id == user_id).one()
        user.status = new_status
        db_session.commit()
        return user
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

