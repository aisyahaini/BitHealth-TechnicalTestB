from fastapi import FastAPI
from .api.routes import router
app = FastAPI(title="Refactored RAG Demo")
app.include_router(router)