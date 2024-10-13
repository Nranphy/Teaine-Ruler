from fastapi import FastAPI

from app.api.routes.base_prompt import router as base_prompt_router

app = FastAPI()

app.include_router(base_prompt_router, prefix='/base_prompt')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
