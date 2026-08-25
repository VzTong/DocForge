"""Engine B - Groq API (Whisper large-v3).
Cần: pip install groq
Env: GROQ_API_KEY, (optional) GROQ_MODEL, GROQ_MAX_BYTES
"""
from __future__ import annotations

import os
from pathlib import Path

from app.core.config import settings
from app.media.transcription.base import (
    TranscriberBase,
    TranscriptionResult,
    Segment,
    TranscriptionError,
)


def _extract_segments(resp) -> tuple[list[Segment], str | None, float | None]:
    """Chuẩn hóa response verbose_json -> (segments, language, duration)."""
    # Groq SDK trả object; cũng hỗ trợ dict
    if isinstance(resp, dict):
        raw_segments = resp.get("segments") or []
        language = resp.get("language")
        duration = resp.get("duration")
    else:
        raw_segments = getattr(resp, "segments", None) or []
        language = getattr(resp, "language", None)
        duration = getattr(resp, "duration", None)

    segments: list[Segment] = []
    for s in raw_segments:
        if isinstance(s, dict):
            start, end, text = s.get("start"), s.get("end"), s.get("text", "")
        else:
            start = getattr(s, "start", None)
            end = getattr(s, "end", None)
            text = getattr(s, "text", "") or ""

        if start is None or end is None:
            continue
        segments.append(Segment(float(start), float(end), text.strip()))

    return segments, language, duration


class GroqTranscriber(TranscriberBase):
    name = "groq"

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.model = model or settings.groq_model or os.getenv("GROQ_MODEL", "whisper-large-v3")
        self.api_key = api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise TranscriptionError(
                "GROQ_API_KEY chưa được thiết lập. "
                "Hãy set trong .env hoặc truyền api_key khi khởi tạo."
            )
        self.max_bytes = settings.groq_max_bytes

    def transcribe(
        self,
        audio_path,
        language: str | None = None,
        prompt: str | None = None,
    ) -> TranscriptionResult:
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise TranscriptionError(f"File audio không tồn tại: {audio_path}")

        size = audio_path.stat().st_size
        if size > self.max_bytes:
            raise TranscriptionError(
                f"File audio quá lớn ({size} bytes). "
                f"Groq API giới hạn ~{self.max_bytes // (1024 * 1024)}MB/file."
            )

        try:
            from groq import Groq
        except ImportError as e:
            raise TranscriptionError("groq chưa được cài. Chạy: pip install groq") from e

        try:
            client = Groq(api_key=self.api_key)
            with audio_path.open("rb") as f:
                # ĐÃ SỬA: trước đây fallback cứng "vi" khi không truyền language, khiến
                # Groq luôn bị ép decode như tiếng Việt kể cả khi audio không phải —
                # sai lệch với whisper_local.py (ở đó None = auto-detect). Giờ đồng nhất:
                # chỉ set "language" khi caller thực sự truyền vào, còn lại để Groq tự nhận diện.
                lang = language.strip() if language and str(language).strip() else None
                create_kwargs = {
                    "file": (audio_path.name, f.read()),
                    "model": self.model,
                    "response_format": "verbose_json",
                    "temperature": 0.0,
                }
                if lang:
                    create_kwargs["language"] = lang
                if prompt and str(prompt).strip():
                    create_kwargs["prompt"] = prompt.strip()

                resp = client.audio.transcriptions.create(**create_kwargs)
        except Exception as e:
            raise TranscriptionError(f"Transcription failed: {e}") from e

        segments, detected_lang, duration = _extract_segments(resp)
        if not segments:
            raise TranscriptionError(
                "Groq API trả về kết quả rỗng. "
                "Có thể file không có lời nói hoặc API gặp sự cố."
            )

        return TranscriptionResult(
            segments=segments,
            language=detected_lang or language,
            duration=duration,
        )