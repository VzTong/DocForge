"""API endpoints cho DocForge_PyService."""
from __future__ import annotations

import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.converters.base import ConversionError
from app.converters.common import PageSize
from app.converters.markdown.md2pdf import MarkdownToPdfConverter
from app.converters.markdown.options import MarkdownThemeOptions
from app.converters.pdf.converter import PdfToDocxConverter
from app.converters.markdown.meta import split_document_header
from app.converters.registry import get_converter, available
from app.core.config import settings

router = APIRouter()

DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


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


class MarkdownPreviewRequest(BaseModel):
    """Request body cho endpoint preview (không cần upload file)."""
    contents: str
    theme: Optional[str] = MarkdownThemeOptions.DOCUMENT.value
    title: Optional[str] = None
    subtitle: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    links: Optional[str] = None
    page_size: Optional[str] = PageSize.A4.value


@router.post("/convert/md-to-pdf", summary="Convert file using specified converter", tags=["md-to-pdf"])
async def md_to_pdf(
    file: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
    filename: Optional[str] = Form(None),
    theme: Optional[str] = Form(MarkdownThemeOptions.DOCUMENT.value),
    title: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    contact: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    links: Optional[str] = Form(None),
    page_size: Optional[str] = Form(PageSize.A4.value),
) -> FileResponse:
    """Nhận file .md hoặc nội dung text và trả về file .pdf."""
    converter = get_converter(MarkdownToPdfConverter.name)
    if converter is None:
        raise HTTPException(status_code=500, detail="Unregistered converter")

    # Xác định nguồn nội dung: file upload hoặc text thuần
    if file:
        if not (file.filename or "").lower().endswith((".md", ".markdown")):
            raise HTTPException(status_code=400, detail="Only accepts .md/.markdown files.")
        job_dir = settings.work_dir / uuid.uuid4().hex
        input_path = _save_uploaded_file(file, job_dir)
        md_text = input_path.read_text(encoding="utf-8")
    elif content:
        if not content.strip():
            raise HTTPException(status_code=400, detail="Content is empty.")
        job_dir = settings.work_dir / uuid.uuid4().hex
        md_text = content
    else:
        raise HTTPException(status_code=400, detail="Either 'file' or 'content' is required.")

    try:
        # Chỉ trích metadata cho options — KHÔNG cắt body
        extracted_title, extracted_subtitle, extracted_contact, extracted_address, extracted_links, _ = (
            split_document_header(md_text)
        )

        # Truyền các tùy chọn render vào converter
        options = {
            "theme": theme,
            "title": title or extracted_title,
            "subtitle": subtitle or extracted_subtitle,
            "contact": contact or extracted_contact,
            "address": address or extracted_address,
            "links": links or extracted_links,
            "page_size": page_size,
            "filename": filename or "output",
        }
        # FULL text
        pdf_path = converter.convert_from_text(md_text, job_dir / "out", **options)
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=pdf_path.name,
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.post("/preview/md-to-pdf", summary="Preview PDF from raw markdown text", tags=["md-to-pdf"])
async def preview_md_to_pdf(request: MarkdownPreviewRequest) -> FileResponse:
    """Nhận text Markdown (không cần upload file) và trả về file .pdf."""
    converter = get_converter(MarkdownToPdfConverter.name)

    # Đảm bảo converter có hỗ trợ convert_from_text
    if not isinstance(converter, MarkdownToPdfConverter):
        raise HTTPException(status_code=500, detail="Invalid converter configuration")

    job_dir = settings.work_dir / uuid.uuid4().hex
    try:
        # Chỉ trích metadata cho options — KHÔNG cắt body
        extracted_title, extracted_subtitle, extracted_contact, extracted_address, extracted_links, _ = (
            split_document_header(request.contents)
        )

        data = request.model_dump()
        data.pop("contents")

        # Nếu người dùng nhập riêng title/subtitle/contact thì ưu tiên các giá trị đó.
        # Nếu không nhập, fallback sang metadata trong Markdown.
        if data.get("title") in (None, "") and extracted_title:
            data["title"] = extracted_title
        if data.get("subtitle") in (None, "") and extracted_subtitle:
            data["subtitle"] = extracted_subtitle
        if data.get("contact") in (None, "") and extracted_contact:
            data["contact"] = extracted_contact
        if data.get("address") in (None, "") and extracted_address:
            data["address"] = extracted_address
        if data.get("links") in (None, "") and extracted_links:
            data["links"] = extracted_links
        if data.get("page_size") in (None, ""):
            data["page_size"] = request.page_size

        # FULL text
        pdf_path = converter.convert_from_text(request.contents, job_dir / "out", **data)
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=pdf_path.name,
            content_disposition_type="inline",
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    

def _save_uploaded_file(upload_file: UploadFile, out_dir: Path) -> Path:
    """Lưu file upload vào thư mục tạm thời và trả về Path tới file đó. Kiểm tra kích thước file."""
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

@router.post(
    "/convert/pdf-to-docx",
    summary="Convert PDF to DOCX",
    tags=["pdf-to-docx"],
    response_class=FileResponse,
    responses={
        400: {"description": "Bad Request"},
        413: {"description": "File too large"},
        422: {"description": "Conversion Error"},
    },
)
def pdf_to_docx(
    file: UploadFile = File(..., description="PDF file to convert"),
    start_page: Optional[str] = Form(None, description="Start page (0-indexed)"),
    end_page: Optional[str] = Form(None, description="End page (exclusive)"),
) -> FileResponse:
    """Chuyển PDF sang Word, giữ layout và định dạng. Trả về file .docx."""
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only accepts .pdf files.")

    # Xử lý chuỗi rỗng → None
    def _parse_page(value: Optional[str]) -> Optional[int]:
        if value is None or str(value).strip() == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail=f"Invalid page number: '{value}'")

    start = _parse_page(start_page)
    end = _parse_page(end_page)

    converter = get_converter(PdfToDocxConverter.name)
    if converter is None:
        raise HTTPException(status_code=500, detail="Unregistered converter")

    job_dir = settings.work_dir / uuid.uuid4().hex
    try:
        input_path = _save_uploaded_file(file, job_dir)
        output_path = converter.convert(
            input_file=input_path,
            output_file=job_dir / "out",
            start_page=start,
            end_page=end,
        )
        return FileResponse(
            path=output_path,
            media_type=DOCX_MEDIA_TYPE,
            filename=output_path.name,
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e