"""场景相关模型"""

from sqlalchemy.dialects.postgresql import JSONB, BIGINT
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Annotated
from enum import StrEnum

from .common import JSONValue


class SceneType(StrEnum):
    """应用场景类型枚举"""

    test = 'test'
    '''测试场景'''

    live_normal = 'live_normal'
    '''
    普通直播场景
    
    表示普通的针对用户互动行为进行响应的直播场景
    '''

    live_private = 'live_private'
    '''
    封闭直播场景

    表示对模型的输入是可控的直播场景，如开发者对话、联动、外景等
    '''

    live_readbook = 'live_readbook'
    '''
    读书会直播场景
    '''

    live_playgame = 'live_playgame'
    '''
    游戏直播场景
    '''

    chat_private = 'chat_private'
    '''
    私人聊天场景
    
    只有单个其他聊天参与人的聊天场景
    '''

    chat_public = 'chat_public'
    '''
    公共聊天场景
    
    有多个其他聊天参与人的聊天场景
    '''

    tweet = 'tweet'
    '''
    推文生成场景
    
    仅指代生成推文的过程，不包括推文的回复
    '''

    community = 'community'
    '''
    社区场景
    
    社区内容的回复、评论等，包括对自身内容的回复
    '''

    unknown = 'unknown'
    '''未知场景'''


class Scene_Info(SQLModel, table=True):
    """
    应用场景实例信息表模型
    
    应用场景指一段特定的应用区间，如一场直播、一段推文生成、一个社区回复主题等，不区分媒体平台
    """

    id: int | None = Field(default=None, primary_key=True, nullable=False)
    """应用场景实例系统标识"""

    scene_type: Annotated[str, SceneType] = Field(default=SceneType.unknown, nullable=False)
    """应用场景类别"""

    description: str = Field(default='', nullable=False)
    """该次场景实例简单描述"""

    start_timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000),
        sa_type=BIGINT,
        nullable=False,
    )
    """应用场景开始时间戳(毫秒)"""

    @property
    def start_datetime(self) -> datetime:
        """应用场景开始时间"""
        return datetime.fromtimestamp(self.start_timestamp / 1000)

    end_timestamp: int | None = Field(
        default=None,
        sa_type=BIGINT,
        nullable=True,
    )
    """应用场景结束时间戳(毫秒)"""

    @property
    def end_datetime(self) -> datetime | None:
        """应用场景结束时间"""
        if self.end_timestamp is None:
            return None
        return datetime.fromtimestamp(self.end_timestamp / 1000)

    fields: dict[str, JSONValue] = Field(default_factory=dict, sa_type=JSONB, nullable=False)
    """
    场景实例信息字段
    
    通常存放模型参数、提示词等信息
    """


__all__ = [
    "SceneType",
    "Scene_Info",
]
