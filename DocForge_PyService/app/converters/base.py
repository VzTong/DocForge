"""Interface chung cho mọi converter.
Strategy pattern: mỗi converter sẽ implement interface này. Để dễ thêm loại chuyển đổi mới (pdf->docx, docx->pdf, html->pdf, html->docx, ...), chỉ cần implement interface này và thêm vào factory mà không sửa code cũ (Open/Closed Principle - SOLID)."""
from __future__ import annotations

import abc
from pathlib import Path

class ConversionError(Exception):
    """Lỗi nghiệp vụ khi chuyển đổi file. Ví dụ: file không hợp lệ, file bị hỏng, file không đọc được, thiếu dependencies ..."""

class BaseConverter(abc.ABC):
    #: Mã định danh loại converter, ví dụ: "pdf2docx", "docx2pdf", "html2pdf", "md2pdf"...
    name: str = "base"

    @abc.abstractmethod
    def convert(self, input_file: Path, out_dir: Path, **options: Any) -> Path:
        """Chuyển đổi file input_file sang định dạng khác, lưu vào thư mục out_dir.
        Trả về path của file output.
        Raise ConversionError nếu có lỗi nghiệp vụ (file không hợp lệ, file bị hỏng, file không đọc được, thiếu dependencies ...)
        `options` là các tùy chọn bổ sung riêng của từng converter
        (VD: md-to-pdf có thể có theme, title, subtitle, contact; pdf-to-docx có thể có page_range, ...). Converter cụ thể sẽ tự định nghĩa các tùy chọn này. (Không dùng có thể bỏ qua)
        """
        raise NotImplementedError