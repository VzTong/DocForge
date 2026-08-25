"""Cấu hình tập trung cho DocForge_PyService.
Đọc từ biến môi trường (12-factor). Dùng WeasyPrint (thuần python) nên KHÔNG cần dò đường dẫn Chrome."""
from __future__ import annotations

import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Cấu hình tập trung cho DocForge_PyService."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",          # ← thêm dòng này
    )

    app_name: str = "DocForge_PyService"
    debug: bool = True
    version: str = "0.1.0"

    # Thư mục làm việc tạm (I/O). Docker sẽ mount volume vào đây. Nếu không có thì tạo tạm trong /tmp
    work_dir: Path = (
        Path("/tmp/docforge_workdir")
        if not sys.platform.startswith("win")
        else Path.home() / "docforge_tmp"
    )

    # Giới hạn dung lượng upload file (bytes). Mặc định 20MB
    max_file_size: int = 20 * 1024 * 1024

    # Giới hạn dung lượng upload file cho audio (bytes). Mặc định 100MB
    max_audio_size: int = 100 * 1024 * 1024

    # Whisper model settings | whisper-local (dev) or whisper-large-v3 (Groq API)
    transcription_engine: str = "Groq"
    whisper_model: str = "medium"
    # GROQ_MODEL
    groq_api_key: str = ""
    groq_model: str = "whisper-large-v3"
    groq_max_bytes: int = 25 * 1024 * 1024

settings = Settings()
settings.work_dir.mkdir(parents=True, exist_ok=True)  # tạo thư mục làm việc nếu chưa có