# DocForge

Monorepo chứa các dịch vụ chuyển đổi tài liệu (Document Conversion Services).

## Cấu trúc dự án

```
DocForge/
├── CarRental_BE/          # .NET Backend (Car Rental System)
├── CarRental_FE/          # Vue.js Frontend (Car Rental System)
└── DocForge_PyService/    # Python FastAPI Service - Markdown → PDF Converter
```

## DocForge_PyService

Dịch vụ Python chuyển đổi Markdown sang PDF với nhiều theme.

### Tính năng
- **Theme `document`** — Tài liệu chung, layout đơn giản
- **Theme `github`** — Style giống GitHub README
- **Theme `cv`** — Resume/CV layout chuyên nghiệp

### Cài đặt & Chạy

```bash
cd DocForge_PyService

# Tạo virtual environment (lần đầu)
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# hoặc: source .venv/bin/activate  # Linux/macOS

# Cài dependencies
pip install -r requirements-dev.txt

# Chạy server (dev mode)
python -m uvicorn app.main:app --reload
# Mở http://localhost:8000/docs để xem Swagger UI
```

### Chạy Test

```bash
# Chạy tất cả test
python -m pytest -v --tb=short

# Chạy 1 test cụ thể
python -m pytest tests/test_api.py::test_render_cv_theme -v -s

# Xem coverage (Thấy được code nào chưa test)
pip install pytest-cov
python -m pytest --cov=app --cov-report=term-missing
-> Hiện % code được test + dòng nào chưa được test tới
```

### API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/health` | Health check |
| GET | `/converters` | Liệt kê converter khả dụng |
| POST | `/convert/md-to-pdf` | Chuyển Markdown → PDF |

**Ví dụ request `/convert/md-to-pdf`:**
```json
{
  "file": "<markdown-file>",
  "theme": "cv",
  "title": "Nguyễn Văn A",
  "subtitle": "Backend Developer",
  "contact": "email@example.com | 0909 123 456"
}
```

### Cấu trúc code

```
DocForge_PyService/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── converters/
│   │   ├── base.py             # BaseConverter abstract class
│   │   ├── registry.py         # Registry pattern cho converters
│   │   ├── md2pdf.py           # MarkdownToPdfConverter
│   │   ├── MarkdownThemeRenderer.py  # Theme loader + Jinja2 render
│   │   ├── markdown_options.py # Enum: MarkdownTheme, PageSize
│   │   └── templates/
│   │       └── markdown/
│   │           ├── document/   # Theme document
│   │           ├── github/     # Theme github
│   │           └── cv/         # Theme cv (resume)
│   └── api/                    # API routes
├── tests/
│   ├── test_api.py             # Integration + unit tests
│   └── fixtures/
│       ├── sample.md           # Sample markdown
│       └── samplecv.md         # Sample CV markdown
├── requirements.txt
├── requirements-dev.txt
└── Dockerfile
```

### Thêm Theme mới

1. Tạo folder `app/converters/templates/markdown/<theme-name>/`
2. Thêm `template.j2` (Jinja2 template) và `style.css`
3. Thêm theme name vào `MarkdownTheme` enum trong `markdown_options.py`
4. Theme sẽ tự động khả dụng — không cần sửa code khác

### Docker

```bash
docker build -t docforge-pyservice .
docker run -p 8000:8000 docforge-pyservice
```

---

## CarRental_BE / CarRental_FE

Xem README trong từng folder con để biết chi tiết.