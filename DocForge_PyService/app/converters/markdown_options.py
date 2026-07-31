"""
Configuration models used by Markdown converters.

Centralizes theme names and rendering options to avoid hard-coded strings
throughout the converter implementation.
---
Các mô hình cấu hình được sử dụng bởi các bộ chuyển đổi Markdown.

Tập ​​trung hóa tên giao diện và các tùy chọn hiển thị để tránh việc mã hóa cứng (hard-code) các chuỗi văn bản trong toàn bộ quá trình triển khai bộ chuyển đổi.
"""

from enum import Enum

class MarkdownThemeOptions(str, Enum):
    """Built-in themes supported by the Markdown renderer."""

    DOCUMENT = "document"
    GITHUB = "github"
    CV = "cv"


class PageSize(str, Enum):
    """Supported PDF page sizes."""

    A4 = "A4"
    LETTER = "Letter"