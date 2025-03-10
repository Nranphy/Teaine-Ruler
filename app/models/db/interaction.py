"""用户的交互动作相关模型"""

from sqlalchemy.dialects.postgresql import TEXT, JSONB, BIGINT
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Annotated

from app.common.models.db.typing import JSONValue
from app.common.models.db.enums import InteractionType


class Interaction(SQLModel, table=True):
    """交互行为记录表模型"""

    id: int | None = Field(default=None, primary_key=True, nullable=False)
    """交互行为主键 id"""

    timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000),
        sa_type=BIGINT,
        nullable=False,
    )
    """交互行为记录时间戳"""

    @property
    def datetime(self) -> datetime:
        """交互行为记录时间"""
        return datetime.fromtimestamp(self.timestamp / 1000)

    scene_id: int = Field(nullable=False)
    """应用场景实例系统标识"""

    user_id: int = Field(nullable=False)
    """用户账号系统标识"""

    type: Annotated[str, InteractionType] = Field(default=InteractionType.unknown, nullable=False)
    """交互行为类型"""

    text: str = Field(default='', sa_type=TEXT, nullable=False)
    """交互行为文本"""

    amount: int = Field(default=0, nullable=False)
    """
    交互行为总金额(分)

    只统计人民币金额，不统计虚拟代币数量
    
    交互行为存在复数个子行为，如一次赠送多个礼物时，应该统计总金额，而非单价
    """

    item_name: str = Field(default='', nullable=False)
    """
    交互相关名称
    
    赠礼场景如礼物名，订阅场景如订阅套餐名
    """

    item_num: int = Field(default=0, nullable=False)
    """
    交互相关名称数量
    
    赠礼场景如礼物数量，订阅场景如订阅套餐个数
    """

    fields: dict[str, JSONValue] = Field(default_factory=dict, sa_type=JSONB, nullable=False)
    """
    其他私有字段
    """


__all__ = [
    "Interaction",
]
