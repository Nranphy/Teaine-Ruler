from pydantic import DirectoryPath
import re

from app.models.base_prompt import BasePrompt
from app.core.config import settings
from app.utils.log import logger


class BasePromptManager:
    """base prompt 管理器"""

    base_prompt_data_dir: DirectoryPath | None
    """base prompt 数据目录"""

    base_prompt_map: dict[str, str]
    """base prompt 名称内容映射表"""

    def __init__(self):
        self.base_prompt_map = dict()
        self.refresh(refresh_data_dir=True)

    def refresh(self, refresh_data_dir: bool = False):
        if refresh_data_dir:
            self.base_prompt_data_dir = settings.base_prompt_data_dir
        self.base_prompt_map.clear()

        if self.base_prompt_data_dir is None:
            logger.warning('base prompt 目录配置项为空。')
            return

        for file_name in self.base_prompt_data_dir.iterdir():
            if not file_name.name.endswith('.txt'):
                continue
            self.base_prompt_map[file_name.name.removesuffix('.txt')] = \
                file_name.read_text(encoding='utf-8-sig').strip()

        logger.success("base prompt 更新成功。")
        if len(self.base_prompt_map) > 0:
            logger.debug(
                "当前 base prompt 内容概述如下：" + '[' + (
                    ', '.join(
                        f'<名称:{name}, 文本长:{len(text)}, 参数量:{len(re.findall(r"{{{[A-Za-z]+?}}}", text))}>'
                        for name, text in self.base_prompt_map.items()
                    )
                ) + '].'
            )
        else:
            logger.debug('当前无 base prompt 内容。')

    def get(self, name: str, params: dict[str, str], refresh: bool = False) -> BasePrompt:
        if refresh:
            self.refresh()
        base_prompt = self.base_prompt_map.get(name)
        if base_prompt is None:
            return BasePrompt(name=name, text='', params=params)
        return BasePrompt(name=name, text=base_prompt, params=params)

    def add(self, name: str, text: str):
        if self.base_prompt_data_dir is None:
            raise FileNotFoundError('base prompt 目录配置项为空。')
        file_path = self.base_prompt_data_dir / f'{name}.txt'
        file_path.write_text(text, encoding='utf-8-sig')
        self.refresh()

    def get_all(self, params: dict[str, str], refresh: bool = False) -> list[BasePrompt]:
        if refresh:
            self.refresh()
        return [self.get(name, params) for name in self.base_prompt_map.keys()]


base_prompt_manager = BasePromptManager()
"""base prompt 管理器实例"""

__all__ = [
    "base_prompt_manager",
]
