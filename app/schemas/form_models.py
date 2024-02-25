# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 12:28
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : form_models.py
# @Software: PyCharm


from fastapi import Form
from typing import Optional


class OAuth2PasswordRequestFormEmail:
    def __init__(
            self,
            email: str = Form(...),
            password: str = Form(...),
            scope: Optional[str] = Form(""),
            grant_type: Optional[str] = Form(None),
            client_id: Optional[str] = Form(None),
            client_secret: Optional[str] = Form(None)
    ):
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret


class OAuth2PasswordRequestFormPhone:
    def __init__(
            self,
            country_code: str = Form(...),
            phone_number: str = Form(...),
            password: str = Form(...),
            scope: Optional[str] = Form(""),
            grant_type: Optional[str] = Form(None),
            client_id: Optional[str] = Form(None),
            client_secret: Optional[str] = Form(None)
    ):
        self.country_code = country_code
        self.phone_number = phone_number
        self.password = password
        self.scopes = scope.split()
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
