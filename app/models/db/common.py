"""定义模型的通用组件"""

from enum import StrEnum
from typing import Union


class Platform(StrEnum):
    """媒体平台枚举"""

    system = 'system'
    '''系统'''

    bilibili = 'bilibili'
    '''Bilibili'''

    douyin = 'douyin'
    '''抖音'''

    tiktok = 'tiktok'
    '''Tiktok'''

    youtube = 'youtube'
    '''Youtube'''

    unknown = 'unknown'
    '''未知平台'''


JSONValue = Union[float, int, str]
'''表模型中 JSON 的键类型'''

__all__ = [
    "Platform",
    "JSONValue",
]
