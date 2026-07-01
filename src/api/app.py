from fastapi import FastAPI

from src.api.routes.health import router as health_router

from src.api.router import router

app = FastAPI(
    title="Document Chat LLM API",
    version = "0.1.0",
    description = "API for interacting with documents using a chat-based LLM.",
)

app.include_router(router)
