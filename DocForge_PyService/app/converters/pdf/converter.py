"""PDF -> DOCX converter. Dùng pdf2docx để convert PDF sang DOCX (Thuần Python, không cần cài đặt MS Word)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from app.converters.base import BaseConverter, ConversionError

class PdfToDocxConverter(BaseConverter):
    name = "pdf-to-docx"

    def convert(self, input_file: Path, output_file: Path, **options: Any) -> Path:
        """Chuyển PDF sang DOCX.

        options:
            - start_page (int): Trang bắt đầu (mặc định là 0)
            - end_page (int | None): Trang kết thúc (không bao gồm), None = hết file
        """
        try:
            from pdf2docx import Converter
        except ImportError as e:
            raise ConversionError("pdf2docx is not installed. Please install it to use this converter.") from e

        start_page = options.get("start_page", 0)
        end_page = options.get("end_page", None)

        if start_page is None:
            start_page = 0

        # === SỬA Ở ĐÂY ===
        output_file.mkdir(parents=True, exist_ok=True)          # tạo thư mục "out"
        docx_path = output_file / f"{input_file.stem}.docx"

        cv = None
        try:
            cv = Converter(str(input_file))

            convert_kwargs = {
                "start": start_page,
                "multi_processing": False,
                "cpu_count": 1,
            }
            if end_page is not None:
                convert_kwargs["end"] = end_page

            cv.convert(str(docx_path), **convert_kwargs)

        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "password" in msg.lower():
                raise ConversionError("The PDF file is password protected. Please provide a valid PDF file.") from e
            elif "not a pdf" in msg.lower():
                raise ConversionError("The input file is not a valid PDF file. Please provide a valid PDF file.") from e
            elif "failed to read" in msg.lower():
                raise ConversionError("Failed to read the PDF file. It may be corrupted or in an unsupported format.") from e
            else:
                raise ConversionError(f"An error occurred during conversion: {msg}") from e
        finally:
            if cv is not None:
                cv.close()

        if not docx_path.exists():
            raise ConversionError("Conversion failed: DOCX file was not created.")
        return docx_path