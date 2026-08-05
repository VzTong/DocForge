"""
Markdown -> PDF converter using WeasyPrint.

Pipeline:
    Markdown
        ↓
    HTML (markdown package)
        ↓
    Apply Theme (HTML Template + CSS)
        ↓
    WeasyPrint
        ↓
    PDF

Design:
- Markdown parsing is handled by the `markdown` package.
- HTML rendering is delegated to `MarkdownTheme`.
- PDF generation is delegated to WeasyPrint.
- Theme (HTML/CSS) is completely separated from the converter so new themes
  can be added without modifying this file.

Notes:
- WeasyPrint requires several native libraries (Pango, Cairo, GDK-PixBuf, libffi, ...).
- On Windows: install GTK3 Runtime.
- On Linux/Docker: install the required system packages before running.
---
Thiết kế:
- Việc phân tích cú pháp Markdown được thực hiện bởi gói `markdown`.
- Việc kết xuất (render) HTML được giao cho `MarkdownTheme`.
- Việc tạo PDF được giao cho WeasyPrint.
- Giao diện (HTML/CSS) được tách biệt hoàn toàn khỏi bộ chuyển đổi, nhờ đó có thể
  thêm giao diện mới mà không cần sửa đổi tệp này.

Lưu ý:
- WeasyPrint yêu cầu một số thư viện hệ thống (Pango, Cairo, GDK-PixBuf, libffi, ...).
- Trên Windows: cài đặt GTK3 Runtime.
- Trên Linux/Docker: cài đặt các gói hệ thống cần thiết trước khi chạy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import markdown
import re

from app.converters.base import BaseConverter, ConversionError
from app.converters.markdown.ThemeRender import MarkdownTheme

class MarkdownToPdfConverter(BaseConverter):
    """
    Convert a Markdown document into PDF.

    Responsibilities:
        1. Read Markdown source.
        2. Convert Markdown -> HTML.
        3. Apply selected HTML/CSS theme.
        4. Generate PDF using WeasyPrint.

    This class intentionally knows nothing about:
        - HTML template structure.
        - CSS styling.
        - Theme loading.

    Those responsibilities belong to `MarkdownTheme`.
    """

    name = "md-to-pdf"

    def __init__(
        self,
        theme: str = "cv",
        title: str = "",
        subtitle: str = "",
        contact: str = "",
        address: str = "",
        links: str = "",
    ) -> None:
        """
        Initialize the Markdown converter.

        Args:
            theme:
                Name of the rendering theme.
                Example: "modern", "github", "cv".

            title:
                HTML document title.  For the CV theme this is
                typically the person's name.

            subtitle:
                Optional subtitle (e.g. job title).  Used by the
                CV theme template.

            contact:
                Optional contact info (e.g. email / phone).
                Used by the CV theme template.

            address:
                Optional address line shown below contact.

            links:
                Optional profile links line shown below address.
        """

        self.theme = MarkdownTheme(theme)
        self.title = title
        self.subtitle = subtitle
        self.contact = contact
        self.address = address
        self.links = links

    def _render_html(self, md_text: str, **options: Any) -> str:
        """
        Convert Markdown into a complete HTML document.
        """
        # Cho phép options đè lên các giá trị khởi tạo
        theme_name = options.get("theme", self.theme.name)
        title = options.get("title", self.title)
        subtitle = options.get("subtitle", self.subtitle)
        contact = options.get("contact", self.contact)
        address = options.get("address", self.address)
        links = options.get("links", self.links)
        page_size = options.get("page_size", "A4")

        # Nếu theme trong options khác với theme hiện tại, tạo renderer mới
        renderer = self.theme
        if theme_name != self.theme.name:
            renderer = MarkdownTheme(theme_name)

        body = markdown.markdown(
            md_text,
            extensions=[
                "tables",
                "fenced_code",
                "nl2br",
            ],
        )

        def render_inline_markdown(text: str | None) -> str:
            if not text:
                return ""
            rendered = markdown.markdown(text, extensions=["nl2br"])
            match = re.fullmatch(r"<p>(.*)</p>", rendered, flags=re.S)
            return match.group(1) if match else rendered

        return renderer.render(
            title=title,
            subtitle_html=render_inline_markdown(subtitle),
            contact_html=render_inline_markdown(contact),
            address_html=render_inline_markdown(address),
            links_html=render_inline_markdown(links),
            page_size=page_size,
            body=body,
        )

    def convert_from_text(self, md_text: str, out_dir: Path, **options: Any) -> Path:
        """
        Chuyển đổi trực tiếp từ text Markdown sang PDF.
        """
        try:
            from weasyprint import HTML
        except OSError as e:
            raise ConversionError(f"WeasyPrint import failed: {e}") from e

        print(f"Converting Markdown to PDF using theme '{options.get('theme', self.theme.name)}'...")
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = options.get("filename", "output")
        pdf_path = out_dir / f"{filename}.pdf"

        # Markdown -> HTML
        html = self._render_html(md_text, **options)

        # HTML -> PDF
        try:
            HTML(string=html).write_pdf(str(pdf_path))
        except Exception as e:
            raise ConversionError(f"Failed to generate PDF: {e}") from e

        return pdf_path

    def convert(self, input_path: Path, out_dir: Path, **options: Any) -> Path:
        """
        Convert a Markdown file into PDF.
        """
        try:
            md_text = input_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ConversionError(f"Failed to read '{input_path}'.") from e

        # Sử dụng lại logic convert_from_text
        if "filename" not in options:
            options["filename"] = input_path.stem

        return self.convert_from_text(md_text, out_dir, **options)