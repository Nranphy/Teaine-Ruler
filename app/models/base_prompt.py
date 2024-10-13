from pydantic import BaseModel, model_validator

from app.utils.log import logger


class BasePrompt(BaseModel):
    """base prompt 模型"""

    name: str
    """base prompt 名称"""

    text: str
    """base prompt 内容"""

    params: dict[str, str]
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


__all__ = [
    "BasePrompt",
]
