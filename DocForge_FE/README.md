# DocForge_FE

Frontend của dự án **DocForge** — giao diện web hiện đại, thân thiện giúp người dùng sử dụng các công cụ chuyển đổi tài liệu và xử lý media một cách dễ dàng.

Được xây dựng bằng **Vue 3 + Vite**, sử dụng Bootstrap 5, Pinia, Vue Router và các thư viện animation nhẹ (GSAP, Anime.js).

---

## Tính năng hiện có

| Trang / Chức năng | Đường dẫn | Mô tả |
|-------------------|-----------|-------|
| Trang chủ | `/` | Giới thiệu các công cụ, điều hướng nhanh |
| Markdown → PDF | `/convert/md-to-pdf` | Upload hoặc dán Markdown, chọn theme (document / github / cv), preview & tải PDF |
| PDF → DOCX | `/convert/pdf-to-docx` | Upload PDF, chọn khoảng trang (tùy chọn), tải file Word |
| Audio → Text (Transcript Editor) | `/convert/audio-to-text` | Upload audio → xem & chỉnh sửa segments → xuất SRT / VTT / TXT |

**Sắp tới** (đã có sẵn route comment sẵn trong `route.js`):
- Video → Text
- Dịch transcript bằng AI

---

## Công nghệ sử dụng

- **Vue 3** (Composition API)
- **Vite 7**
- **Vue Router 4**
- **Pinia** (state management)
- **Bootstrap 5** + Bootstrap Icons
- **VeeValidate** (validate form)
- **GSAP** & **Anime.js** (animation)
- Font: Poppins + Rubik

---

## Yêu cầu

- Node.js 18+ (khuyến nghị 20 LTS)
- npm hoặc yarn / pnpm

---

## Cài đặt & Chạy

```bash
cd DocForge_FE

# Cài dependencies
npm install

# Chạy development server (hot-reload)
npm run dev
```

Mặc định chạy tại: [http://localhost:5173](http://localhost:5173)

### Build production

```bash
npm run build
```

File build sẽ nằm trong thư mục `dist/`.

### Preview bản build

```bash
npm run preview
```

---

## Cấu trúc thư mục

```
DocForge_FE/
├── public/                     # Static assets
├── src/
│   ├── assets/                 # Hình ảnh, font, style chung
│   ├── components/             # Component tái sử dụng
│   ├── composables/            # Logic tái sử dụng (useApi, useMdToPdfConverter...)
│   ├── configs/                # Cấu hình (API base URL...)
│   ├── pages/
│   │   └── client/
│   │       ├── Home.vue
│   │       ├── Mdtopdf.vue
│   │       ├── PdftodocxPage.vue
│   │       └── TranscriptEditorPage.vue
│   ├── services/               # Gọi API (axios / fetch wrapper)
│   ├── utils/
│   ├── App.vue
│   ├── Menu.vue
│   ├── main.js
│   └── route.js                # Định nghĩa routes
├── index.html
├── package.json
├── vite.config.js
├── Dockerfile
└── README.md
```

---

## Kết nối với Backend (DocForge_PyService)

Frontend gọi API của `DocForge_PyService` (mặc định `http://localhost:8000`).

Cấu hình base URL thường nằm trong:
- `src/configs/` hoặc
- biến môi trường Vite (`VITE_API_BASE_URL`)

Khi chạy local, hãy đảm bảo:

1. Backend đang chạy ở port 8000.
2. CORS đã được mở (hiện tại backend cho phép `*`).

---

## Các trang chính

### 1. Markdown → PDF (`Mdtopdf.vue`)

- Hỗ trợ upload file `.md` hoặc dán trực tiếp nội dung.
- Chọn theme: `document`, `github`, `cv`.
- Điền metadata (title, subtitle, contact...) hoặc để hệ thống tự trích từ Markdown.
- Preview PDF ngay trên trình duyệt.
- Tải xuống file PDF.

### 2. PDF → DOCX (`PdftodocxPage.vue`)

- Upload file PDF.
- Tùy chọn chọn trang bắt đầu / kết thúc.
- Tải về file `.docx`.

### 3. Transcript Editor (`TranscriptEditorPage.vue`)

Đây là trang phức tạp nhất hiện tại:

1. Upload file audio.
2. (Tùy chọn) Chọn / gõ **hint** (gợi ý từ khó, chủ đề) để cải thiện độ chính xác.
3. Gọi `POST /transcribe/preview` → nhận danh sách segments.
4. Hiển thị editor cho phép:
   - Xem & sửa từng đoạn text.
   - Find & Replace.
   - Giữ nguyên timestamp.
5. Xuất file SRT / VTT / TXT qua `POST /transcribe/export`.

Trang này đã được thiết kế theo đúng kế hoạch trong file `Transcript-editor-plan.md` ở root repo.

---

## Thêm công cụ mới (hướng dẫn nhanh)

Khi muốn thêm công cụ mới (ví dụ Video → Text):

1. Tạo page mới trong `src/pages/client/` (ví dụ `VideoToTextPage.vue`).
2. Thêm route trong `src/route.js`.
3. Tạo composable riêng trong `src/composables/` (theo khuôn `useMdToPdfConverter` / `usePdfToDocxConverter`).
4. Thêm entry vào menu / trang chủ.

---

## Docker

```bash
# Build
docker build -t docforge-fe .

# Run
docker run -p 80:80 docforge-fe
```

---

## Scripts có sẵn

| Lệnh | Mô tả |
|------|-------|
| `npm run dev` | Chạy development server |
| `npm run build` | Build production |
| `npm run preview` | Xem trước bản build |

---

## Ghi chú phát triển

- Ưu tiên **Composition API** + `<script setup>`.
- Tách logic gọi API ra composable để dễ tái sử dụng và test.
- Giữ UI sạch, responsive, ưu tiên trải nghiệm người dùng Việt Nam (tiếng Việt đầy đủ).
- Khi làm tính năng mới liên quan đến transcript, luôn tham khảo `Transcript-editor-plan.md` và `PLAN_video_and_translate.md` ở backend.

---

## License

MIT
