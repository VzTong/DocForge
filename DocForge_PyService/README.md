# DocForge_PyService

Python FastAPI service phục vụ các chức năng chuyển đổi tài liệu và xử lý media của dự án **DocForge**.

Service này là backend chính, cung cấp API RESTful để:

- Chuyển **Markdown → PDF** với nhiều theme đẹp (document, github, cv).
- Chuyển **PDF → DOCX** (giữ layout tối đa, thuần Python).
- **Transcribe audio → text** (SRT / VTT / TXT) với hỗ trợ preview + chỉnh sửa segments.
- (Sắp tới) Video → Text và Dịch transcript bằng AI (xem file `PLAN_video_and_translate.md`).

---

## Tính năng hiện có

| Tính năng | Endpoint chính | Mô tả ngắn |
|-----------|----------------|----------|
| Markdown → PDF | `POST /convert/md-to-pdf`<br>`POST /preview/md-to-pdf` | Nhiều theme (document, github, cv), hỗ trợ metadata header, page size |
| PDF → DOCX | `POST /convert/pdf-to-docx` | Dùng `pdf2docx`, hỗ trợ chọn trang bắt đầu/kết thúc |
| Audio → Text (file) | `POST /transcribe/transcribe/audio-to-file` | Upload audio → nhận file SRT/VTT/TXT ngay |
| Audio → Text (preview) | `POST /transcribe/preview` | Trả về JSON segments + `job_id` để chỉnh sửa |
| Export transcript đã sửa | `POST /transcribe/export` | Nhận segments đã chỉnh → xuất file SRT/VTT/TXT |
| Health & Listing | `GET /health`<br>`GET /converters`<br>`GET /transcribe/health`<br>`GET /transcribe/format` | Kiểm tra trạng thái và danh sách hỗ trợ |

**Engine transcription**: Hỗ trợ cả **faster-whisper** (local) và **Groq API** (nhanh, cần API key).

---

## Yêu cầu hệ thống

- **Python** 3.10 trở lên
- **WeasyPrint** system dependencies (để render PDF):
  - **Windows**: Cài [GTK3 Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
  - **Linux (Ubuntu/Debian)**:
    ```bash
    sudo apt-get update
    sudo apt-get install -y libpango-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 libffi-dev
    ```
- (Tùy chọn) GPU + CUDA nếu muốn chạy faster-whisper nhanh hơn trên local.
- (Tùy chọn) `ffmpeg` nếu sau này dùng tính năng video (đã nằm trong PLAN).

---

## Cài đặt

```bash
cd DocForge_PyService

# 1. Tạo virtual environment
python -m venv .venv

# 2. Kích hoạt
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Cài dependencies (bao gồm cả dev)
pip install -r requirements-dev.txt

# 4. (Khuyến nghị) Tạo file .env từ mẫu
cp .env.example .env
# Sau đó chỉnh sửa các giá trị trong .env (đặc biệt GROQ_API_KEY nếu dùng Groq)
```

### Cập nhật requirements.txt khi thêm thư viện mới

Sau khi `pip install` thêm package mới, luôn chạy lệnh sau để ghi lại phiên bản chính xác:

```bash
pip freeze > requirements.txt
```

Sau đó kiểm tra lại file và commit.

---

## Chạy Server

```bash
# Development (tự động reload khi sửa code)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Mở trình duyệt:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Cấu hình (.env)

| Biến | Mô tả | Ví dụ |
|------|-------|-------|
| `DEBUG` | Bật debug mode | `true` / `false` |
| `MAX_FILE_SIZE` | Giới hạn kích thước file document (bytes) | `20971520` (20MB) |
| `MAX_AUDIO_SIZE` | Giới hạn kích thước file audio (bytes) | `104857600` (100MB) |
| `TRANSCRIBER_ENGINE` | Engine transcription | `local` hoặc `groq` |
| `GROQ_API_KEY` | API key của Groq (bắt buộc nếu dùng groq) | `gsk_...` |
| `GROQ_MODEL` | Model Groq | `whisper-large-v3` |
| `GROQ_MAX_BYTES` | Giới hạn file gửi lên Groq | `26214400` |

---

## API Endpoints chi tiết

### 1. Health & Info

```http
GET /health
GET /converters
GET /transcribe/health
GET /transcribe/format
```

### 2. Markdown → PDF

**Upload file hoặc gửi nội dung text:**

```http
POST /convert/md-to-pdf
Content-Type: multipart/form-data

file (optional)          : File .md / .markdown
content (optional)       : Nội dung Markdown dạng text
theme                    : document | github | cv   (mặc định: document)
title, subtitle, contact, address, links
page_size                : A4 | Letter | ...
```

**Preview (nhận JSON body, trả PDF inline):**

```http
POST /preview/md-to-pdf
Content-Type: application/json

{
  "contents": "# Tiêu đề\n\nNội dung...",
  "theme": "cv",
  "title": "Nguyễn Văn A",
  "subtitle": "Backend Developer",
  "contact": "email@example.com | 0909 123 456"
}
```

### 3. PDF → DOCX

```http
POST /convert/pdf-to-docx
Content-Type: multipart/form-data

file          : File PDF
start_page    : Trang bắt đầu (0-indexed, optional)
end_page      : Trang kết thúc (exclusive, optional)
```

### 4. Transcription

**Chuyển audio thành file ngay:**

```http
POST /transcribe/transcribe/audio-to-file
Content-Type: multipart/form-data

audio_file    : File audio (.mp3, .wav, .m4a, .flac, .ogg, .aac, ...)
fmt           : srt | vtt | txt
language      : vi | en | ... (để trống = tự nhận diện)
prompt        : Gợi ý ngữ cảnh / từ khó (optional)
```

**Preview (trả JSON segments để chỉnh sửa):**

```http
POST /transcribe/preview
Content-Type: multipart/form-data

audio_file    : File audio (lần đầu)
job_id        : ID job đã upload trước (khi muốn transcribe lại với prompt mới)
language      : ...
prompt        : Gợi ý ngữ cảnh
```

Response mẫu:

```json
{
  "job_id": "a1b2c3d4e5f6...",
  "language": "vi",
  "duration": 812.4,
  "segments": [
    {
      "id": "seg_0001",
      "start": 81.32,
      "end": 84.10,
      "text": "Tôi biết dễ mẹ sẽ đến"
    }
  ]
}
```

**Export segments đã sửa:**

```http
POST /transcribe/export
Content-Type: multipart/form-data

fmt           : srt | vtt | txt
filename      : Tên file (không cần đuôi)
segments      : JSON string của mảng segments
```

---

## Cấu trúc thư mục

```
DocForge_PyService/
├── app/
│   ├── main.py                     # Entry point FastAPI
│   ├── api/
│   │   ├── routes.py               # md-to-pdf, pdf-to-docx
│   │   └── transcription_routes.py # audio transcription
│   ├── converters/
│   │   ├── base.py
│   │   ├── registry.py
│   │   ├── common.py
│   │   ├── markdown/               # Markdown → PDF
│   │   ├── pdf/                    # PDF → DOCX
│   │   └── templates/
│   │       └── markdown/
│   │           ├── document/       # Theme document
│   │           ├── cv/             # Theme CV / resume
│   │           └── github/         # Theme giống GitHub README
│   │               ├── template.j2
│   │               ├── github-markdown.css
│   │               ├── override.css
│   │               ├── README.md
│   │               └── LICENSE      # MIT của thư viện github-markdown-css (sindresorhus)
│   ├── media/
│   │   └── transcription/          # Whisper / Groq + formatter
│   └── core/
│       ├── config.py
│       └── exception_handler.py
├── tests/
│   ├── test_api.py
│   └── fixtures/
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .env.example
└── README.md
```

> **Ghi chú về License:**
> - File `LICENSE` hiện có nằm ở `app/converters/templates/markdown/github/LICENSE` — đây là **license MIT của thư viện bên thứ ba** (`github-markdown-css` của Sindre Sorhus), không phải license của toàn bộ dự án DocForge_PyService.
> - Bản thân service hiện chưa có file `LICENSE` riêng ở root. README cũ chỉ ghi “MIT”. Nếu muốn công khai rõ ràng, nên thêm file `LICENSE` (MIT chuẩn) vào thư mục gốc monorepo hoặc vào `DocForge_PyService/`.

---

## Chạy Test

```bash
# Chạy tất cả test
python -m pytest -v --tb=short

# Chạy test cụ thể
python -m pytest tests/test_api.py::test_render_cv_theme -v -s
python -m pytest tests/test_api.py::test_pdf_to_docx_success -v

# Xem coverage
pip install pytest-cov
python -m pytest --cov=app --cov-report=term-missing
```

> **Lưu ý**: Một số test PDF sẽ trả về `422` nếu máy thiếu system libraries của WeasyPrint. Đây là hành vi mong đợi.

---

## Docker

```bash
# Build
docker build -t docforge-pyservice .

# Run
docker run -p 8000:8000 --env-file .env docforge-pyservice
```

---

## Troubleshooting

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|----------|
| `WeasyPrint import failed` | Thiếu GTK/Pango/Cairo | Cài system dependencies như phần "Yêu cầu hệ thống" |
| `Theme 'xyz' does not exist` | Theme chưa tạo | Tạo folder theme mới hoặc dùng theme có sẵn |
| `413 File too large` | Vượt `MAX_FILE_SIZE` / `MAX_AUDIO_SIZE` | Tăng giá trị trong `.env` hoặc nén file |
| Transcription chậm | Đang dùng engine local | Chuyển sang `TRANSCRIBER_ENGINE=groq` + điền API key |
| `Job không tồn tại` | `job_id` hết hạn (TTL 2 giờ) | Upload lại audio |

---

## Roadmap ngắn hạn

Xem file **[PLAN_video_and_translate.md](./PLAN_video_and_translate.md)** để biết kế hoạch phát triển:

1. Video → Text (tách audio bằng ffmpeg + hỗ trợ link YouTube hợp pháp).
2. Dịch transcript bằng AI (dịch thoát nghĩa, tự nhiên theo ngữ cảnh).

---

## License

MIT
