from pydantic import BaseModel, model_validator, Field

from app.utils.log import logger


class BasePrompt(BaseModel):
    """base prompt 模型"""

    name: str
    """base prompt 名称"""

    text: str
    """base prompt 内容"""

    params: dict[str, str] = Field(default_factory=dict)
    """
    base prompt 参数表
    
    参数名与 base prompt 中的参数相对应，不需要加入参数标记；
    base prompt 将在实例化时自动完成渲染。
    """

    @model_validator(mode="after")
    def params_render(self):
        """base prompt 自动渲染"""
        for k, v in self.params.items():
            if v.startswith('{{{') or v.endswith('}}}'):
                logger.warning('base prompt 渲染参数值以{{{和}}}开头或结尾，可能导致渲染结果错误。')
            self.text = self.text.replace('{{{' + k + '}}}', v)
        return self


class BasePromptCreate(BaseModel):
    """base prompt 创建模型"""

    name: str
    """base prompt 名称"""

    text: str
    """base prompt 内容"""


class BasePromptInfo(BaseModel):
    """base prompt 基础情况"""

    name: str
    """base prompt 名称"""

    length: int
    """base prompt 长度"""

    param_num: int
    """base prompt 参数位个数"""

    def __str__(self) -> str:
        return ('<'
                f'名称: {self.name}, '
                f'长度: {self.length}, '
                f'参数数: {self.param_num}'
                '>')


class BasePromptManagerStatus(BaseModel):
    """base prompt 管理器状态模型"""

    is_available: bool
    """当前是否可用"""

    base_prompt_info: list[BasePromptInfo]
    """base prompt 基础信息"""


__all__ = [
    "BasePrompt",
    "BasePromptInfo",
    "BasePromptCreate",
    "BasePromptManagerStatus",
]
