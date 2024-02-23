#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author  ：Chen GangQiang
@Date    ：2024/2/22 23:09 
@Desc    ：
"""

from app.app import create_app

app = create_app()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)