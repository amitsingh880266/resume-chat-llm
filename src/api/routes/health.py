from fastapi import APIRouter

from src.api.schemas.health_response import HealthResponse

router = APIRouter(
    tags = ["Health"]
)

@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}