"""Global exception handler cho DocForge_PyService.

Bắt exception không được xử lý, log chi tiết.
Response luôn dùng key `detail` (chuẩn FastAPI) để FE đọc được.
"""
from __future__ import annotations

import logging
import traceback
from datetime import datetime

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger("docforge")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(console_handler)


def log_exception(exc: Exception, context: str = "") -> None:
    """Log exception kèm stack trace."""
    timestamp = datetime.now().isoformat()
    logger.error(
        f"[{timestamp}] Exception in {context or 'unknown'}: "
        f"{type(exc).__name__}: {exc}"
    )
    logger.debug(
        "Stack trace:\n"
        + "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTPException → JSON { detail, status_code } (chuẩn FastAPI)."""
    log_exception(exc, f"HTTP {request.method} {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,  # FE + OpenAPI đọc field này
            "status_code": exc.status_code,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Lỗi validate body/query → 422 + detail dạng list FastAPI."""
    log_exception(exc, f"Validation {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


async def pydantic_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    log_exception(exc, f"Pydantic {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Mọi exception khác → 500, vẫn trả detail string."""
    log_exception(exc, f"Unhandled {request.method} {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": f"{type(exc).__name__}: {exc}",
            "status_code": 500,
        },
    )


def register_exception_handlers(app) -> None:
    """Gọi từ app.main sau khi tạo FastAPI()."""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, pydantic_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)