from fastapi import FastAPI

from app.api.routes.base_prompt import router as base_prompt_router
from app.api.routes.corpus import router as corpus_router

app = FastAPI()

app.include_router(base_prompt_router, prefix='/base_prompt')
app.include_router(corpus_router, prefix='/corpus')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
