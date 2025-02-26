from collections import defaultdict
from pydantic import DirectoryPath
from asyncio import Lock
import aiofiles
import hashlib
import json

from app.utils.config import settings
from app.utils.log import logger
from app.models.corpus import *

DATASET_INFO_FILENAME = 'INFO.json'
"""语料数据集信息文件"""

BUCKET_FILE_PREFIX = 'bucket_'
"""语料桶文件前缀"""

bucket_file_lock = defaultdict(Lock)
"""语料桶文件锁"""


class CorpusDatasetManager:
    """语料库数据集管理器"""

    corpus_data_dir: DirectoryPath | None
    """语料库数据目录"""

    def __init__(self):
        self.corpus_data_dir = settings.corpus_data_dir

    def get_info(self, dataset_name: str) -> DatasetInfo:
        if self.corpus_data_dir is None:
            raise ValueError("语料库目录配置项为空。")
        dataset_dir = self.corpus_data_dir / dataset_name
        if not dataset_dir.is_dir():
            raise ValueError(f"语料库目录 {dataset_dir} 不存在。")
        dataset_info_path = dataset_dir / DATASET_INFO_FILENAME
        if not dataset_info_path.is_file():
            raise ValueError(f"语料库目录 {dataset_dir} 中没有 {DATASET_INFO_FILENAME} 文件。")
        return DatasetInfo.model_validate(json.loads(dataset_info_path.read_text(encoding='utf-8-sig')))

    def get_all_info(self) -> list[DatasetInfo]:
        if self.corpus_data_dir is None:
            raise ValueError("语料库目录配置项为空。")
        res = []
        for dir in self.corpus_data_dir.iterdir():
            if not dir.is_dir():
                continue
            try:
                res.append(self.get_info(dir.name))
            except ValueError:
                logger.warning(f"获取语料库 {dir.name} 信息时发生错误。")
        return res

    def create(
        self,
        dataset_name: str,
        description: str = "",
        bucket_num: int = 8,
        exist_ok: bool = False,
    ):
        if self.corpus_data_dir is None:
            raise ValueError("语料库目录配置项为空。")
        dataset_dir = self.corpus_data_dir / dataset_name
        if dataset_dir.is_dir():
            if not exist_ok:
                raise ValueError(f"语料库目录 {dataset_dir} 已存在。")
            else:
                logger.warning(f"语料库目录 {dataset_dir} 已存在，已忽略创建请求。")
                return
        dataset_dir.mkdir(parents=True)
        dataset_info_path = dataset_dir / DATASET_INFO_FILENAME
        dataset_info_path.write_text(
            DatasetInfo(
                name=dataset_name,
                description=description,
                bucket_num=bucket_num,
            ).model_dump_json(),
            encoding='utf-8-sig',
        )
        logger.success(f"语料库 {dataset_name} 创建成功，分桶数为 {bucket_num}。")
        return self.get_info(dataset_name)

    async def add_corpus(self, dataset_name: str, corpus: Corpus):
        if self.corpus_data_dir is None:
            raise ValueError("语料库目录配置项为空。")
        dataset_dir = self.corpus_data_dir / dataset_name
        if not dataset_dir.is_dir():
            raise ValueError(f"语料库目录 {dataset_dir} 不存在。")
        corpus_json_str = corpus.model_dump_json()
        dataset_info = self.get_info(dataset_name)
        bucket_id = int(hashlib.sha256(corpus_json_str.encode('utf-8')).hexdigest(), 16) % dataset_info.bucket_num + 1
        bucket_file_path = dataset_dir / (BUCKET_FILE_PREFIX + str(bucket_id) + '.jsonl')
        async with bucket_file_lock[bucket_file_path]:
            async with aiofiles.open(bucket_file_path, 'a', encoding='utf-8-sig') as f:
                await f.write(corpus_json_str + '\n')
        logger.success(f"数据集 {dataset_name} 语料添加成功，分桶 id 为 {bucket_id}。")


corpus_dataset_manager = CorpusDatasetManager()
"""语料库数据集管理器实例"""

__all__ = [
    "corpus_dataset_manager",
]
