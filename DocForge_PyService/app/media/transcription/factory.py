"""Chọn engine transcription phù hợp dựa trên môi trường triển khai (local, GPU, cloud, v.v.)
Đổi ENGINE mặc định bằng cách cài đặt biến môi trường TRANSCRIBER_ENGINE=whisper-local|groq|..."""
from __future__ import annotations

import os
from functools import lru_cache
from app.core.config import settings
from app.media.transcription.base import TranscriberBase


@lru_cache(maxsize=1)
def get_transcriber() -> TranscriberBase:
    """Lấy engine transcription phù hợp dựa trên biến môi trường TRANSCRIBER_ENGINE."""
    engine = (settings.transcription_engine or "whisper-local").strip().lower()

    if engine in ("groq", "whisper-large-v3"):
        from app.media.transcription.groq_api import GroqTranscriber
        return GroqTranscriber()

    # mặc định local
    from app.media.transcription.whisper_local import WhisperLocalTranscriber
    return WhisperLocalTranscriber(model_size=settings.whisper_model or "base")

def reset_cache() -> None:
    """Xóa cache của get_transcriber để có thể tạo lại engine mới."""
    get_transcriber.cache_clear()