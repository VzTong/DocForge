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

import markdown

from app.converters.base import BaseConverter, ConversionError
from app.converters.MarkdownThemeRenderer import MarkdownTheme

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
        theme: str = "document",
        title: str = "Document",
        subtitle: str = "",
        contact: str = "",
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
        """

        self.theme = MarkdownTheme(theme)
        self.title = title
        self.subtitle = subtitle
        self.contact = contact

    def _render_html(self, md_text: str) -> str:
        """
        Convert Markdown into a complete HTML document.

        The rendering process consists of two stages:

        1. Parse Markdown into HTML fragments.
        2. Apply the selected theme (HTML template + CSS).

        This method does NOT generate the PDF.
        It only prepares the final HTML for WeasyPrint.

        Args:
            md_text:
                Raw Markdown content.

        Returns:
            Complete HTML document.
        """

        body = markdown.markdown(
            md_text,
            extensions=[
                "tables",
                "fenced_code",
                "nl2br",
            ],
        )

        return self.theme.render(
            title=self.title,
            body=body,
            subtitle=self.subtitle,
            contact=self.contact,
        )

    def convert(self, input_path: Path, out_dir: Path) -> Path:
        """
        Convert a Markdown file into PDF.

        Args:
            input_path:
                Source Markdown file.

            out_dir:
                Directory where the generated PDF will be stored.

        Returns:
            Path to the generated PDF.

        Raises:
            ConversionError:
                If the source cannot be read,
                WeasyPrint cannot be initialized,
                or PDF generation fails.
        """

        # Import lazily so the service can still start even if
        # WeasyPrint system dependencies are not installed.
        try:
            from weasyprint import HTML

        except OSError as e:
            raise ConversionError(
                "WeasyPrint import failed.\n"
                "Please ensure required system libraries are installed.\n"
                "Windows : GTK3 Runtime.\n"
                "Linux   : libpango, cairo, gdk-pixbuf, libffi.\n\n"
                f"Original error: {e}"
            ) from e

        # Read Markdown source.
        try:
            md_text = input_path.read_text(
                encoding="utf-8"
            )

        except Exception as e:  # noqa: BLE001
            raise ConversionError(
                f"Failed to read '{input_path}'."
            ) from e

        out_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        pdf_path = out_dir / f"{input_path.stem}.pdf"

        # Markdown -> HTML
        html = self._render_html(md_text)

        # HTML -> PDF
        try:
            HTML(string=html).write_pdf(str(pdf_path))

        except Exception as e:  # noqa: BLE001
            raise ConversionError(
                f"Failed to generate PDF: {e}"
            ) from e

        if not pdf_path.exists():
            raise ConversionError(
                f"PDF was not created: {pdf_path}"
            )

        return pdf_path