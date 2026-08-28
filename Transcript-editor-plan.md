# DocForge — Kế hoạch: Transcript Editor (Hint + Find & Replace)

> Tài liệu đặc tả để hướng dẫn AI/dev triển khai đúng phạm vi đã chốt, đúng thứ
> tự ưu tiên theo tác động. Không lan man sang phần chưa cần — mục 6 liệt kê rõ
> những gì **cố tình để sau**.

## 0. Ghi chú quan trọng — đảo hướng so với trao đổi trước đó

Ở lượt trao đổi trước, đã có bàn tới hướng **hậu xử lý transcript bằng LLM**
(gọi Groq hoặc Ollama local để tự sửa từ nghe nhầm) — đã tạo `postprocess.py`,
thêm `correct_with_llm`/`correction_hint` vào `service.py` và
`transcription_routes.py`.

**Tài liệu này THAY THẾ hướng đó.** Quyết định cuối: dùng **ô hint (tuỳ chọn,
áp dụng lúc transcribe) + editor find & replace (áp dụng sau, do người dùng
tự sửa)**, thay vì để một LLM thứ hai tự động "đoán sửa" sau lưng người dùng.
Lý do: đơn giản hơn, không tốn thêm lượt gọi API/latency, và quan trọng nhất —
**người dùng toàn quyền kiểm soát kết quả cuối cùng** thay vì tin vào một model
sửa hộ có thể sửa sai theo hướng khác.

➡️ Khi triển khai tài liệu này, có thể **giữ nguyên `postprocess.py` nhưng
KHÔNG gọi tới nó** (để đó cho tương lai nếu cần), hoặc gỡ bỏ hẳn 3 chỗ đã nối
dây (`service.py`, `transcription_routes.py`, `config.py` — các field
`correct_with_llm`, `correction_hint`, `groq_llm_model`). Không bắt buộc phải
dọn ngay, nhưng đừng nhầm đây là 2 tính năng cùng chạy song song.

---

## 1. Phạm vi & thứ tự ưu tiên (theo tác động, không làm dồn 1 lúc)

| # | Việc | Tác động | Khi nào làm |
|---|------|----------|-------------|
| 1 | **Ô hint tuỳ chọn** khi transcribe (3 chế độ: không mồi / dropdown chủ đề preset / gõ tay) | Giải quyết **phần lớn** lỗi từ khó | **Làm trước** |
| 2 | **Editor find & replace**, giữ nguyên timestamp từng segment | Dọn nốt lỗi cố định còn sót sau bước 1 | **Làm ngay sau** bước 1 |
| 3 | Prompt nền tiếng Việt cố định (định hướng chính tả/dấu câu chung) | Cải thiện nhẹ, không đặc thù theo audio | **Thêm sau**, ~3 dòng code |
| 4 | Lọc `no_speech_prob` (bỏ từ tượng thanh do model ảo giác, vd "pew"→"you") | Giảm nhiễu, không liên quan từ khó | **Thêm cuối cùng**, optional |

Mục 3 và 4 là "gia vị" — **không** đụng vào cho tới khi mục 1 và 2 chạy ổn.

### Bảng đối chiếu: đúng công cụ cho đúng vấn đề

| Muốn làm | Cách đúng | Không phải |
|---|---|---|
| Giảm lỗi dấu câu tiếng Việt nói chung | ✅ 1 prompt nền cố định | ❌ |
| Sửa từ khó riêng theo từng audio (vd "Dế Mèn") | ✅ Ô hint tuỳ chọn (mục 1) | ❌ prompt cố định (không đặc thù được) |
| Bỏ từ tượng thanh ("pew"→"you") | ✅ Lọc `no_speech_prob` (mục 4) | ❌ prompt (không giải quyết được ảo giác) |
| Lỗi cố định còn sót sau khi transcribe | ✅ Find & replace ở editor (mục 2) | — |

---

## 2. Kiến trúc tổng quan — 2 giai đoạn, tách rõ trách nhiệm

```
GIAI ĐOẠN 1 (gọi service)                    GIAI ĐOẠN 2 (thuần FE)
──────────────────────────                   ──────────────────────
User upload audio                             FE hiển thị transcript
   + chọn/gõ hint (optional)                     trong Editor (list segment)
        │                                              │
        ▼                                     User sửa text từng segment
FE: POST /transcribe/preview                    (find & replace áp dụng
   (audio_file, không có job_id)                trên field text, KHÔNG
        │                                        đụng start/end)
        ▼                                              │
PyService: lưu audio theo job_id                        ▼
   + transcribe + cắt cue                     User bấm "Tải xuống"
   (KHÔNG ghi file kết quả, trả JSON)                   │
        │                                               ▼
        ▼                                     FE: POST /transcribe/export
FE nhận { job_id, segments }                     (gửi segments ĐÃ SỬA,
   → render vào Editor, lưu job_id                KHÔNG cần job_id)
        │                                               │
        │ (user đổi hint, muốn thử lại)                 ▼
        ▼                                     PyService: render() có sẵn
FE: POST /transcribe/preview                     trong formatter.py
   (job_id, KHÔNG gửi audio_file lại)             → trả file .srt/.vtt/.txt
        │
        ▼
PyService: tìm audio theo job_id
   + transcribe lại với prompt mới
        │
        ▼
FE nhận segments mới, thay vào Editor
```

Điểm mấu chốt: **transcribe chỉ chạy 1 lần** (giai đoạn 1). Giai đoạn 2 không
gọi lại whisper/Groq — chỉ format lại text đã sửa thành file, dùng `render()`
đã có sẵn trong `formatter.py`, cực rẻ và nhanh.

---

## 3. Phân chia trách nhiệm FE ↔ Service

| Việc | Ở đâu | Vì sao |
|---|---|---|
| Transcribe audio | 🐍 PyService | Cần whisper-local/Groq, không chạy được ở trình duyệt |
| Hiển thị transcript | 💚 FE | Thuần UI |
| Editor + find & replace | 💚 FE | Thuần tương tác trên state đã có, không cần gọi server |
| Ô "gợi ý" (hint) | 💚 FE nhập → 🐍 Service dùng | User nhập ở FE, Service mồi vào tham số `prompt` đã có sẵn trong `transcribe()`/`transcribe_audio()` |
| Tạo file .srt/.vtt/.txt cuối | 🐍 Service (`/transcribe/export`) | Tái dùng `render()` có sẵn trong `formatter.py`, không cần logic mới |

**Không cần đổi gì ở tầng transcription engine** (`whisper_local.py`,
`groq_api.py`) — tham số `prompt`/`initial_prompt` đã tồn tại sẵn, chỉ cần FE
truyền đúng giá trị lên qua field `prompt` đã có trong
`transcription_routes.py`.

---

## 4. GIAI ĐOẠN 1 — Lấy transcript (chi tiết)

### 4.1. Ô hint — 3 chế độ

| Chế độ | Hành vi | Khi dùng |
|---|---|---|
| **Mặc định: không mồi gì** | `prompt = None`, gửi rỗng lên service | Luôn chạy được cho MỌI audio, không rủi ro mồi sai làm lệch kết quả |
| **Tuỳ chọn: dropdown chủ đề preset** | User chọn 1 mục có sẵn → FE tự nạp chuỗi hint tương ứng | Khi biết trước thể loại nội dung, đỡ phải gõ tay |
| **Tuỳ chọn: gõ tay** | User tự gõ hint riêng (tên nhân vật, thuật ngữ...) | Khi có audio đặc thù, dropdown preset không đủ |

Dropdown và ô gõ tay dùng **chung một field** gửi lên service — nếu chọn
dropdown, FE tự điền text tương ứng vào ô input (user vẫn có thể sửa tiếp
trước khi gửi, không bắt buộc dùng nguyên preset).

### 4.2. Bộ chủ đề preset (FE, static — không cần API riêng)

Danh sách khởi điểm, có thể mở rộng dần, không cần làm đầy đủ ngay:

| Label hiển thị | Hint text nạp vào |
|---|---|
| Văn học Việt Nam | `Dế Mèn, Tô Hoài, cổ tích, ca dao, tục ngữ` |
| Harry Potter | `Hogwarts, Voldemort, Dumbledore, Hermione, Muggle, phù thủy` |
| Lịch sử Việt Nam | `triều Nguyễn, kháng chiến, khởi nghĩa, niên hiệu` |
| Công nghệ / IT | `API, framework, backend, cloud, thuật toán` |
| Kinh doanh / Tài chính | `cổ phiếu, lãi suất, doanh thu, ngân hàng, đầu tư` |
| *(Không chọn)* | *(rỗng — không mồi gì, giữ nguyên chế độ mặc định)* |

Đây là dữ liệu tĩnh phía FE (mảng JS đơn giản), **không cần** endpoint backend
riêng để lấy danh sách này ở giai đoạn 1 — chỉ khi danh sách phình to/cần quản
lý động mới cân nhắc đưa lên server sau.

### 4.3. API: `POST /transcribe/preview` (MỚI)

Route mới, thêm vào `transcription_routes.py`, tái dùng toàn bộ logic
transcribe hiện có trong `service.py` — chỉ khác ở **không ghi/trả file**, mà
trả JSON.

**Request** (`multipart/form-data`):

| Field | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `audio_file` | File | ⚠️ Có điều kiện | Bắt buộc ở lần gọi ĐẦU TIÊN. Bỏ qua nếu đã có `job_id` từ lần gọi trước (xem mục 4.4) |
| `job_id` | string | ⚠️ Có điều kiện | Dùng khi muốn transcribe LẠI audio đã upload trước đó (vd đổi hint) mà không cần chọn file lại |
| `language` | string | ❌ | Giống endpoint cũ, để trống = tự nhận diện |
| `prompt` | string | ❌ | **Đây là ô hint** — dropdown preset hoặc gõ tay đều gửi vào field này |

Bắt buộc đúng MỘT trong hai: `audio_file` HOẶC `job_id` (giống pattern
`file`/`content` đã dùng ở route `md-to-pdf` trong `routes.py`) — thiếu cả
hai hoặc có cả hai đều trả lỗi 400.

**Response 200** (`application/json`):

```json
{
  "job_id": "a1b2c3d4e5f6...",
  "language": "vi",
  "duration": 812.4,
  "segments": [
    { "id": "seg_0001", "start": 81.32, "end": 84.10, "text": "Tôi biết dễ mẹ sẽ đến" },
    { "id": "seg_0002", "start": 85.00, "end": 88.20, "text": "Gương kia ngự trên tường" }
  ]
}
```

Ghi chú triển khai:

- Vẫn gọi `split_long_segments()` **ở bước này** (giống endpoint cũ) — để
  segment trả về đã đúng kích thước 1 cue phụ đề (~42 ký tự / ≤7s), editor ở
  FE hiển thị đúng luôn, không cần xử lý cắt thêm.
- Thêm field `id` cho mỗi segment (vd `f"seg_{i:04d}"`) — dùng làm `key` khi
  render list ở FE, không bắt buộc nhưng nên có cho an toàn (tránh dùng index
  mảng làm key nếu sau này có nhu cầu thêm/xoá dòng).
- **KHÔNG** gọi `correct_segments_with_llm()` (xem mục 0) — bỏ qua bước LLM
  hậu xử lý, giữ pipeline: transcribe → split_long_segments → trả JSON.
- Endpoint cũ `/transcribe/transcribe/audio-to-file` **giữ nguyên, không đổi**
  — vẫn hữu ích cho use case "tải nhanh không cần sửa gì".

### 4.4. Giữ audio server-side qua `job_id` — đổi hint không cần chọn lại file

**Quyết định (đã chốt):** giữ audio lại trên server sau lần preview đầu, để
user đổi hint (vd thử "không mồi" rồi thử "Văn học VN" rồi thử gõ tay riêng)
mà **không phải chọn lại file mỗi lần** — tránh trải nghiệm khó chịu.

**Cách hoạt động:**

1. Lần gọi `/transcribe/preview` đầu tiên: có `audio_file`, không có `job_id`.
   Backend lưu file vào `settings.work_dir / job_id` (dùng lại đúng hàm
   `_save_uploaded_file()` đã có trong `transcription_routes.py`), sinh
   `job_id = uuid.uuid4().hex` (giống pattern đã dùng ở `routes.py`/
   `transcription_routes.py` cho `job_dir`), trả `job_id` trong response.
2. FE lưu `job_id` vào state của trang (không phải localStorage — chỉ cần
   sống trong phiên làm việc hiện tại, mất khi F5 là chấp nhận được).
3. User đổi dropdown hint → FE gọi lại `/transcribe/preview`, lần này gửi
   `job_id` (không gửi `audio_file`). Backend tìm lại file audio đã lưu theo
   `job_id`, transcribe lại với `prompt` mới, trả `segments` mới — audio
   **không upload lại**.
4. `/transcribe/export` **không cần** `job_id` — export chỉ cần `segments`
   (đã sửa) gửi thẳng từ FE, không đụng tới audio gốc nữa.

**Chính sách dọn dẹp (bắt buộc phải có, vì giờ đã giữ file lâu hơn 1 request):**

Trước đây mỗi `job_dir` chỉ sống trong đúng 1 request rồi thôi (không ai dọn
cũng không sao vì ít phát sinh). Giờ file sống qua nhiều request của cùng 1
phiên sửa transcript → cần TTL để tránh đầy đĩa theo thời gian. Cách đơn giản
nhất, không cần thêm cron/worker riêng — **dọn kiểu lazy** ngay trong chính
route `/transcribe/preview`, trước khi tạo job mới:

```python
# Ý tưởng, đặt trong transcription_routes.py hoặc 1 util riêng
import time

JOB_TTL_SECONDS = 2 * 60 * 60  # 2 giờ — đủ cho 1 phiên sửa transcript

def _cleanup_stale_jobs(work_dir: Path, ttl_seconds: int = JOB_TTL_SECONDS) -> None:
    """Xoá các job_dir cũ hơn ttl_seconds, gọi lazy mỗi khi có request mới —
    không cần cron/worker riêng cho quy mô hiện tại."""
    now = time.time()
    if not work_dir.exists():
        return
    for entry in work_dir.iterdir():
        if entry.is_dir() and (now - entry.stat().st_mtime) > ttl_seconds:
            shutil.rmtree(entry, ignore_errors=True)
```

Gọi `_cleanup_stale_jobs(settings.work_dir)` ở đầu route `/transcribe/preview`
(chỗ nào cũng được, miễn chạy trước khi xử lý request hiện tại) — đơn giản,
đủ dùng cho quy mô hiện tại của DocForge_PyService, không cần task queue.

`job_id` bản chất là 1 capability token (uuid hex, khó đoán) — đủ an toàn cho
mức độ 1 công cụ nội bộ/cá nhân như hiện tại, **không** cần xây thêm cơ chế
xác thực/phân quyền cho `job_id` ở phạm vi tài liệu này.

---

## 5. GIAI ĐOẠN 2 — Sửa + tải (thuần FE + 1 API export)

### 5.1. Data model ở FE: `TranscriptSegment`

```ts
interface TranscriptSegment {
  id: string;      // từ backend, dùng làm key
  start: number;    // giây, KHÔNG được sửa qua UI
  end: number;      // giây, KHÔNG được sửa qua UI
  text: string;     // user sửa được — đây là phần duy nhất editable
}

// State của trang editor:
const segments = ref<TranscriptSegment[]>([]) // nạp từ response /transcribe/preview
```

### 5.2. UI Editor — bắt buộc dạng danh sách segment, KHÔNG phải 1 textarea to

**Sai** (dễ hỏng): 1 ô `<textarea>` to chứa nguyên khối text SRT thô
(`1\n00:01:21,000 --> ...\nTôi biết dễ mẹ...`) rồi để user sửa tự do — user có
thể vô tình xoá/lệch dòng số thứ tự hoặc timestamp, khiến FE không parse lại
được khi tải xuống.

**Đúng**: mỗi segment 1 dòng riêng, timestamp hiển thị **read-only**, chỉ ô
text là input được:

```
[00:01:21 - 00:01:24]  [ Tôi biết dễ mẹ sẽ đến              ]  ← sửa ô này
[00:01:25 - 00:01:28]  [ Gương kia ngự trên tường           ]
[00:01:29 - 00:01:32]  [ Ai là người đẹp nhất trần gian?    ]
```

Mỗi dòng = 1 `<input>` hoặc `<textarea>` nhỏ, `v-model` 2 chiều vào
`segments[i].text`. Timestamp chỉ hiển thị (format `mm:ss` hoặc `hh:mm:ss` tuỳ
độ dài audio), không có input nào cho `start`/`end` ở phase này.

### 5.3. Find & replace — chạy trên field `text` của TỪNG segment

Thao tác: user nhập cặp "tìm" / "thay bằng" (vd tìm `dễ mẹ`, thay bằng
`Dế Mèn`) → duyệt qua **toàn bộ `segments`**, với mỗi segment:

```js
function applyFindReplace(segments, find, replace, { caseSensitive = false } = {}) {
  const flags = caseSensitive ? 'g' : 'gi'
  const pattern = new RegExp(escapeRegExp(find), flags)
  return segments.map(seg => ({
    ...seg,
    text: seg.text.replace(pattern, replace), // CHỈ đổi text, start/end giữ nguyên
  }))
}
```

Điểm bắt buộc: hàm này **chỉ trả về bản sao mới của `text`**, không đụng tới
`start`/`end`/`id` — vì vậy dù thay bao nhiêu lần, timestamp luôn nguyên vẹn,
không có bước "parse lại SRT" nào cần thiết.

Gợi ý UX thêm (không bắt buộc phải làm ngay): preview số lượng chỗ khớp trước
khi thay, nút "Undo" 1 bước gần nhất (giữ 1 snapshot `segments` trước lần
replace gần nhất là đủ, không cần full history/stack).

### 5.4. API: `POST /transcribe/export` (MỚI)

Route mới, tái dùng `render()` đã có sẵn trong `formatter.py` — **không gọi
lại transcriber**, chỉ format text đã sửa thành file.

**Request** (`application/json`):

```json
{
  "fmt": "srt",
  "filename": "de-men-phieu-luu-ky",
  "segments": [
    { "start": 81.32, "end": 84.10, "text": "Tôi biết Dế Mèn sẽ đến" },
    { "start": 85.00, "end": 88.20, "text": "Gương kia ngự trên tường" }
  ]
}
```

(Field `id` không cần gửi lên — backend chỉ cần `start`/`end`/`text` để dựng
lại `list[Segment]` rồi gọi `render(segments, fmt)`.)

**Response 200**: `FileResponse` — `.srt`/`.vtt`/`.txt` tuỳ `fmt`, y hệt cách
endpoint cũ trả file, chỉ khác input là JSON segments thay vì audio file.

Ghi chú triển khai:

- Validate tối thiểu: `segments` không rỗng, mỗi phần tử có `start < end`,
  `text` không rỗng sau khi `.strip()` (bỏ qua dòng rỗng nếu user xoá hết text
  1 segment — coi như user chủ động xoá dòng đó khỏi phụ đề).
- `fmt` dùng lại enum `TranscriptionFormat` đã có (`srt`/`vtt`/`txt`) —
  KHÔNG cần thêm giá trị mới.
- Route này **không cần** `settings.work_dir`/job_dir phức tạp như route
  transcribe — có thể render thẳng ra response hoặc ghi file tạm rồi trả, tuỳ
  cách các route khác trong project đang làm (theo đúng pattern `FileResponse`
  hiện có trong `transcription_routes.py`/`routes.py`).

---

## 6. Việc CỐ TÌNH chưa làm ở giai đoạn này

### 6.1. Prompt nền tiếng Việt cố định (mục ưu tiên 3)

Ý tưởng: một đoạn hint **cố định, luôn được nối thêm** (không phải do user
nhập) để định hướng chính tả/dấu câu tiếng Việt nói chung — vd:

```python
# Ý tưởng cho SAU NÀY, chưa triển khai ở tài liệu này:
_VI_BASE_PROMPT = "Phiên âm tiếng Việt có dấu, viết hoa đầu câu, dùng dấu câu chuẩn."
```

Khi triển khai (sau khi mục 1, 2 đã ổn định): nối `_VI_BASE_PROMPT` vào trước
hint của user (nếu có) trước khi truyền vào `transcribe_audio(..., prompt=...)`.
Ước lượng ~3 dòng code, không cần đổi API contract đã định nghĩa ở mục 4.3.

### 6.2. Lọc `no_speech_prob` (mục ưu tiên 4, optional)

Ý tưởng: `faster-whisper` trả `no_speech_prob` cho mỗi segment (xác suất đoạn
đó thực ra là im lặng/không có lời) — segment nào có `no_speech_prob` cao bất
thường mà vẫn có `text` thường là **model ảo giác ra chữ** (vd tiếng nhạc nền,
tiếng động → bị đoán thành "pew" hay các từ tượng thanh vô nghĩa).

Khi triển khai (sau này, optional):

- Cần lưu thêm `no_speech_prob: float | None` vào `Segment` (giống cách đã
  thêm `words` trước đó) — chỉ `whisper_local.py` cung cấp được field này,
  Groq không có tương đương đáng tin cậy nên field này sẽ `None` cho engine
  Groq (giữ nguyên transcript, không lọc được ở nhánh Groq).
- Thêm 1 threshold (vd `> 0.6`) để tự động bỏ qua segment nghi ngờ, hoặc đánh
  dấu để FE hiển thị mờ/cảnh báo cho user tự quyết định giữ hay xoá — **ưu
  tiên phương án cảnh báo hơn tự xoá**, vì false positive (xoá nhầm câu thật)
  sẽ khó phát hiện hơn false negative (còn sót câu rác).

**Không đụng vào mục 6 cho tới khi mục 1 (hint) và mục 2 (editor) chạy ổn định
trên thực tế** — đúng nguyên tắc "đừng làm quá nhiều thứ cùng lúc".

---

## 7. Checklist triển khai theo đúng thứ tự

- [ ] **7.1.** Backend: thêm route `POST /transcribe/preview` trong
      `transcription_routes.py` — nhận `audio_file` HOẶC `job_id` (đúng một
      trong hai), lưu/tìm lại audio theo `job_id` (mục 4.4), transcribe +
      `split_long_segments()`, trả JSON `{ job_id, language, duration,
      segments: [{id, start, end, text}] }`, KHÔNG ghi file kết quả, KHÔNG
      gọi `correct_segments_with_llm`.
- [ ] **7.1b.** Backend: thêm `_cleanup_stale_jobs()` (mục 4.4), gọi lazy ở
      đầu route `/transcribe/preview` — TTL 2 giờ, không cần cron/worker
      riêng.
- [ ] **7.2.** Backend: thêm route `POST /transcribe/export` — nhận JSON
      segments đã sửa, dựng `list[Segment]`, gọi `render()` có sẵn trong
      `formatter.py`, trả `FileResponse`.
- [ ] **7.3.** FE: trang upload audio — thêm dropdown chủ đề preset (mục 4.2,
      static data) + ô input hint (đổ từ preset hoặc gõ tay), gọi
      `POST /transcribe/preview` (lần đầu gửi `audio_file`), nhận `segments`
      + `job_id` lưu vào state. Đổi hint sau đó → gọi lại `preview` chỉ với
      `job_id` (không hỏi lại file).
- [ ] **7.4.** FE: component Editor — render danh sách segment (mục 5.2),
      timestamp read-only, mỗi dòng 1 ô sửa `text`.
- [ ] **7.5.** FE: chức năng find & replace (mục 5.3) — chạy trên field
      `text` của toàn bộ `segments`, không đụng `start`/`end`.
- [ ] **7.6.** FE: nút "Tải xuống" — gọi `POST /transcribe/export` với
      `segments` hiện tại (đã qua sửa/find&replace), nhận file, trigger
      download giống pattern đã dùng ở `useMdToPdfConverter.js`/
      `usePdfToDocxConverter.js`.
- [ ] **7.7.** Test end-to-end: audio có từ khó (vd đoạn Dế Mèn) → thử cả 3
      chế độ hint (không mồi / preset / gõ tay) → so sánh độ chính xác →
      dùng find & replace sửa nốt → tải file → mở kiểm tra timestamp còn
      đúng.
- [ ] **7.8.** (Sau khi 7.1–7.7 ổn định) Cân nhắc triển khai mục 6.1 (prompt
      nền tiếng Việt).
- [ ] **7.9.** (Sau đó nữa, optional) Cân nhắc triển khai mục 6.2 (lọc
      `no_speech_prob`).
- [ ] **7.10.** Dọn dẹp: xem lại `postprocess.py`/`correct_with_llm` từ hướng
      cũ (mục 0) — quyết định giữ để dành hay gỡ bỏ khỏi `service.py`/
      `transcription_routes.py`/`config.py`.

---

## 8. Quyết định bổ sung (đã chốt, không còn là câu hỏi mở)

- **Giữ audio giữa các lần preview?** → **CÓ**, để tránh trải nghiệm khó chịu
  khi user muốn thử lại với hint khác. Triển khai qua cơ chế `job_id` (mục
  4.4), kèm chính sách dọn dẹp TTL 2 giờ để không phát sinh nợ kỹ thuật về
  dung lượng đĩa.
- **Giới hạn độ dài audio riêng cho preview?** → **KHÔNG** — dùng chung
  `max_audio_size` hiện có trong `config.py`, không thêm giới hạn riêng.