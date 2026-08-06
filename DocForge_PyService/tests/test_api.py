"""Test cơ bản cho DocForge_PyService (Phase 0 - khung test)

Chạy project: pytest -v (từ thư mục DocForge_PyService)
Không cần Chrome: kiểm tra health, listing, render HTML, và các nhánh lỗi"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.converters.markdown.md2pdf import (
    MarkdownToPdfConverter,
    _is_simple_cv_header,
)
from app.converters.markdown.meta import split_document_header
from app.main import app

from pathlib import Path

client = TestClient(app)

SAMPLE_MD = """# CV\n\n| Kỹ năng | Mức độ |\n| --- | --- |\n| Python | 5/5 |\n| FastAPI | 4/5 |\n\n## Kinh nghiệm\n- Công ty A: 2020-2022\n- Công ty B: 2022-2024\n\n```python\nprint("Hello World")\n```"""

SAMPLE_MD_PATH = Path(__file__).parent / "fixtures" / "sample.md"

SAMPLE_CV_MD_PATH = Path(__file__).parent / "fixtures" / "samplecv.md"

SAMPLE_CV_MD = SAMPLE_CV_MD_PATH.read_text(encoding="utf-8")

# Báo cáo có metadata lines trước --- (dùng để test document/github giữ nguyên header)
SAMPLE_DOC_MD = Path(__file__).parent / "fixtures" / "sampledoc.md"

# Header CV phức tạp (HTML layout / icon) → không được tách
SAMPLE_COMPLEX_CV_MD = """# Fullname

<div class="cv-header-grid">
  <div class="left">
    <strong>.NET Backend Developer (Fresher)</strong>
  </div>
  <div class="right">
    <span class="icon">🌐</span> name.id.vn<br>
    <span class="icon">✉</span> name@gmail.com
  </div>
</div>

---

## Kinh nghiệm
- Công ty A
"""


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
    assert '<pre><code class="language-python">' in html_content


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


def test_render_document_theme_supports_page_size_option():
    """Theme document phải nhận page_size và render CSS tương ứng."""
    converter = MarkdownToPdfConverter(theme="document", title="Test Document")
    html = converter._render_html(SAMPLE_MD, page_size="Letter")

    assert "size: Letter;" in html


def _read_md() -> str:
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
    """Test CV theme render HTML có header (tên, chức danh, contact) và body.

    Khi không truyền subtitle/contact qua options, converter tự trích từ
    Markdown (samplecv có **Backend Developer** → ra <strong>).
    """
    converter = MarkdownToPdfConverter(theme="cv")
    html = converter._render_html(SAMPLE_CV_MD)

    assert "<h1>Nguyễn Văn A</h1>" in html
    assert "<strong>Backend Developer</strong>" in html
    assert "email@example.com" in html
    assert "0909 123 456" in html
    assert 'href="https://linkedin.com/in/nguyenvana"' in html
    assert "<hr>" not in html
    assert '<main class="cv-body">' in html


def test_cv_theme_has_css_classes():
    """Test CV theme CSS có các class cần thiết."""
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


def test_preview_md_to_pdf_cv_metadata_not_duplicated():
    """Preview từ Markdown CV không được render lặp metadata ở body."""
    response = client.post(
        "/preview/md-to-pdf",
        json={
            "contents": SAMPLE_CV_MD,
            "theme": "cv",
            "title": "Nguyễn Văn A",
            "subtitle": "Backend Developer",
            "contact": "email@example.com | 0909 123 456",
        },
    )
    assert response.status_code in (200, 422)
    if response.status_code == 200:
        assert response.headers["content-type"] == "application/pdf"
        assert response.headers["content-disposition"].startswith("inline")


def test_split_document_header_extracts_address_and_links():
    """Header CV phải tách được cả address và links."""
    title, subtitle, contact, address, links, body = split_document_header(SAMPLE_CV_MD)

    assert title == "Nguyễn Văn A"
    assert subtitle == "**Backend Developer**"
    assert contact == "📧 email@example.com | 📱 0909 123 456"
    assert address == "📍 TP. Hồ Chí Minh, Việt Nam"
    assert links == "[LinkedIn](https://linkedin.com/in/nguyenvana) | [GitHub](https://github.com/nguyenvana)"
    assert "Tóm tắt nghề nghiệp" in body


# ---------------------------------------------------------------------------
# Header handling: document / github giữ nguyên; CV simple tách; CV complex không tách
# ---------------------------------------------------------------------------

def test_is_simple_cv_header_recognizes_samplecv():
    """samplecv.md là header đơn giản → được nhận diện để tách."""
    assert _is_simple_cv_header(SAMPLE_CV_MD) is True


def test_is_simple_cv_header_rejects_complex_html():
    """Header có div/span class (layout/icon) → coi là phức tạp, không tách."""
    assert _is_simple_cv_header(SAMPLE_COMPLEX_CV_MD) is False


def test_is_simple_cv_header_document_style_is_simple():
    """Báo cáo metadata lines (không HTML layout) vẫn được heuristic coi là simple.
    Việc không tách khi dùng theme document là do theme != cv, không phải heuristic.
    """
    assert _is_simple_cv_header(SAMPLE_DOC_MD) is True


def test_document_theme_keeps_metadata_lines():
    """Theme document phải giữ nguyên H1 + dòng metadata trước ---."""
    converter = MarkdownToPdfConverter(theme="document")
    html = converter._render_html(SAMPLE_DOC_MD)

    assert "Báo cáo Dự án" in html
    assert "Tên dự án" in html
    assert "Hệ thống Quản lý Kho hàng" in html
    assert "03/08/2026" in html
    assert "Nguyễn Văn A" in html
    assert "Tóm tắt" in html


def test_github_theme_keeps_metadata_lines():
    """Theme github phải giữ nguyên H1 + dòng metadata trước ---."""
    converter = MarkdownToPdfConverter(theme="github")
    html = converter._render_html(SAMPLE_DOC_MD)

    assert "Báo cáo Dự án" in html
    assert "Tên dự án" in html
    assert "Hệ thống Quản lý Kho hàng" in html
    assert "Tóm tắt" in html


def test_cv_theme_simple_header_is_split():
    """CV + header đơn giản (samplecv) → header đưa lên template, body không lặp metadata."""
    converter = MarkdownToPdfConverter(theme="cv")
    html = converter._render_html(SAMPLE_CV_MD)

    # Header nằm trong vùng cv-header
    assert "<h1>Nguyễn Văn A</h1>" in html
    assert "Backend Developer" in html
    assert "email@example.com" in html
    assert "TP. Hồ Chí Minh" in html
    assert "linkedin.com/in/nguyenvana" in html

    # Body bắt đầu từ section
    assert "Tóm tắt nghề nghiệp" in html

    body_start = html.find('<main class="cv-body">')
    assert body_start != -1
    body_html = html[body_start:]
    # Tên không còn trong body (đã tách lên header)
    assert "Nguyễn Văn A" not in body_html


def test_cv_theme_complex_header_is_kept_in_body():
    """CV + header phức tạp (HTML layout) → không tách, toàn bộ nằm trong body."""
    converter = MarkdownToPdfConverter(theme="cv")
    html = converter._render_html(SAMPLE_COMPLEX_CV_MD)

    # Nội dung custom header vẫn còn trong output
    assert "cv-header-grid" in html
    assert ".NET Backend Developer" in html
    assert "name@gmail.com" in html
    assert "Kinh nghiệm" in html

    # Title vẫn được trích cho <title> / h1 template
    assert "<h1>Fullname</h1>" in html