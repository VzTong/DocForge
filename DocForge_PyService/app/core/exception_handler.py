"""Global exception handler cho DocForge_PyService.

Bắt tất cả exception không được xử lý và log chi tiết ra console/file.
"""
from __future__ import annotations

import logging
import traceback
from datetime import datetime
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# Cấu hình logger
logger = logging.getLogger("docforge")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)
logger.addHandler(console_handler)


def log_exception(exc: Exception, context: str = "") -> None:
    """Log exception chi tiết kèm stack trace."""
    timestamp = datetime.now().isoformat()
    logger.error(
        f"[{timestamp}] Exception in {context or 'unknown context'}: {type(exc).__name__}: {exc}"
    )
    logger.debug(f"Stack trace:\n{''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))}")


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Xử lý HTTPException - log và trả về response chuẩn."""
    log_exception(exc, f"HTTP {request.method} {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Xử lý RequestValidationError - log chi tiết validation errors."""
    log_exception(exc, f"Validation {request.method} {request.url.path}")
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Validation error", "details": errors},
    )


async def pydantic_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Xử lý ValidationError từ Pydantic."""
    log_exception(exc, f"Pydantic {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "Data validation error", "details": exc.errors()},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Bắt tất cả exception còn lại - log full stack trace."""
    log_exception(exc, f"Unhandled {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)},
    )


def register_exception_handlers(app: Any) -> None:
    """Đăng ký tất cả exception handlers vào FastAPI app."""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)