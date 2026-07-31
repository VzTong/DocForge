"""Entry point FastAPI cho DocForge_PyService."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version=settings.version
    )

# CORS middleware cho phép DocForge_FE (Vue) gọi (chỉnh origin cụ thể ở production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO prod: đặt domain FE cụ thể
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"service": settings.app_name, "version": settings.version, "docs": "/docs"}