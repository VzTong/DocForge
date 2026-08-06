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
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import markdown
import re

from app.converters.base import BaseConverter, ConversionError
from app.converters.markdown.ThemeRender import MarkdownTheme
from app.converters.markdown.meta import (
    extract_title_subtitle,
    split_document_header,
)

class MarkdownToPdfConverter(BaseConverter):
    """Convert a Markdown document into PDF."""

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
        self.theme = MarkdownTheme(theme)
        self.title = title
        self.subtitle = subtitle
        self.contact = contact
        self.address = address
        self.links = links

    def _render_html(self, md_text: str, **options: Any) -> str:
        """
        - cv + header đơn giản → tách header vào template CV
        - cv + header phức tạp / document / github → giữ nguyên full Markdown
        """
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

        if theme_name == "cv":
            (
                extracted_title,
                extracted_subtitle,
                extracted_contact,
                extracted_address,
                extracted_links,
                body_md,
            ) = split_document_header(md_text)

            title = title or extracted_title or ""
            subtitle = subtitle or extracted_subtitle or ""
            contact = contact or extracted_contact or ""
            address = address or extracted_address or ""
            links = links or extracted_links or ""
        else:
            body_md = md_text
            if not title:
                extracted_title, _ = extract_title_subtitle(md_text)
                title = extracted_title or ""

        body = markdown.markdown(
            body_md,
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