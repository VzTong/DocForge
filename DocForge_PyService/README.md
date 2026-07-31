# DocForge_PyService

Python FastAPI service để chuyển đổi Markdown sang PDF với nhiều theme tùy chỉnh.

## Tính năng

- **Theme `document`** — Tài liệu chung, layout đơn giản, phù hợp báo cáo, tài liệu kỹ thuật
- **Theme `github`** — Style giống GitHub README, phù hợp documentation
- **Theme `cv`** — Resume/CV layout chuyên nghiệp (header: tên, chức danh, contact; sections: Skills, Experience, Projects)

## Yêu cầu hệ thống

- Python 3.10+
- WeasyPrint dependencies (GTK3, Pango, Cairo, GDK-PixBuf, libffi)
  - **Windows**: Cài [GTK3 Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
  - **Linux**: `sudo apt-get install libpango-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 libffi-dev`

## Cài đặt

```bash
cd DocForge_PyService

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # Linux/macOS

# Cài dependencies
pip install -r requirements-dev.txt
```

## Chạy Server

```bash
# Development (auto-reload)
python -m uvicorn app.main:app --reload

# Production
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Mở http://localhost:8000/docs để xem Swagger UI.

## API Endpoints

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "DocForge_PyService"
}
```

### GET `/converters`
Liệt kê các converter khả dụng.

**Response:**
```json
{
  "available_converters": ["md-to-pdf"]
}
```

### POST `/convert/md-to-pdf`
Chuyển đổi file Markdown sang PDF.

**Request (multipart/form-data):**
| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| file | file | ✓ | File .md hoặc .markdown |
| theme | string | ✗ | Theme: `document`, `github`, `cv` (mặc định: `document`) |
| title | string | ✗ | Tiêu đề document (mặc định: "Document") |
| subtitle | string | ✗ | Phụ đề (chỉ dùng cho theme `cv`) |
| contact | string | ✗ | Thông tin liên hệ (chỉ dùng cho theme `cv`) |

**Response:**
- `200` — File PDF (`application/pdf`)
- `400` — File không phải Markdown
- `422` — Lỗi chuyển đổi (thiếu system dependencies)

**Ví dụ curl:**
```bash
curl -X POST http://localhost:8000/convert/md-to-pdf \
  -F "file=@sample.md" \
  -F "theme=cv" \
  -F "title=Nguyễn Văn A" \
  -F "subtitle=Backend Developer" \
  -F "contact=email@example.com | 0909 123 456" \
  --output output.pdf
```

## Chạy Test

```bash
# Tất cả test
python -m pytest -v --tb=short

# Test cụ thể
python -m pytest tests/test_api.py::test_render_cv_theme -v -s

# Coverage
pip install pytest-cov
python -m pytest --cov=app --cov-report=term-missing
```

## Cấu trúc Code

```
app/
├── main.py                      # FastAPI app + routes
├── converters/
│   ├── base.py                  # BaseConverter (abstract)
│   ├── registry.py              # Registry pattern
│   ├── md2pdf.py                # MarkdownToPdfConverter
│   ├── MarkdownThemeRenderer.py # Theme loader + Jinja2 render
│   ├── markdown_options.py      # Enum: MarkdownTheme, PageSize
│   └── templates/
│       └── markdown/
│           ├── document/        # Theme document
│           │   ├── template.j2
│           │   └── style.css
│           ├── github/          # Theme github
│           │   ├── template.j2
│           │   ├── github-markdown.css
│           │   └── override.css
│           └── cv/              # Theme cv (resume)
│               ├── template.j2
│               └── style.css
└── api/
    └── routes.py                # API route definitions
```

## Thêm Theme Mới

1. Tạo folder: `app/converters/templates/markdown/<theme-name>/`
2. Thêm 2 file:
   - `template.j2` — Jinja2 template (có `{{ title }}`, `{{ css }}`, `{{ body }}`)
   - `style.css` — CSS stylesheet
3. Thêm theme name vào `MarkdownTheme` enum trong `markdown_options.py`
4. Theme tự động khả dụng — **không cần sửa code khác**

## Docker

```bash
# Build
docker build -t docforge-pyservice .

# Run
docker run -p 8000:8000 docforge-pyservice
```

**Lưu ý:** Docker image cần cài system dependencies cho WeasyPrint. Xem `Dockerfile` để biết chi tiết.

## Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `WeasyPrint import failed` | Thiếu GTK3/Pango/Cairo | Cài system dependencies (xem trên) |
| `Theme 'xyz' does not exist` | Theme chưa được tạo | Tạo folder theme hoặc dùng theme có sẵn |
| `422 Unprocessable Entity` | WeasyPrint error khi render PDF | Kiểm tra log server, thường do thiếu font hoặc CSS không hợp lệ |

## License

MIT