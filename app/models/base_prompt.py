from pydantic import BaseModel, model_validator, Field
import re


class BasePrompt(BaseModel):
    """base prompt 模型"""

    name: str
    """base prompt 名称"""

    text: str
    """
    base prompt 文本内容
    
    如果传入 params 参数，则为渲染后的 base prompt 文本
    """

    params: dict[str, str] = Field(default_factory=dict)
    """
    base prompt 参数表
    
    参数名与 base prompt 中的参数相对应，不需要加入参数标记；
    base prompt 将在实例化时自动完成渲染。
    """

    @model_validator(mode="after")
    def params_render(self):
        """base prompt 自动渲染"""
        patterns = sorted(
            (re.escape(k) for k in self.params.keys()),
            key=len,
            reverse=True,
        )
        regex = re.compile(r'\{\{\{(' + '|'.join(patterns) + r')\}\}\}')
        self.text = regex.sub(lambda match: str(self.params[match.group(1)]), self.text)
        return self


class BasePromptAdd(BaseModel):
    """base prompt 创建模型"""

    name: str
    """base prompt 名称"""

    text: str
    """base prompt 内容"""


class BasePromptGet(BaseModel):
    """base prompt 请求模型"""

    name: str
    """base prompt 名称"""

    params: dict[str, str] = Field(default_factory=dict)
    """
    base prompt 参数表
    
    参数名与 base prompt 中的参数相对应，不需要加入参数标记；
    base prompt 将在实例化时自动完成渲染。
    """


class BasePromptGetAll(BaseModel):
    """base prompt 请求所有模型"""

    params: dict[str, str] = Field(default_factory=dict)
    """
    base prompt 参数表
    
    参数名与 base prompt 中的参数相对应，不需要加入参数标记；
    base prompt 将在实例化时自动完成渲染。
    """


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
    "BasePromptAdd",
    "BasePromptGet",
    "BasePromptGetAll",
    "BasePromptInfo",
    "BasePromptManagerStatus",
]
