from fastapi import APIRouter, HTTPException

from app.common.models.corpus import *
from app.core.corpus import corpus_dataset_manager

router = APIRouter()


@router.get('/info', response_model=list[DatasetInfo])
async def _():
    try:
        return corpus_dataset_manager.get_all_info()
    except ValueError as e:
        raise HTTPException(403, *e.args)


@router.get('/info/{dataset_name}', response_model=DatasetInfo)
async def _(dataset_name: str):
    try:
        return corpus_dataset_manager.get_info(dataset_name)
    except ValueError as e:
        raise HTTPException(403, *e.args)


@router.post('/create', response_model=DatasetInfo)
async def _(model: DatasetInfo):
    try:
        return corpus_dataset_manager.create(model.name, model.description, model.bucket_num)
    except ValueError as e:
        raise HTTPException(403, *e.args)


@router.post('/add', response_model=DatasetInfo)
async def _(model: CorpusAdd):
    try:
        info = corpus_dataset_manager.get_info(model.dataset_name)
    except ValueError as e:
        raise HTTPException(403, *e.args)
    await corpus_dataset_manager.add_corpus(model.dataset_name, model.corpus)
    return info
