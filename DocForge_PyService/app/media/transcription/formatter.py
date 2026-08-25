"""Format list[Segment] thành các định dạng khác nhau (srt, vtt, txt, json, v.v.) KHÔNG phụ thuộc vào engine transcription nào cả.
+ hậu xử lý cắt câu cho phụ đề."""
from __future__ import annotations

import re
from enum import Enum
from app.media.transcription.base import Segment, Word

class TranscriptionFormat(str, Enum):
    """Các định dạng xuất kết quả transcription"""
    SRT = "srt"
    VTT = "vtt"
    TXT = "txt"

def _format_ts(seconds: float, sep: str = ",") -> str:
    """Giây -> timestamp (HH:MM:SS,mmm) (SRT) hoặc (HH:MM:SS.mmm) (VTT)"""
    if seconds < 0:
        seconds = 0
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600_000) # 3600_000 ms = 1 giờ / 3600_000 <=> 3600 * 1000
    m, ms = divmod(ms, 60_000)   # 60_000 ms = 1 phút
    s, ms = divmod(ms, 1000)     # 1000 ms = 1 giây
    return f"{h:02}:{m:02}:{s:02}{sep}{ms:03}"

def to_str(segment: list[Segment]) -> str:
    """Chuyển list[Segment] thành định dạng SRT (SubRip)"""
    block = []
    for i, seg in enumerate(segment, start=1):
        block.append(f"{i}\n{_format_ts(seg.start)} --> {_format_ts(seg.end)}\n{seg.text}\n")

    return "\n".join(block).strip()

def to_vtt(segment: list[Segment]) -> str:
    """Chuyển list[Segment] thành định dạng VTT (WebVTT)"""
    block = ["WEBVTT\n"]
    for seg in segment:
        block.append(f"{_format_ts(seg.start, sep='.') } --> {_format_ts(seg.end, sep='.')}\n{seg.text}\n")

    return "\n".join(block).strip()

def to_txt(segment: list[Segment]) -> str:
    """Chuyển list[Segment] thành định dạng TXT (plain text)"""
    return "\n".join(seg.text for seg in segment).strip()

def render(segments: list[Segment], fmt: TranscriptionFormat) -> str:
    """Chuyển list[Segment] thành định dạng `fmt`"""
    return {
        TranscriptionFormat.SRT: to_str,
        TranscriptionFormat.VTT: to_vtt,
        TranscriptionFormat.TXT: to_txt,
    }[fmt](segments)

def merge_chunk_segments(
        chunk_segments: list[list[Segment]],
        chunk_offset: list[float],
    ) -> list[Segment]:
    """Gộp các list[Segment] từ nhiều chunk audio thành một list[Segment] duy nhất, cộng offset để timeline đúng tuyệt đối"""
    merged: list[Segment] = []
    for segments, offset in zip(chunk_segments, chunk_offset):
        merged.extend(seg.shifted(offset) for seg in segments)
    return merged

# ---------------------------------------------------------------------------
# Hậu xử lý: cắt segment dài theo dấu câu / giới hạn độ dài (cho phụ đề)
# ---------------------------------------------------------------------------

# Tách ưu tiên sau các dấu này (giữ dấu ở cuối câu trước)
_SPLIT_PUNCT = re.compile(r"(?<=[.,!?;:…])\s+")


def _split_by_words(seg: Segment, max_chars: int, max_duration: float) -> list[Segment]:
    """Cắt segment dài dựa trên mốc thời gian THẬT của từng từ (seg.words).
    Chính xác hơn hẳn cách ước lượng theo tỷ lệ ký tự vì dùng đúng timestamp
    faster-whisper trả về cho mỗi từ."""
    pieces: list[Segment] = []
    buf_words: list[Word] = []
    buf_start = seg.words[0].start

    def flush(end_time: float):
        if not buf_words:
            return
        text = " ".join(w.text for w in buf_words).strip()
        if text:
            pieces.append(Segment(buf_start, end_time, text))

    for w in seg.words:
        trial_text = " ".join([*(x.text for x in buf_words), w.text]).strip()
        trial_duration = w.end - buf_start
        would_overflow = buf_words and (len(trial_text) > max_chars or trial_duration > max_duration)

        if would_overflow:
            flush(buf_words[-1].end)
            buf_words = [w]
            buf_start = w.start
        else:
            buf_words.append(w)

    flush(seg.words[-1].end if buf_words else seg.end)
    return pieces or [Segment(seg.start, seg.end, seg.text)]


def split_long_segments(
    segments: list[Segment],
    max_chars: int = 42,
    max_duration: float = 7.0,
) -> list[Segment]:
    """Tách segment quá dài để SRT/VTT dễ đọc.

    - max_chars: độ dài text tối đa mỗi cue (phụ đề thường ~32–42 ký tự/dòng)
    - max_duration: số giây tối đa mỗi cue

    Có word-level timestamp (whisper-local) -> cắt đúng theo thời gian nói thật.
    Không có (Groq trả segment-level only) -> fallback về cách cũ: chia đều thời
    gian theo tỷ lệ độ dài từng mảnh text (không chính xác từng từ, nhưng đủ tốt).
    """
    result: list[Segment] = []

    for seg in segments:
        text = (seg.text or "").strip()
        if not text:
            continue

        duration = max(seg.end - seg.start, 0.01)
        need_split = len(text) > max_chars or duration > max_duration

        if not need_split:
            result.append(Segment(seg.start, seg.end, text))
            continue

        # Có word-level timestamp thật (whisper-local) -> ưu tiên dùng, chính xác hơn hẳn
        if seg.words:
            result.extend(_split_by_words(seg, max_chars, max_duration))
            continue

        # --- Fallback cũ: không có word-level (vd: Groq) -> ước lượng theo tỷ lệ ký tự ---
        # 1) Thử tách theo dấu câu
        parts = [p.strip() for p in _SPLIT_PUNCT.split(text) if p.strip()]

        # 2) Nếu vẫn còn mảnh quá dài → cắt theo số từ
        refined: list[str] = []
        for part in parts or [text]:
            if len(part) <= max_chars:
                refined.append(part)
                continue
            words = part.split()
            buf: list[str] = []
            for w in words:
                trial = (" ".join(buf + [w])).strip()
                if buf and len(trial) > max_chars:
                    refined.append(" ".join(buf))
                    buf = [w]
                else:
                    buf.append(w)
            if buf:
                refined.append(" ".join(buf))

        if len(refined) <= 1:
            result.append(Segment(seg.start, seg.end, text))
            continue

        # Chia thời gian tỷ lệ theo độ dài ký tự từng mảnh
        total_len = sum(len(p) for p in refined) or 1
        t = seg.start
        for i, part in enumerate(refined):
            ratio = len(part) / total_len
            piece_dur = duration * ratio
            end = seg.end if i == len(refined) - 1 else t + piece_dur
            # Đảm bảo end > start
            if end <= t:
                end = t + 0.05
            result.append(Segment(t, min(end, seg.end), part))
            t = end

    return result