"""Test cơ bản cho DocForge_PyService (Phase 0 - khung test)

Chạy project: pytest -v (từ thư mục DocForge_PyService)
Không cần Chrome: kiểm tra health, listing, render HTML, và các nhánh lỗi"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.converters.md2pdf import MarkdownToPdfConverter
from app.main import app

from pathlib import Path

client = TestClient(app)

SAMPLE_MD = """# CV\n\n| Kỹ năng | Mức độ |\n| --- | --- |\n| Python | 5/5 |\n| FastAPI | 4/5 |\n\n## Kinh nghiệm\n- Công ty A: 2020-2022\n- Công ty B: 2022-2024\n\n```python\nprint("Hello World")\n```"""

SAMPLE_MD_PATH = Path(__file__).parent / "fixtures" / "sample.md"

SAMPLE_CV_MD_PATH = Path(__file__).parent / "fixtures" / "samplecv.md"

SAMPLE_CV_MD = SAMPLE_CV_MD_PATH.read_text(encoding="utf-8")


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_list_converters():
    """Test listing available converters."""
    response = client.get("/converters")
    assert response.status_code == 200
    data = response.json()
    assert "available_converters" in data
    assert MarkdownToPdfConverter.name in data["available_converters"]

def test_render_html_keeps_table_and_code_block():
    """Test render HTML giữ nguyên table và code block."""
    converter = MarkdownToPdfConverter()
    html_content = converter._render_html(SAMPLE_MD)
    # Kiểm tra table
    assert "<table>" in html_content
    assert "<th>Kỹ năng</th>" in html_content
    # Kiểm tra code block
    assert "<pre><code class=\"language-python\">" in html_content

def test_convert_reject_wrong_filetype():
    """Test convert từ file không phải Markdown."""
    response = client.post(
        "/convert/md-to-pdf",
        files={"file": ("test.exe", b"bad", "application/octet-stream")},
    )
    assert response.status_code == 400

def test_convert_md_return_pdf_or_442():
    """Nếu WeasyPrint + lib hệ thống đầy đủ -> 200 PDF, nếu thiếu lib hệ thống -> 422 (WeasyPrint error)"""
    response = client.post(
        "/convert/md-to-pdf",
        files={"file": ("testcv.md", SAMPLE_MD.encode("utf-8"), "text/markdown")},
    )
    assert response.status_code in (200, 422)
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/pdf"

# def test_debug_show_html():
#     """Test tạm để nhìn HTML render ra - mở file bằng trình duyệt."""

#     # html = MarkdownToPdfConverter()._render_html(SAMPLE_MD)
#     # Lấy đường dẫn tuyệt đối của file hiện tại
#     current_dir = Path(__file__).parent

#     # Tạo đường dẫn đến file sample.md
#     sample_md_path = current_dir / "fixtures" / "sample.md"

#     # Đọc nội dung file
#     with open(sample_md_path, "r", encoding="utf-8") as f:
#         md_content = f.read()#     # Truyền vào converter
#     html = MarkdownToPdfConverter()._render_html(md_content)

#     # Thư mục fixtures nằm cùng cấp với test_api.py
#     fixtures_dir = Path(__file__).parent / "fixtures"
#     fixtures_dir.mkdir(exist_ok=True)

#     output_file = fixtures_dir / "debug_output.html"
#     output_file.write_text(html, encoding="utf-8")

#     print(f"\n=== Đã ghi HTML vào: {output_file.resolve()} ===")
#     print(html[:300])  # In 300 ký tự đầu

def _read_md() -> str:
    # Đọc nội dung file
    with open(SAMPLE_MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()
    return md_content

def _write_debug_html(theme: str, html: str) -> Path:
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)
    output_file = fixtures_dir / f"debug_output_{theme}.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"\n=== Đã ghi HTML ({theme}) vào: {output_file.resolve()} ===")
    return output_file


def test_render_document_theme():
    """Test render Markdown sang HTML với theme document."""
    md_content = _read_md()
    converter = MarkdownToPdfConverter(theme="document", title="Test Document")
    html = converter._render_html(md_content)
    out_file = _write_debug_html("document", html)
    assert out_file.exists()
    assert "<html" in html.lower()


def test_render_github_theme():
    """Test render Markdown sang HTML với theme github."""
    md_content = _read_md()
    converter = MarkdownToPdfConverter(theme="github", title="Test Github")
    html = converter._render_html(md_content)
    out_file = _write_debug_html("github", html)
    assert out_file.exists()
    assert "<html" in html.lower()


def test_render_cv_theme():
    """Test render Markdown sang HTML với theme cv (resume style)."""
    md_content = _read_md()
    converter = MarkdownToPdfConverter(
        theme="cv",
        title="Nguyễn Văn A",
        subtitle="Backend Developer",
        contact="email@example.com  |  0909 123 456",
    )
    html = converter._render_html(md_content)
    out_file = _write_debug_html("cv", html)
    assert out_file.exists()
    assert "<html" in html.lower()
    assert "cv-container" in html
    assert "cv-header" in html
    assert "cv-body" in html
    assert "<h1>Nguyễn Văn A</h1>" in html


def test_cv_theme_render_html():
    """Test CV theme render HTML có header (tên, chức danh, contact) và body."""
    converter = MarkdownToPdfConverter(
        theme="cv",
        title="Nguyễn Văn A",
        subtitle="Backend Developer",
        contact="email@example.com  |  0909 123 456",
    )
    html = converter._render_html(SAMPLE_CV_MD)

    assert "<h1>Nguyễn Văn A</h1>" in html
    assert "Backend Developer" in html
    assert "email@example.com" in html
    assert "0909 123 456" in html
    assert "<hr>" in html
    assert "<main class=\"cv-body\">" in html


def test_cv_theme_has_css_classes():
    """Test CV theme CSS chứa các class cần thiết."""
    converter = MarkdownToPdfConverter(theme="cv")
    html = converter._render_html("# Test\n\nSome text.")

    assert "cv-container" in html
    assert "cv-header" in html
    assert "cv-body" in html


def test_convert_cv_md_to_pdf():
    """Test convert file samplecv.md -> PDF (hoặc 422 nếu thiếu lib hệ thống)."""
    response = client.post(
        "/convert/md-to-pdf",
        files={"file": ("samplecv.md", SAMPLE_CV_MD.encode("utf-8"), "text/markdown")},
    )
    assert response.status_code in (200, 422)
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/pdf"