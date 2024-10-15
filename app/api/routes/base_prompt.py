from fastapi import APIRouter, HTTPException

from app.models.base_prompt import (
    BasePromptManagerStatus,
    BasePromptGetAll,
    BasePromptGet,
    BasePromptAdd,
    BasePrompt,
)
from app.core.base_prompt import base_prompt_manager

router = APIRouter()


@router.get('/status', response_model=BasePromptManagerStatus)
async def _():
    return base_prompt_manager.status()


@router.get('/refresh', response_model=BasePromptManagerStatus)
async def _():
    return base_prompt_manager.status(refresh=True)


@router.post('/get', response_model=BasePrompt)
async def _(model: BasePromptGet):
    try:
        return base_prompt_manager.get(name=model.name, params=model.params)
    except ValueError as e:
        raise HTTPException(403, *e.args)


@router.post('/get_all', response_model=list[BasePrompt])
async def _(model: BasePromptGetAll):
    try:
        return base_prompt_manager.get_all(params=model.params)
    except ValueError as e:
        raise HTTPException(403, *e.args)


@router.post('/add', response_model=BasePromptManagerStatus)
async def _(model: BasePromptAdd):
    try:
        base_prompt_manager.add(name=model.name, text=model.text)
        return base_prompt_manager.status()
    except ValueError as e:
        raise HTTPException(403, *e.args)
