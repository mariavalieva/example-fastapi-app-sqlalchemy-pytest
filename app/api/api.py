from fastapi import APIRouter

from app.api.endpoints import athlete, medal

api_router = APIRouter()
api_router.include_router(athlete.router, prefix="/athletes", tags=["athletes"])
api_router.include_router(medal.router, prefix="/medals", tags=["medals"])
