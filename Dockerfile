# 使用官方Python镜像作为基础镜像
from python:3.12-slim

# 设置容器内的工作目录
WORKDIR /app

# 复制项目文件
COPY pyproject.toml poetry.lock* /app/

# 安装Poetry和依赖
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# 复制当前目录下的所有文件到工作目录
COPY . /app


CMD uvicorn main:app --port=8000 --host=0.0.0.0
