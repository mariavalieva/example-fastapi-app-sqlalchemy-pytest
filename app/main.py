from typing import Any, Awaitable

from fastapi import FastAPI
from starlette.requests import Request

from app import settings
from app.api.api import api_router
from app.db import SessionLocal


def get_application() -> FastAPI:
    tags_metadata = [
        {"name": "athletes", "description": "Operations with athletes"},
        {"name": "medals", "description": "Operations with medals"},
    ]
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        root_path=settings.API_PREFIX,
        docs_url="/",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        description="Information about Olympic Games Medalists (years 2000+)",
        openapi_tags=tags_metadata,
    )
    application.include_router(api_router)
    return application


app = get_application()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next: Any) -> Awaitable[Any]:
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
