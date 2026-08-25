"""Interface & data model cho transcription service (audio -> text)."""
from __future__ import annotations

import abc
from dataclasses import dataclass

class TranscriptionError(Exception):
    """Lỗi khi transcription service gặp vấn đề, ví dụ: không thể kết nối, file audio không hợp lệ, thiếu engine, v.v."""

@dataclass
class Word:
    """Một từ có mốc thời gian riêng (chỉ có khi engine hỗ trợ word-level timestamp)"""
    start: float
    end: float
    text: str

@dataclass
class Segment:
    """Một đoạn lời nói có mốc thời gian (giây, tính từ đầu audio)"""
    start: float
    end: float
    text: str
    words: list[Word] | None = None  # None = engine không hỗ trợ word-level (vd: Groq)

    def shifted(self, delta: float) -> Segment:
        """Trả về một bản sao của đoạn này với mốc thời gian được dịch chuyển"""
        shifted_words = (
            [Word(w.start + delta, w.end + delta, w.text) for w in self.words]
            if self.words else None
        )
        return Segment(start=self.start + delta, end=self.end + delta, text=self.text, words=shifted_words)

@dataclass
class TranscriptionResult:
    """Kết quả của một phiên transcription"""
    segments: list[Segment]
    language: str | None = None
    duration: float | None = None

class TranscriberBase(abc.ABC):
    """Giao diện chung cho mọi engine transcription. Các engine cụ thể sẽ kế thừa và triển khai các phương thức này."""
    name: str = "base"

    @abc.abstractmethod
    def transcribe(self, audio_path, language: str | None = None, prompt: str | None = None) -> TranscriptionResult:
        """Thực hiện transcription cho file audio tại `audio_path`. Nếu `language` được cung cấp, engine sẽ ưu tiên sử dụng ngôn ngữ đó."""
        raise NotImplementedError