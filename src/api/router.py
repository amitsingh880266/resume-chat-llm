from fastapi import APIRouter

from src.api.routes.health import router as health_router
from src.api.routes.questions import router as questions_router
from src.api.routes.documents import router as documents_router

router = APIRouter()

router.include_router(health_router)
router.include_router(questions_router)
router.include_router(documents_router)