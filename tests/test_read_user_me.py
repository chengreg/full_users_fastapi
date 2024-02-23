#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/23 02:30 
@Desc    ：
"""

import requests
import pytest

# 替换为你的API端点
BASE_URL = "http://127.0.0.1:8844"
TOKEN_URL = f"{BASE_URL}/v1/auth/token"
USERS_ME_URL = f"{BASE_URL}/v1/user/me"


def get_access_token(username: str, password: str) -> str:
    response = requests.post(TOKEN_URL, data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def access_token() -> str:
    # 替换为有效的用户名和密码
    USERNAME = "pigbaby0521"
    PASSWORD = "chengang"
    return get_access_token(USERNAME, PASSWORD)

def test_read_users_me(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USERS_ME_URL, headers=headers)
    assert response.status_code == 200
    # 这里可以添加更多的断言，例如验证返回的用户信息
    assert "username" in response.json()
