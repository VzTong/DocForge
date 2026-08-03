"""Registy gom các converter theo tên.
Thêm converter mới: chỉ cần implement BaseConverter và thêm vào registry này.(Không sửa API layer)"""
from __future__ import annotations

from app.converters.base import BaseConverter
from app.converters.markdown.md2pdf import MarkdownToPdfConverter

_CONVERTER_REGISTRY: dict[str, BaseConverter] = {
    c.name: c() for c in (
        MarkdownToPdfConverter,
    )
    # MarkdownToPdfConverter.name: MarkdownToPdfConverter()
    # TODO phase sau:
    # pdfToDocxConverter.name: PdfToDocxConverter(),
    # docxToPdfConverter.name: DocxToPdfConverter(),
}

def get_converter(name: str) -> BaseConverter | None:
    """Lấy converter theo tên. Raise ValueError nếu không tìm thấy."""
    if name not in _CONVERTER_REGISTRY:
        raise ValueError(f"Converter '{name}' not found.")
    return _CONVERTER_REGISTRY.get(name)

def available() -> list[str]:
    return sorted(_CONVERTER_REGISTRY.keys())