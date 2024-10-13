from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
)
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """全局配置类"""

    model_config = SettingsConfigDict(
        json_file=Path(__file__).parent.parent / 'setting.json',
        json_file_encoding='UTF-8-sig'
    )

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
    return Settings(*args, **kwargs)


def refresh_settings() -> Settings:
    """刷新全局配置实例，这将重新读取配置文件"""
    global settings
    settings = get_settings()
    return settings


settings = get_settings()
"""全局配置实例"""

__all__ = [
    'settings',
    'get_settings',
    'refresh_settings',
]
