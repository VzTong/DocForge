"""Đảm bảo pytest tìm thấy package `app` khi chạy từ thư mục DocForge_PyService."""
import sys
from pathlib import Path

# Thêm thư mục gốc của project vào sys.path để pytest tìm thấy package `app`
sys.path.insert(0, str(Path(__file__).parent))