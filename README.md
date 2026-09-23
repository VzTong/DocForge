# DocForge

<p align="center">
  <strong>Bộ công cụ web chuyển đổi tài liệu & xử lý media</strong>
</p>

<p align="center">
  <a href="https://forgedoc.onrender.com">
    <img src="https://img.shields.io/badge/Demo-Live-brightgreen?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo"/>
  </a>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License MIT"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status"/>
</p>

<p align="center">
  <!-- Frontend -->
  <img src="https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" alt="Vue 3"/>
  <img src="https://img.shields.io/badge/Vite-7-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/Pinia-State-FFD859?style=flat-square&logo=pinia&logoColor=black" alt="Pinia"/>
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
  <img src="https://img.shields.io/badge/Vue_Router-4-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" alt="Vue Router"/>
  &nbsp;
  <!-- Backend -->
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/WeasyPrint-PDF-E34F26?style=flat-square&logo=css3&logoColor=white" alt="WeasyPrint"/>
  <img src="https://img.shields.io/badge/Whisper-Transcription-FF6F00?style=flat-square&logo=openai&logoColor=white" alt="Whisper"/>
  <img src="https://img.shields.io/badge/Groq-API-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq"/>
</p>

---

**DocForge** gồm hai phần chính:

| Phần | Thư mục | Mô tả |
|------|---------|-------|
| **Frontend** | `DocForge_FE` | Giao diện web (Vue 3 + Vite) |
| **Backend** | `DocForge_PyService` | API RESTful (Python FastAPI) |

🔗 **Demo:** [https://forgedoc.onrender.com](https://forgedoc.onrender.com)

---

## Tính năng hiện có

| Tính năng | Đường dẫn Frontend | Endpoint Backend chính | Mô tả ngắn |
|-----------|--------------------|------------------------|------------|
| **Markdown → PDF** | `/convert/md-to-pdf` | `POST /convert/md-to-pdf`<br>`POST /preview/md-to-pdf` | Upload/dán Markdown, chọn theme (`document` / `github` / `cv`), preview & tải PDF. Hỗ trợ metadata (title, subtitle, contact...) |
| **PDF → DOCX** | `/convert/pdf-to-docx` | `POST /convert/pdf-to-docx` | Upload PDF, tùy chọn khoảng trang, tải file Word (dùng `pdf2docx`) |
| **Audio → Text (Transcript Editor)** | `/convert/audio-to-text` | `POST /transcribe/preview`<br>`POST /transcribe/export`<br>`POST /transcribe/transcribe/audio-to-file` | Upload audio → xem & chỉnh sửa segments → xuất SRT / VTT / TXT. Hỗ trợ hint (prompt) để tăng độ chính xác |

**Sắp tới** (đã có route comment sẵn trong `DocForge_FE/src/route.js` và kế hoạch trong `DocForge_PyService/PLAN_video_and_translate.md`):

- Video → Text
- Dịch transcript bằng AI

---

## Cấu trúc monorepo

```
DocForge/
├── DocForge_FE/                 # Frontend (Vue 3 + Vite)
│   ├── src/
│   │   ├── pages/client/        # Home, Mdtopdf, PdftodocxPage, TranscriptEditorPage
│   │   ├── composables/         # Logic gọi API (useMdToPdfConverter, usePdfToDocxConverter...)
│   │   ├── configs/             # Cấu hình API base URL
│   │   ├── components/
│   │   ├── services/
│   │   ├── route.js
│   │   └── ...
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── README.md
│
├── DocForge_PyService/          # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py              # Entry point
│   │   ├── api/
│   │   │   ├── routes.py        # md-to-pdf, pdf-to-docx
│   │   │   └── transcription_routes.py
│   │   ├── converters/          # Markdown → PDF, PDF → DOCX + templates
│   │   ├── media/transcription/ # faster-whisper / Groq
│   │   └── core/
│   ├── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── .env.example
│   ├── Dockerfile
│   ├── PLAN_video_and_translate.md
│   ├── Transcript-editor-plan.md
│   └── README.md
│
└── .gitignore
```

---

## Công nghệ sử dụng

### Frontend (`DocForge_FE`)

| Công nghệ | Badge | Vai trò |
|-----------|-------|---------|
| Vue 3 | ![Vue](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white) | Framework UI (Composition API) |
| Vite 7 | ![Vite](https://img.shields.io/badge/Vite-7-646CFF?style=flat-square&logo=vite&logoColor=white) | Build tool |
| Vue Router 4 | ![Vue Router](https://img.shields.io/badge/Vue_Router-4-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white) | Routing |
| Pinia | ![Pinia](https://img.shields.io/badge/Pinia-State-FFD859?style=flat-square&logo=pinia&logoColor=black) | State management |
| Bootstrap 5 | ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white) | UI framework + Icons |
| VeeValidate | ![VeeValidate](https://img.shields.io/badge/VeeValidate-Form-42B883?style=flat-square) | Form validation |
| GSAP | ![GSAP](https://img.shields.io/badge/GSAP-Animation-88CE02?style=flat-square&logo=greensock&logoColor=white) | Animation |
| Anime.js | ![Anime.js](https://img.shields.io/badge/Anime.js-Animation-FF2D55?style=flat-square) | Animation nhẹ |
| Poppins / Rubik | ![Fonts](https://img.shields.io/badge/Fonts-Poppins_·_Rubik-4285F4?style=flat-square&logo=googlefonts&logoColor=white) | Typography |

### Backend (`DocForge_PyService`)

| Công nghệ | Badge | Vai trò |
|-----------|-------|---------|
| FastAPI | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | Web framework |
| Python 3.10+ | ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white) | Ngôn ngữ |
| Uvicorn | ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=flat-square&logo=uvicorn&logoColor=white) | ASGI server |
| WeasyPrint | ![WeasyPrint](https://img.shields.io/badge/WeasyPrint-PDF-E34F26?style=flat-square) | Render Markdown → PDF |
| pdf2docx | ![pdf2docx](https://img.shields.io/badge/pdf2docx-PDF_to_DOCX-2B579A?style=flat-square&logo=microsoftword&logoColor=white) | Chuyển PDF → DOCX |
| faster-whisper | ![Whisper](https://img.shields.io/badge/faster--whisper-Local-FF6F00?style=flat-square&logo=openai&logoColor=white) | Transcription local |
| Groq API | ![Groq](https://img.shields.io/badge/Groq-API-F55036?style=flat-square) | Transcription cloud (nhanh) |
| Pydantic | ![Pydantic](https://img.shields.io/badge/Pydantic-Settings-E92063?style=flat-square) | Config & validation |
| Jinja2 | ![Jinja2](https://img.shields.io/badge/Jinja2-Templates-B41717?style=flat-square) | Theme templates (MD→PDF) |

---

## Yêu cầu hệ thống

### Chung
- Git
- Node.js **18+** (khuyến nghị 20 LTS)
- Python **3.10+**

### Backend – System dependencies (WeasyPrint)
- **Windows**: Cài [GTK3 Runtime](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get update
  sudo apt-get install -y libpango-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 libffi-dev
  ```
- (Tùy chọn) GPU + CUDA nếu muốn chạy `faster-whisper` nhanh hơn trên local
- (Tùy chọn) `ffmpeg` (dành cho tính năng Video → Text trong roadmap)

---

## Cài đặt & Chạy local

### 1. Backend (DocForge_PyService)

```bash
cd DocForge_PyService

# Tạo virtual environment
python -m venv .venv

# Kích hoạt
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Cài dependencies (bao gồm cả dev)
pip install -r requirements-dev.txt

# Tạo file .env
cp .env.example .env
# Chỉnh sửa .env (đặc biệt GROQ_API_KEY nếu dùng engine groq)
```

Chạy server:

```bash
# Development (auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend (DocForge_FE)

```bash
cd DocForge_FE

npm install

# Chạy development server
npm run dev
```

Mặc định: http://localhost:5173

Frontend gọi backend tại `http://localhost:8000` (cấu hình trong `src/configs/` hoặc biến môi trường `VITE_API_BASE_URL`). CORS backend hiện cho phép `*`.

### Build production Frontend

```bash
npm run build      # output → dist/
npm run preview    # xem trước bản build
```

---

## Cấu hình Backend (`.env`)

| Biến | Mô tả | Ví dụ |
|------|-------|-------|
| `DEBUG` | Bật debug mode | `true` / `false` |
| `MAX_FILE_SIZE` | Giới hạn file document (bytes) | `20971520` (20MB) |
| `MAX_AUDIO_SIZE` | Giới hạn file audio (bytes) | `104857600` (100MB) |
| `TRANSCRIBER_ENGINE` | Engine transcription | `local` hoặc `groq` |
| `GROQ_API_KEY` | API key Groq (bắt buộc nếu dùng `groq`) | `gsk_...` |
| `GROQ_MODEL` | Model Groq | `whisper-large-v3` |
| `GROQ_MAX_BYTES` | Giới hạn file gửi lên Groq | `26214400` |

---

## API Endpoints chính

### Health & Info
```
GET /health
GET /converters
GET /transcribe/health
GET /transcribe/format
```

### Markdown → PDF
```
POST /convert/md-to-pdf          # multipart/form-data (file hoặc content)
POST /preview/md-to-pdf          # application/json → PDF inline
```

Tham số quan trọng: `theme` (`document` | `github` | `cv`), `title`, `subtitle`, `contact`, `page_size`...

### PDF → DOCX
```
POST /convert/pdf-to-docx        # multipart/form-data
```
Tham số: `file`, `start_page` (0-indexed, optional), `end_page` (exclusive, optional)

### Transcription
```
POST /transcribe/preview                 # upload audio → JSON segments + job_id
POST /transcribe/export                  # segments đã sửa → SRT/VTT/TXT
POST /transcribe/transcribe/audio-to-file  # upload audio → file ngay
```

Engine: `faster-whisper` (local) hoặc Groq API. Hỗ trợ `prompt` (hint) để cải thiện độ chính xác.

Chi tiết đầy đủ xem trong `DocForge_PyService/README.md`.

---

## Docker

### Backend
```bash
cd DocForge_PyService
docker build -t docforge-pyservice .
docker run -p 8000:8000 --env-file .env docforge-pyservice
```

### Frontend
```bash
cd DocForge_FE
docker build -t docforge-fe .
docker run -p 80:80 docforge-fe
```

---

## Chạy Test (Backend)

```bash
cd DocForge_PyService
python -m pytest -v --tb=short

# Test cụ thể
python -m pytest tests/test_api.py::test_render_cv_theme -v -s
python -m pytest tests/test_api.py::test_pdf_to_docx_success -v
```

> Lưu ý: Một số test PDF có thể trả `422` nếu máy thiếu system libraries của WeasyPrint.

---

## Troubleshooting nhanh

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `WeasyPrint import failed` | Thiếu GTK/Pango/Cairo | Cài system dependencies như mục "Yêu cầu hệ thống" |
| `Theme 'xyz' does not exist` | Theme chưa có | Dùng `document` / `github` / `cv` |
| `413 File too large` | Vượt `MAX_FILE_SIZE` / `MAX_AUDIO_SIZE` | Tăng giá trị trong `.env` hoặc nén file |
| Transcription chậm | Đang dùng engine local | Đặt `TRANSCRIBER_ENGINE=groq` + điền `GROQ_API_KEY` |
| `Job không tồn tại` | `job_id` hết hạn (TTL ~2 giờ) | Upload lại audio |

---

## Roadmap ngắn hạn

Xem chi tiết trong:

- `DocForge_PyService/PLAN_video_and_translate.md`
- `DocForge_PyService/Transcript-editor-plan.md`

1. **Video → Text** (tách audio bằng ffmpeg + hỗ trợ link YouTube hợp pháp)
2. **Dịch transcript bằng AI** (dịch thoát nghĩa, tự nhiên theo ngữ cảnh)

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

MIT

> Ghi chú: File `LICENSE` hiện có trong `app/converters/templates/markdown/github/` là license của thư viện bên thứ ba (`github-markdown-css`), không phải license của toàn bộ dự án. Nên thêm file `LICENSE` (MIT) ở root monorepo nếu muốn công khai rõ ràng.
```
