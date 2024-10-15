from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

from app.core.config import settings
from .log import logger


def get_session() -> Generator[Session, None, None]:
    """通过依赖注入获取 Session 实例"""
    if engine is None:
        logger.warning("数据库 URL 配置项为空，无法提供 Seesion 对象。")
        raise ValueError("数据库 URL 配置项为空，无法提供 Seesion 对象。")
    with Session(engine) as session:
        yield session


def init_db():
    """初始化数据库，完成建表操作"""
    if engine is None:
        logger.warning("数据库 URL 配置项为空，无法初始化数据库，已略过。")
        return
    SQLModel.metadata.create_all(engine)


if settings.db_url is None:
    logger.warning("数据库 URL 配置项为空，。")
    engine = None
else:
    engine = create_engine(settings.db_url.unicode_string())
    """sqlmodel 引擎对象"""

__all__ = [
    "engine",
    "init_db",
    "get_session",
]
