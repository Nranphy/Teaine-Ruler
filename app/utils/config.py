from pydantic import DirectoryPath, model_validator, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
)
from functools import lru_cache
from pathlib import Path

from .log import logger


class Settings(BaseSettings):
    """全局配置类"""

    data_dir: DirectoryPath = Path(__file__).parent.parent / 'data'
    """数据目录"""

    base_prompt_data_dir: DirectoryPath | None = None
    """base prompt 数据目录"""

    corpus_data_dir: DirectoryPath | None = None
    """微调语料库数据目录"""

    db_url: PostgresDsn | None = None
    """
    PostgreSQL 的 URL 路径
    
    期望格式：postgresql://[name]:[password]@[host]:[post]/[database]
    """

    model_config = SettingsConfigDict(
        json_file=Path(__file__).parent.parent / 'setting.json',
        json_file_encoding='utf-8-sig',
    )

    @model_validator(mode='after')
    def data_dir_validator(self):
        if self.base_prompt_data_dir is None and (
            (self.data_dir / 'base_prompt').is_dir() or not (self.data_dir / 'base_prompt').exists()
        ):
            self.base_prompt_data_dir = self.data_dir / 'base_prompt'
        if self.corpus_data_dir is None and (
            (self.data_dir / 'corpus').is_dir() or not (self.data_dir / 'corpus').exists()
        ):
            self.corpus_data_dir = self.data_dir / 'corpus'
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )


@lru_cache
def get_settings(*args, **kwargs) -> Settings:
    """构建配置实例，可自定义参数，所构建实例与全局配置实例不为同一对象"""
    settings = Settings(*args, **kwargs)
    logger.debug("新生成配置实例内容如下：" + settings.model_dump_json())
    return settings


def refresh_settings() -> Settings:
    """刷新全局配置实例，这将重新读取配置文件"""
    global settings
    settings = get_settings()
    logger.debug("全局配置实例刷新完成。")
    return settings


settings: Settings = get_settings()
"""全局配置实例"""

__all__ = [
    'settings',
    'get_settings',
    'refresh_settings',
]
