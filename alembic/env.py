from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
from dotenv import load_dotenv
from sqlmodel import SQLModel

from app.models import User, UserProfile, SecretKey

# 加载环境变量配置
def load_env_config():
    app_env = os.getenv("APP_ENV", "development")
    env_file = {
        "development": ".env",
        "production": ".env.production",
        "testing": ".env.testing",
    }.get(app_env, ".env")
    load_dotenv(dotenv_path=env_file)

load_env_config()


# Alembic配置对象
config = context.config

# 如果env.py配置了Logging，可以通过fileConfig来配置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """在离线模式下运行迁移."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"},)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在在线模式下运行迁移"""
    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = os.getenv('MYSQL_URL')  # 使用环境变量中的数据库URL
    connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
