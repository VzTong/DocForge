
from enum import Enum

class PageSize(str, Enum):
    """Supported PDF page sizes."""

    A4 = "A4"
    LETTER = "Letter"