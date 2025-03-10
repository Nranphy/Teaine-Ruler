"""用户相关模型"""

from sqlalchemy.dialects.postgresql import TEXT, JSONB, BIGINT
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Annotated

from app.common.models.db.typing import JSONValue
from app.common.models.db.enums import Platform


class User_Info(SQLModel, table=True):
    """
    用户信息表模型
    
    本模型将存储用户多个媒体平台的账号，通过主副账号的方式提供跨平台的用户识别
    """

    id: int | None = Field(default=None, primary_key=True, nullable=False)
    """
    用户账号系统标识
    
    数据库自动生成，唯一确定某一用户在某一平台的某一账号
    """

    main_id: int | None = Field(default=None, nullable=True)
    """
    用户主账号系统标识
    
    用于跨平台用户识别，当用户绑定账号后将用对应 id 字段填充，默认为 NULL
    """

    platform: Annotated[str, Platform] = Field(default=Platform.unknown, nullable=False)
    """用户账号所在媒体平台"""

    user_platform_id: str = Field(default='', nullable=False)
    """
    用户媒体平台 id
    
    该 id 应是对应媒体平台提供的唯一标识，且可以保证较长周期内不会变更
    """

    user_name: str = Field(default='', nullable=False)
    """用户名称"""

    description: str = Field(default='', sa_type=TEXT, nullable=False)
    """
    用户简单描述
    
    用于补充对用户的认知知识，如用户的昵称、曾用名、经历、情感等
    """

    platform_fields: dict[str, JSONValue] = Field(default_factory=dict, sa_type=JSONB, nullable=False)
    """
    用户平台信息字段

    存储用户账号在某平台特有的参数字段，如平台账号等级、关注数、粉丝数等

    同一平台的参数模型需要一致，公共字段可单独作为新字段
    """

    register_timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000),
        sa_type=BIGINT,
        nullable=False,
    )
    """用户注册时间戳"""

    @property
    def register_datetime(self) -> datetime:
        """用户注册时间"""
        return datetime.fromtimestamp(self.register_timestamp / 1000)


__all__ = [
    "User_Info",
]
