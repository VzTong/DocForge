"""API endpoints for transcription-related operations."""
from __future__ import annotations

import shutil
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse, Response

from app.core.config import settings
from app.media.transcription.base import TranscriptionError, Segment
from app.media.transcription.formatter import TranscriptionFormat, render
from app.media.transcription.service import transcribe_audio

router = APIRouter(prefix="/transcribe", tags=["Transcription"])

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac", ".wma", ".alac", ".opus"}


def _save_uploaded_file(upload_file: UploadFile, dest_path: Path) -> Path:
    """Lưu tệp đã tải lên vào đường dẫn đích"""
    dest_path.mkdir(parents=True, exist_ok=True)
    dest_file_path = dest_path / Path(upload_file.filename or "audio").name
    size = 0
    with dest_file_path.open("wb") as buffer:
        while chunk := upload_file.file.read(1024 * 1024):
            size += len(chunk)
            if size > settings.max_audio_size:
                buffer.close()
                shutil.rmtree(dest_path, ignore_errors=True)
                raise HTTPException(
                    status_code=413,
                    detail="File quá lớn. Vui lòng tải lên tệp nhỏ hơn.",
                )
            buffer.write(chunk)
    return dest_file_path


def _cleanup_stale_jobs(work_dir: Path, ttl_seconds: int = 2 * 60 * 60) -> None:
    """Xoá các job_dir cũ hơn ttl_seconds, gọi lazy mỗi khi có request mới"""
    now = time.time()
    if not work_dir.exists():
        return
    for entry in work_dir.iterdir():
        if entry.is_dir() and (now - entry.stat().st_mtime) > ttl_seconds:
            shutil.rmtree(entry, ignore_errors=True)


@router.get("/health", summary="Kiểm tra trạng thái của dịch vụ transcription")
async def health_check():
    return {"status": "ok"}


@router.get("/format", summary="Danh sách các định dạng xuất kết quả transcription")
async def get_transcription_formats() -> dict:
    return {"formats": [fmt.value for fmt in TranscriptionFormat]}


@router.post(
    "/transcribe/audio-to-file",
    summary="Transcribe audio file và lưu kết quả ra file định dạng `fmt`",
    responses={
        200: {"description": "File transcription đã được tạo thành công."},
        400: {"description": "Yêu cầu không hợp lệ."},
        413: {"description": "File quá lớn."},
        422: {"description": "Lỗi transcription."},
        500: {"description": "Lỗi server."},
    },
)
async def transcribe_audio_to_file(
    audio_file: UploadFile = File(..., description="File audio"),
    fmt: TranscriptionFormat = Form(TranscriptionFormat.SRT),
    language: str | None = Form(
        None,
        description="Mã ngôn ngữ (vd: vi, en). Để trống = tự nhận diện",
    ),
    prompt: str | None = Form(
        None,
        description="Gợi ý ngữ cảnh / từ khó (optional). VD: 'Truyện Dế Mèn phiêu lưu ký'",
    ),
) -> FileResponse:
    filename = audio_file.filename or ""
    ext = Path(filename).suffix.lower()
    if not filename or ext not in AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File không hợp lệ. Chỉ chấp nhận: {', '.join(sorted(AUDIO_EXTENSIONS))}",
        )

    lang = language.strip() if language and language.strip() else None
    user_prompt = prompt.strip() if prompt and prompt.strip() else None

    job_dir = settings.work_dir / uuid.uuid4().hex
    try:
        audio_path = _save_uploaded_file(audio_file, job_dir)
        output_path = transcribe_audio(
            audio_path,
            job_dir / "output",
            fmt=fmt,
            language=lang,
            filename=Path(filename).stem,
            prompt=user_prompt,
        )
    except TranscriptionError as e:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise HTTPException(
            status_code=422,
            detail=f"Lỗi khi xử lý transcription: {e}",
        ) from e
    except Exception:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise

    media_map = {
        TranscriptionFormat.SRT: "application/x-subrip",
        TranscriptionFormat.VTT: "text/vtt",
        TranscriptionFormat.TXT: "text/plain",
    }
    media = media_map.get(fmt, "application/octet-stream")

    return FileResponse(
        path=output_path,
        media_type=media,
        filename=output_path.name,
    )


@router.post(
    "/preview",
    summary="Transcribe audio và trả về segments để preview (không lưu file)",
    responses={
        200: {"description": "Transcription thành công, trả về segments"},
        400: {"description": "Yêu cầu không hợp lệ."},
        413: {"description": "File quá lớn."},
        422: {"description": "Lỗi transcription."},
        500: {"description": "Lỗi server."},
    },
)
async def transcribe_preview(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile | None = File(None, description="File audio"),
    job_id: str | None = Form(None, description="ID của job đã upload trước đó"),
    language: str | None = Form(
        None,
        description="Mã ngôn ngữ (vd: vi, en). Để trống = tự nhận diện",
    ),
    prompt: str | None = Form(
        None,
        description="Gợi ý ngữ cảnh / từ khó (optional). VD: 'Truyện Dế Mèn phiêu lưu ký'",
    ),
):
    """
    Either audio_file (for first upload) or job_id (for re-transcribe with same audio) must be provided.
    Returns job_id, language, duration, and segments.
    """
    # Cleanup stale jobs (lazy cleanup)
    _cleanup_stale_jobs(settings.work_dir)

    # Validate input: exactly one of audio_file or job_id
    if bool(audio_file) == bool(job_id):
        raise HTTPException(
            status_code=400,
            detail="Phải cung cấp đúng một trong hai: audio_file hoặc job_id",
        )

    lang = language.strip() if language and language.strip() else None
    user_prompt = prompt.strip() if prompt and prompt.strip() else None

    if audio_file:
        # First upload: save audio and generate job_id
        job_id = uuid.uuid4().hex
        job_dir = settings.work_dir / job_id
        try:
            audio_path = _save_uploaded_file(audio_file, job_dir)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Lỗi lưu file: {e}")
    else:
        # Re-transcribe: find audio file by job_id
        job_dir = settings.work_dir / job_id
        if not job_dir.is_dir():
            raise HTTPException(status_code=404, detail="Job không tồn tại")
        # Find the audio file (assuming only one file in job_dir, ignoring subdirectories)
        items = [item for item in job_dir.iterdir() if item.is_file()]
        if not items:
            raise HTTPException(status_code=404, detail="Không tìm thấy file audio cho job_id")
        audio_path = items[0]

    try:
        # Transcribe (we don't need to save output file, just get segments)
        # We'll use transcribe_audio but with a dummy output directory and filename, then discard the file.
        # Alternatively, we can modify transcribe_audio to return segments? But we don't want to change service.py.
        # Let's create a temporary output directory, transcribe, then read the segments from the generated file?
        # That's wasteful. Instead, let's call the transcriber directly and get the result.
        from app.media.transcription.factory import get_transcriber
        transcriber = get_transcriber()
        result = transcriber.transcribe(audio_path, language=lang, prompt=user_prompt)
        segments = result.segments
        # Apply split_long_segments for SRT/VTT (since we are returning segments for editing, we want them split)
        from app.media.transcription.formatter import split_long_segments
        segments = split_long_segments(segments, max_chars=42, max_duration=7.0)
        # Add id to each segment
        segments_with_id = [
            {"id": f"seg_{i:04d}", "start": seg.start, "end": seg.end, "text": seg.text}
            for i, seg in enumerate(segments)
        ]
        return {
            "job_id": job_id,
            "language": lang or "auto",
            "duration": result.duration,
            "segments": segments_with_id,
        }
    except TranscriptionError as e:
        # If we created a job_dir for this request, clean it up
        if audio_file:
            shutil.rmtree(job_dir, ignore_errors=True)
        raise HTTPException(
            status_code=422,
            detail=f"Lỗi khi xử lý transcription: {e}",
        ) from e
    except Exception as e:
        if audio_file:
            shutil.rmtree(job_dir, ignore_errors=True)
        raise


@router.post(
    "/export",
    summary="Xuất transcript đã sửa thành file (SRT/VTT/TXT)",
    responses={
        200: {"description": "File đã được tạo và gửi về"},
        400: {"description": "Yêu cầu không hợp lệ."},
        422: {"description": "Lỗi dữ liệu segments."},
        500: {"description": "Lỗi server."},
    },
)
async def transcribe_export(
    fmt: TranscriptionFormat = Form(TranscriptionFormat.SRT),
    filename: str | None = Form(None, description="Tên file không bao gồm phần mở rộng"),
    segments: str = Form(..., description="Danh sách segments dưới dạng JSON string"),
):
    """
    Expects a JSON string of segments: [{"start": float, "end": float, "text": str}, ...]
    Returns a file of the specified format.
    """
    import json
    try:
        segments_list = json.loads(segments)
        if not isinstance(segments_list, list):
            raise ValueError("Segments must be a list")
        if not segments_list:
            raise ValueError("Segments list cannot be empty")
        # Convert to Segment objects
        seg_objects = []
        for i, seg in enumerate(segments_list):
            if not isinstance(seg, dict):
                raise ValueError(f"Segment at index {i} is not an object")
            start = seg.get("start")
            end = seg.get("end")
            text = seg.get("text")
            if start is None or end is None or text is None:
                raise ValueError(f"Segment at index {i} missing start, end, or text")
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                raise ValueError(f"Segment at index {i} start and end must be numbers")
            if start >= end:
                raise ValueError(f"Segment at index {i} start must be less than end")
            if not isinstance(text, str):
                raise ValueError(f"Segment at index {i} text must be a string")
            text = text.strip()
            if not text:
                # Skip empty text segments (user may have cleared text)
                continue
            seg_objects.append(Segment(start=float(start), end=float(end), text=text))
        if not seg_objects:
            raise ValueError("All segments have empty text after stripping")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Render the segments
    try:
        rendered = render(seg_objects, fmt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi render: {e}")

    # Determine media type and filename
    media_map = {
        TranscriptionFormat.SRT: "application/x-subrip",
        TranscriptionFormat.VTT: "text/vtt",
        TranscriptionFormat.TXT: "text/plain",
    }
    media = media_map.get(fmt, "application/octet-stream")
    if not filename:
        filename = "transcript"
    # Ensure filename has no extension (we'll add it)
    safe_filename = Path(filename).stem
    download_filename = f"{safe_filename}.{fmt.value}"

    # Return as Response with appropriate headers
    return Response(
        content=rendered,
        media_type=media,
        headers={"Content-Disposition": f'attachment; filename="{download_filename}"'},
    )