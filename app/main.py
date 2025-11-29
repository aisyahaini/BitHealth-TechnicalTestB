# import library
from fastapi import FastAPI
from .api.routes import router

# initializing the FastAPI application
app = FastAPI(title="Refactored RAG Demo")
app.include_router(router)