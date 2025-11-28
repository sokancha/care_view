import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ----------------------------------------------------
# 1. 프로젝트 경로 및 모델 import
# ----------------------------------------------------

# 프로젝트 루트 디렉토리를 Python Path에 추가합니다.
# 이렇게 해야 Alembic이 'app.core.database' 및 'app.core.models'를 찾을 수 있습니다.
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# app/core/database.py 파일에서 정의한 Base 객체를 가져옵니다.
from app.core.database import Base 

# app/models 폴더를 가져옵니다. 
import app.models 

# ----------------------------------------------------
# 2. target_metadata 설정
# ----------------------------------------------------

# target_metadata를 Base.metadata로 설정하여 Alembic이 모델의 메타데이터를 사용하도록 합니다.
target_metadata = Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # ----------------------------------------------------
    # 🚨 수정된 부분: 환경 변수에서 URL을 가져와서 사용
    # ----------------------------------------------------
    db_url = os.environ.get("DATABASE_URL") 
    
    if db_url:
        # 환경 변수 URL이 있다면, 직접 엔진을 생성합니다.
        connectable = engine_from_config(
            {"sqlalchemy.url": db_url}, # 환경 변수 URL을 설정에 주입
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    else:
        # 환경 변수가 없다면, alembic.ini의 기본 설정을 사용합니다.
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        
    # ----------------------------------------------------
    # 나머지 코드는 동일합니다.
    # ----------------------------------------------------
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
