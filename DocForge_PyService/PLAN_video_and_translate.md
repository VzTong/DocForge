# PLAN: Video → Text & Dịch Transcript (AI)

Tài liệu này mô tả kế hoạch phát triển **hai tính năng mới** cho `DocForge_PyService`, bám sát kiến trúc hiện có (đặc biệt phần transcription đã có `preview` + `export`).

**Nguyên tắc bắt buộc:**
- Tất cả giải pháp phải **hợp pháp**.
- Chỉ hỗ trợ nội dung mà người dùng có quyền sử dụng (upload file của chính họ hoặc link YouTube công khai, không bypass DRM, không tải nội dung trả phí).
- Ưu tiên tái sử dụng code hiện có (transcribe pipeline, formatter, job_id, segments).

---

## 1. Video → Text

### 1.1. Mục tiêu

Cho phép người dùng:
1. Upload file video (mp4, mkv, webm, mov, …).
2. Hoặc dán **link YouTube công khai**.
3. Hệ thống tự tách audio → chạy pipeline transcription hiện có → trả về segments để chỉnh sửa / export (giống audio).

### 1.2. Luồng xử lý đề xuất

```
User upload video  ──┐
                     ├──► [Bước mới] Extract audio (ffmpeg) ──► Audio file tạm
User dán YouTube link┘                                          │
                                                                ▼
                                                    Transcribe (giống audio hiện tại)
                                                                │
                                                                ▼
                                                    Trả segments + job_id (preview)
                                                                │
                                                                ▼
                                                    User chỉnh sửa → Export SRT/VTT/TXT
```

### 1.3. Chi tiết kỹ thuật

#### A. Extract audio từ video local

- Thư viện / tool: **ffmpeg** (đã phổ biến, ổn định, miễn phí).
- Lệnh cơ bản (ví dụ):
  ```bash
  ffmpeg -i input_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output_audio.wav
  ```
- Nên chuẩn hóa về 16kHz mono WAV để tương thích tốt với Whisper.
- Lưu audio tạm trong `job_dir` (giống cách lưu audio hiện tại).
- Xóa video gốc sau khi extract xong (tiết kiệm dung lượng).

#### B. Hỗ trợ link YouTube (hợp pháp)

- Tool: **yt-dlp** (fork của youtube-dl, cập nhật thường xuyên).
- Chỉ cho phép:
  - Video công khai (public).
  - Không hỗ trợ video private, age-restricted, premium, DRM.
- Luồng:
  1. User gửi URL.
  2. Backend validate URL (chỉ chấp nhận domain youtube.com / youtu.be).
  3. Dùng `yt-dlp` tải **chỉ audio** (không tải video full) với tùy chọn:
     ```bash
     yt-dlp -x --audio-format wav --audio-quality 0 -o "job_dir/audio.%(ext)s" "URL"
     ```
  4. Sau đó chạy transcription bình thường.
- **Cảnh báo pháp lý**: Phải ghi rõ trong UI và README rằng người dùng chịu trách nhiệm về quyền sử dụng nội dung.

#### C. API mới đề xuất

```http
POST /transcribe/preview-video
```

Hoặc mở rộng endpoint hiện tại `/transcribe/preview` để chấp nhận thêm:
- `video_file` (UploadFile)
- `youtube_url` (string)

Logic:
- Nếu có `video_file` → extract audio.
- Nếu có `youtube_url` → tải audio bằng yt-dlp.
- Sau đó gọi lại logic `transcribe_preview` hiện có.

Giữ nguyên response format (job_id + segments) để Frontend tái sử dụng gần như 100% code của Audio → Text.

### 1.4. Thứ tự triển khai đề xuất

| Bước | Việc | Ưu tiên |
|------|------|--------|
| 1 | Thêm dependency `ffmpeg-python` hoặc gọi subprocess ffmpeg + kiểm tra ffmpeg có sẵn trên hệ thống | Cao |
| 2 | Viết hàm `extract_audio_from_video(video_path, output_audio_path)` | Cao |
| 3 | Mở rộng `/transcribe/preview` hoặc tạo endpoint mới hỗ trợ video_file | Cao |
| 4 | Thêm hỗ trợ `youtube_url` (yt-dlp) + validate domain | Trung bình |
| 5 | Cleanup file tạm (video + audio) theo TTL giống hiện tại | Cao |
| 6 | Viết unit test + integration test | Cao |
| 7 | Cập nhật Swagger + README | Cao |

### 1.5. Rủi ro & xử lý

- File video rất lớn → giới hạn `MAX_VIDEO_SIZE` (ví dụ 500MB–1GB).
- yt-dlp bị YouTube chặn → có cơ chế retry / thông báo lỗi rõ ràng.
- Máy không có ffmpeg → báo lỗi thân thiện + hướng dẫn cài.

---

## 2. Dịch Transcript bằng AI (Dịch thoát nghĩa – Any Language ↔ Any Language)

### 2.1. Mục tiêu

Cho phép người dùng gửi một transcript (danh sách segments) và nhận lại bản dịch **thoát nghĩa, tự nhiên theo ngữ cảnh**, không dịch word-by-word cứng nhắc.

**Hỗ trợ dịch mọi ngôn ngữ sang mọi ngôn ngữ** (Any → Any), không giới hạn chỉ sang tiếng Việt. Ví dụ:
- Tiếng Anh → Tiếng Việt
- Tiếng Nhật → Tiếng Anh
- Tiếng Hàn → Tiếng Việt
- Tiếng Pháp → Tiếng Tây Ban Nha
- … và ngược lại.

**Ví dụ yêu cầu chất lượng (minh họa tiếng Anh → tiếng Việt):**

| Gốc (EN) | Dịch mong muốn (VI) |
|----------|---------------------|
| "Mirror, mirror on the wall, Who is the fairest of them all?" | "Gương kia, ngự ở trên tường, thế gian ai đẹp được dường như ta?" |
| "You" / "Me" trong Harry Potter (tùy ngữ cảnh thân thiết) | "cậu – tớ", "bồ – mình", "ngươi – ta"... |

Khi dịch sang ngôn ngữ khác, model phải tôn trọng đặc trưng văn hóa & cách xưng hô của ngôn ngữ đích.

### 2.2. Nguyên tắc dịch

- **Dịch thoát nghĩa** (sense-for-sense), ưu tiên tự nhiên, đúng văn phong của **ngôn ngữ đích**.
- Giữ nguyên timestamp của từng segment (chỉ dịch phần `text`).
- Hỗ trợ chọn phong cách / cấp độ thân mật (formal / neutral / intimate / literary…).
- Có thể dịch toàn bộ hoặc chỉ một số segment được chọn.
- Luôn cho người dùng xem bản gốc + bản dịch song song trước khi export.
- Hỗ trợ **mọi cặp ngôn ngữ** mà LLM hỗ trợ tốt (ưu tiên các ngôn ngữ phổ biến: vi, en, ja, ko, zh, fr, es, de, th, id…).

### 2.3. Kiến trúc đề xuất

```
Frontend gửi:
  - segments (JSON)
  - source_language (optional – nếu không gửi thì model tự nhận diện)
  - target_language (bắt buộc – ví dụ: "vi", "en", "ja", "ko", "fr"...)
  - style / tone (optional: formal, casual, literary, harry-potter-style...)
  - context_hint (optional: "đây là truyện cổ tích", "đối thoại Harry Potter"...)

Backend:
  1. Ghép các segment thành đoạn văn có ngữ cảnh (hoặc gửi theo batch có overlap).
  2. Gọi LLM (Groq / OpenAI / local Ollama) với system prompt mạnh về dịch thoát nghĩa.
  3. Parse kết quả trả về đúng số lượng segment.
  4. Trả về segments mới (cùng start/end, text đã dịch).
```

### 2.4. Prompt mẫu (gợi ý – đa ngôn ngữ)

```text
You are a professional translator specializing in subtitles and literature.
Translate the following segments into {target_language} in a NATURAL, CONTEXTUAL, sense-for-sense way.
DO NOT translate word-by-word.
Keep the exact number and order of segments.
If the content is dialogue, choose appropriate forms of address / pronouns that match the culture and tone of the target language.
Respect the requested style: {style}

Additional context: {context_hint}
Source language (if known): {source_language}

Segments to translate:
1. [00:01:23 --> 00:01:28] Mirror, mirror on the wall...
2. ...
```

> Prompt nên viết bằng tiếng Anh để model hiểu tốt hơn khi dịch giữa các ngôn ngữ không phải tiếng Việt. Có thể bổ sung few-shot examples theo từng cặp ngôn ngữ phổ biến nếu cần chất lượng cao hơn.

### 2.5. API đề xuất

```http
POST /transcribe/translate
Content-Type: application/json

{
  "segments": [
    {"id": "seg_0001", "start": 1.2, "end": 4.5, "text": "Mirror, mirror on the wall..."}
  ],
  "target_language": "vi",           // bắt buộc – ngôn ngữ đích (vi, en, ja, ko, fr, es...)
  "source_language": "en",           // optional – giúp model chính xác hơn
  "style": "literary",               // optional
  "context_hint": "Fairy tale – Snow White"
}
```

Response:

```json
{
  "segments": [
    {
      "id": "seg_0001",
      "start": 1.2,
      "end": 4.5,
      "text": "Gương kia, ngự ở trên tường, thế gian ai đẹp được dường như ta?",
      "original_text": "Mirror, mirror on the wall..."   // optional, tiện so sánh
    }
  ],
  "source_language": "en",
  "target_language": "vi"
}
```

Sau đó Frontend có thể gọi lại `/transcribe/export` với segments đã dịch.

### 2.6. Thứ tự triển khai đề xuất

| Bước | Việc | Ưu tiên |
|------|------|--------|
| 1 | Chọn LLM provider (ưu tiên Groq vì đã có sẵn trong project) | Cao |
| 2 | Viết hàm `translate_segments(segments, source_lang, target_lang, style, context)` | Cao |
| 3 | Thiết kế system prompt đa ngôn ngữ + few-shot examples (văn học, đối thoại…) | Cao |
| 4 | Xử lý batching (tránh vượt context window) | Trung bình |
| 5 | Endpoint `/transcribe/translate` | Cao |
| 6 | Frontend: nút "Dịch bằng AI" + chọn ngôn ngữ nguồn/đích + style | Cao |
| 7 | Test với nhiều cặp ngôn ngữ + case khó (thơ, xưng hô, thuật ngữ chuyên ngành) | Cao |

### 2.7. Lưu ý quan trọng

- **Chi phí API**: Cần giới hạn độ dài transcript hoặc số segment mỗi lần dịch.
- **Chất lượng**: Luôn để người dùng xem và chỉnh sửa lại sau khi AI dịch.
- **Không thay thế con người**: Tính năng này hỗ trợ, không phải "dịch xong là dùng luôn".
- Tuân thủ điều khoản sử dụng của nhà cung cấp LLM.

---

## 3. Thứ tự ưu tiên tổng thể

1. **Video local → Audio → Text** (dễ nhất, tái sử dụng gần như toàn bộ pipeline hiện có).
2. **Dịch transcript AI (Any Language → Any Language)** (giá trị cao, hỗ trợ mọi cặp ngôn ngữ).
3. **Hỗ trợ YouTube URL** (tiện lợi nhưng cần xử lý pháp lý + ổn định của yt-dlp).

---

## 4. Checklist trước khi merge

- [ ] Tất cả file tạm được dọn dẹp (TTL hoặc sau request).
- [ ] Có giới hạn kích thước file rõ ràng.
- [ ] Error message thân thiện, bằng tiếng Việt.
- [ ] Swagger mô tả đầy đủ.
- [ ] Test coverage cho happy path + edge cases.
- [ ] README được cập nhật.
- [ ] Không chứa dẫn người dùng vi phạm bản quyền.

---

*Tài liệu này sẽ được cập nhật khi bắt đầu implement từng phần.*
