"""Orchestrate: audio -> transcribe -> (optional split) -> format ra file."""
from __future__ import annotations

from pathlib import Path

from app.media.transcription.factory import get_transcriber
from app.media.transcription.formatter import (
    TranscriptionFormat,
    merge_chunk_segments,
    render,
    split_long_segments,  # hậu xử lý SRT
)


def transcribe_audio(
    audio_path: Path,
    out_dir: Path,
    fmt: TranscriptionFormat = TranscriptionFormat.SRT,
    language: str | None = None,
    filename: str = "transcript",
    prompt: str | None = None,
) -> Path:
    """Transcribe audio và lưu file theo fmt.

    prompt: chỉ dùng khi caller chủ động truyền (advanced/dev).
    User thường không cần — production để None.
    """
    transcriber = get_transcriber()
    result = transcriber.transcribe(audio_path, language=language, prompt=prompt)

    segments = result.segments
    # Chỉ tách segment khi xuất phụ đề có timeline (SRT/VTT)
    if fmt in (TranscriptionFormat.SRT, TranscriptionFormat.VTT):
        segments = split_long_segments(segments, max_chars=42, max_duration=7.0)

    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{filename}.{fmt.value}"
    output_path.write_text(render(segments, fmt), encoding="utf-8")
    return output_path


def transcribe_audio_chunks(
    chunk_paths,
    chunk_offsets,
    out_dir,
    fmt: TranscriptionFormat = TranscriptionFormat.SRT,
    language=None,
    filename="transcript",
    prompt: str | None = None,
):
    """Transcribe nhiều chunk rồi merge timeline."""
    transcriber = get_transcriber()
    chunk_segments = []
    for chunk_path in chunk_paths:
        result = transcriber.transcribe(chunk_path, language=language, prompt=prompt)
        chunk_segments.append(result.segments)

    merged = merge_chunk_segments(chunk_segments, chunk_offsets)
    if fmt in (TranscriptionFormat.SRT, TranscriptionFormat.VTT):
        merged = split_long_segments(merged)

    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{filename}.{fmt.value}"
    output_path.write_text(render(merged, fmt), encoding="utf-8")
    return output_path