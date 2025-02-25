from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.engine import Engine
from typing import Generator

from .config import settings
from .log import logger

from app.models.db import *


def init_engine():
    """创建全局 Engine 对象"""
    global engine
    if engine is not None:
        return
    if settings.db_url is None:
        logger.warning("数据库 URL 配置项为空，未初始化 sqlmodel Engine 对象。")
        engine = None
    else:
        engine = create_engine(settings.db_url.unicode_string())
        logger.debug("初始化 sqlmodel Engine 对象完成。")


def check_db_tables():
    """检查数据表，若表不存在，则完成建表操作"""
    global engine
    if engine is None:
        logger.warning("Engine 对象不存在，无法检查数据表，已略过。")
        return
    SQLModel.metadata.create_all(engine)
    logger.debug(f"检查数据表完成，当前元数据中的表如下：{', '.join(SQLModel.metadata.tables.keys())}。")


def get_session() -> Generator[Session, None, None]:
    """通过依赖注入获取 Session 实例"""
    global engine
    if engine is None:
        logger.warning("Engine 对象不存在，无法提供 Session 对象。")
        raise ValueError("Engine 对象不存在，无法提供 Session 对象。")
    with Session(engine) as session:
        yield session


engine: Engine | None = None
"""sqlmodel Engine 对象"""

init_engine()

check_db_tables()

__all__ = [
    "engine",
    "get_session",
]
