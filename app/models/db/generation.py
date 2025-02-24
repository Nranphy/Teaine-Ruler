"""模型生成内容相关模型"""

from sqlalchemy.dialects.postgresql import TEXT, BIGINT
from sqlmodel import SQLModel, Field
from datetime import datetime


class Generation(SQLModel, table=True):
    """模型生成内容表模型"""

    id: int | None = Field(default=None, primary_key=True, nullable=False)
    """生成内容主键 id"""

    timestamp: int = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000),
        sa_type=BIGINT,
        nullable=False,
    )
    """生成内容完成记录时间戳"""

    inference_duration: int = Field(default=0, nullable=False)
    """生成内容完成模型推理时长(毫秒)"""

    @property
    def datetime(self) -> datetime:
        """生成内容完成记录时间"""
        return datetime.fromtimestamp(self.timestamp / 1000)

    scene_id: int = Field(nullable=False)
    """应用场景实例系统标识"""

    interaction_id: int = Field(nullable=False)
    """交互行为实例系统标识"""

    context: str = Field(default='', sa_type=TEXT, nullable=False)
    """模型上下文文本内容"""

    content: str = Field(default='', sa_type=TEXT, nullable=False)
    """模型生成文本内容"""

    edited_content: str = Field(default='', sa_type=TEXT, nullable=False)
    """人工修改后模型生成文本内容"""


__all__ = [
    "Generation",
]
