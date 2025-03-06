from pydantic import BaseModel, Field, model_validator
from typing import Literal

ROLE_TYPE = Literal['system', 'user', 'assistant']
"""角色类型字面量"""

KNOWLEDGE_KEYS = Literal[
    'user_description',
    'datetime_info',
    'background_info',
    'other',
]
"""
知识文本块命名键

user_description: 用户的简单描述文本;
datetime_info: 当前日期和时间信息文本;
background_info: 设定集背景信息文本;
other: 其他未归类知识内容
"""


class Role(BaseModel):
    """角色信息模型"""

    role_type: ROLE_TYPE
    """
    角色类型
    
    与角色名称无关，即使是多角色或多用户也应该规定在类别中
    """

    name: str | None = None
    """角色名"""

    @model_validator(mode="after")
    def strip(self):
        """去除 name 字段的前后空白字符"""
        if self.name is not None:
            self.name = self.name.strip()
        return self


class Message(BaseModel):
    """语料单个消息段模型"""

    role: Role
    """消息角色实例"""

    content: str
    """消息文本内容"""

    knowledge: dict[KNOWLEDGE_KEYS, str] = Field(default_factory=dict)
    """
    消息知识文本内容

    键为知识文本块的命名键，值为知识内容
    """

    @model_validator(mode="after")
    def strip(self):
        """去除 content 字段与语料值的前后空白字符"""
        if self.content is not None:
            self.content = self.content.strip()
        for k, v in self.knowledge.items():
            self.knowledge[k] = v.strip()
        return self


class Corpus(BaseModel):
    """单条语料模型"""

    data: list[Message]
    """对话语料消息列表"""

    role_name_map: dict[str, str] = Field(default_factory=dict, exclude=True)
    """角色名与标准角色名映射表"""

    @model_validator(mode="after")
    def update_role_name_map(self):
        """更新角色名与标准角色名映射表"""
        if self.role_name_map:
            return self
        role_pool: dict[str, set] = {}
        for msg in self.data:
            if msg.role.role_type not in role_pool:
                role_pool[msg.role.role_type] = set()
            if msg.role.name is not None:
                if msg.role.name not in role_pool[msg.role.role_type]:
                    role_pool[msg.role.role_type].add(msg.role.name)
                    self.role_name_map[msg.role.name] = msg.role.role_type + str(len(role_pool[msg.role.role_type]))
        for k, v in role_pool.items():
            if len(v) == 1:
                name = list(v)[0]
                self.role_name_map[name] = k
        return self


class DatasetInfo(BaseModel):
    """语料数据集信息模型"""

    name: str = ''
    """数据集名称"""

    description: str = ''
    """数据集描述"""

    bucket_num: int = 8
    """数据分桶数量"""

    @model_validator(mode="after")
    def check_bucket_num(self):
        """检查数据分桶数量是否合法"""
        if self.bucket_num < 1:
            raise ValueError("数据分桶数量必须大于等于 1。")
        return self


__all__ = [
    "ROLE_TYPE",
    "KNOWLEDGE_KEYS",
    "Role",
    "Message",
    "Corpus",
    "DatasetInfo",
]
