"""API endpoints cho DocForge_PyService."""
from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app.converters.base import ConversionError
from app.converters.md2pdf import MarkdownToPdfConverter
from app.converters.registry import get_converter, available
from app.core.config import settings

router = APIRouter()

@router.get("/health", summary="Health check endpoint")
async def health_check() -> dict:
    """Health check endpoint. Trả về 200 OK nếu service đang chạy."""
    return {"status": "ok"}

@router.get("/converters", summary="List available converters")
async def list_converters() -> dict:
    """Liệt kê các converter có sẵn."""
    return {"available_converters": available()}

def _save_uploaded_file(upload_file: UploadFile, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / (upload_file.filename or f"input_{uuid.uuid4().hex}")
    size = 0
    with dest.open("wb") as f:
        while chunk := upload_file.file.read(1024 * 1024):  # 1MB chunk
            size += len(chunk)
            if size > settings.max_file_size:
                f.close()
                shutil.rmtree(out_dir, ignore_errors=True)  # Clean up the directory
                raise HTTPException(status_code=413, detail="File too large")
            f.write(chunk)
    return dest

@router.post("/convert/md-to-pdf", summary="Convert file using specified converter")
async def md_to_pdf(file: UploadFile = File(...)) -> FileResponse:
    """Nhận file .md và trả về file .pdf."""
    converter = get_converter(MarkdownToPdfConverter.name)
    if converter is None:
        raise HTTPException(status_code=500, detail="Unregistered converter")

    if not (file.filename or "").lower().endswith((".md", ".markdown")):
        raise HTTPException(status_code=400, detail="Only accepts .md/.markdown files.")

    job_dir = settings.work_dir / uuid.uuid4().hex
    try:
        input_path = _save_uploaded_file(file, job_dir)
        pdf_path = converter.convert(input_path, job_dir / "out")
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=pdf_path.name
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    # Dọn job_dir: để backgroundTask/scheduler ở phase sau (tránh xóa trước khi strem xong)