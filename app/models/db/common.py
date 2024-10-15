from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Enum
from datetime import datetime
from sqlalchemy import Column
from enum import StrEnum
from typing import Any


class Platform(StrEnum):
    """平台类别"""

    core = 'core'
    '''核心'''

    bilibili = 'bilibili'
    '''Bilibili'''

    douyin = 'douyin'
    '''抖音'''

    tiktok = 'tiktok'
    '''Tiktok'''

    youtube = 'youtube'
    '''Youtube'''


class SceneType(StrEnum):
    """应用场景类别"""

    test = 'test'
    '''测试场景'''

    live = 'live'
    '''直播场景'''

    chat = 'chat'
    '''聊天场景'''

    tweet = 'tweet'
    '''推文场景'''


class SceneSubType(StrEnum):
    """应用场景子类别"""

    undefined = 'undefined'
    '''未定义场景'''

    live_private_chat = 'live_private_chat'
    '''
    直播私有聊天
    
    直播场景下的私有聊天表示聊天输入是可控的，如开发者对话、联动对话等
    '''

    live_public_chat = 'live_public_chat'
    '''
    直播公开聊天
    
    直播场景下的公共聊天表示聊天输入是不可控的，如回复弹幕等
    '''

    tweet_post = 'tweet_post'
    '''推文发布'''

    community_reply = 'community_reply'
    '''
    社区回复
    
    不限于自己的推文回复，也包含社交媒体的评论回复
    '''


class Scene_Info(SQLModel, table=True):
    """应用场景实例信息表模型"""

    id: int | None = Field(default=None, primary_key=True)
    """唯一实例 id 标识"""

    scene_type: SceneType = Field(default=SceneType.test, sa_column=Column(Enum(SceneType), nullable=False))
    """应用场景类别"""

    scene_sub_type: str = Field(nullable=False)
    """
    应用场景子类别

    例如：

    测试场景的不同功能测试；

    直播场景的不同直播类型，聊天电台、读书、互动游戏等；
    """

    platform: Platform = Field(sa_column=Column(Enum(Platform), nullable=False))
    """应用场景实例所在平台"""

    description: str = Field(default='', nullable=False)
    """该次场景实例简单描述"""

    platform_fields: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB, nullable=False)
    """实例平台信息字段"""

    scene_fields: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB, nullable=False)
    """实例场景类别信息字段"""

    start_time: datetime = Field(default_factory=datetime.now, nullable=False)
    """应用场景开始时间"""

    end_time: datetime | None = Field(default=None, nullable=False)
    """应用场景结束时间"""


class User_Info(SQLModel, table=True):
    """多平台用户信息表模型"""

    id: int | None = Field(default=None, primary_key=True)
    """唯一用户 id 标识"""

    main_id: int | None = Field(default=0, nullable=False)
    """用户主账号 id，用于跨平台用户识别，默认为 0"""

    platform: Platform = Field(sa_column=Column(Enum(Platform), nullable=False))
    """用户所在平台，core 代表内置"""

    user_id: str = Field(default='', nullable=False)
    """用户 id"""

    user_name: str = Field(default='', nullable=False)
    """用户名称"""

    description: str = Field(default='', nullable=False)
    """用户简单描述，用于补充对用户的认知知识"""

    platform_fields: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB, nullable=False)
    """用户平台信息字段"""


__all__ = [
    "Platform",
    "SceneType",
    "SceneSubType",
    "Scene_Info",
    "User_Info",
]
