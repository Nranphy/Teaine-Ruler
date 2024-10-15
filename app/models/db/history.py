from sqlmodel import SQLModel, Field
from datetime import datetime


class History_Base(SQLModel):
    """历史记录表模型基类"""

    id: int | None = Field(default=None, primary_key=True)
    """主键 id"""

    time: datetime = Field(default_factory=datetime.now, nullable=False)
    """记录时间"""

    scene_info_id: int = Field(nullable=False, foreign_key='scene_info.id')
    """场景实例 id"""

    user_id: str = Field(default='', nullable=False)
    """用户 id"""

    user_name: str = Field(default='', nullable=False)
    """用户名称"""


class Chat_History(History_Base, table=True):
    """聊天历史记录表模型"""

    content: str = Field(default='', nullable=False)
    """聊天内容"""

    is_super_chat: bool = Field(default=False, nullable=False)
    """是否醒目留言"""

    amount: int = Field(default=0, nullable=False)
    """留言金额(分)"""

    reply_content: str = Field(default='', nullable=False)
    """回复内容"""


class Gift_History(History_Base, table=True):
    """赠礼历史记录表模型"""

    gift_name: str = Field(default='', nullable=False)
    """礼物名称"""

    is_free: bool = Field(default=True, nullable=False)
    """是否免费礼物"""

    amount: int = Field(default=0, nullable=False)
    """礼物总金额(分)"""

    gift_num: int = Field(default=0, nullable=False)
    """礼物数量"""


class Premium_History(History_Base, table=True):
    """付费订阅历史记录表模型"""

    premium_type: str = Field(default='', nullable=False)
    """付费订阅名称"""

    amount: int = Field(default=0, nullable=False)
    """订阅总金额(分)"""

    duration_days: int = Field(default=0, nullable=False)
    """持续时长(天)"""
