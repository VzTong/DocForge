"""Trích meta từ Markdown và gợi ý tên file đầu ra.

Tách riêng khỏi converter vì đây là business rule độc lập, dễ test, và có thể tái sử dụng (Core API C#, FE, CLI,... đều dùng chung API)."""
from __future__ import annotations

import re
import unicodedata

# Bảng viết tắt chức danh phổ biến (key luôn viết thường, không dấu và không khoảng trắng)
ROLE_ABBREVIATIONS: dict[str, str] = {
    # Cụm BE có thể viết tắt thành BE, nhưng không nên viết tắt thành BSE (Backend Software Engineer) vì dễ gây nhầm lẫn với BS (Bác sĩ).
    "backend developer": "BE",
    "backend engineer": "BE",
    "backend software engineer": "BE",
    "back-end developer": "BE",
    "back-end engineer": "BE",
    "back-end software engineer": "BE",
    # Cụm FE và FS có thể viết tắt thành FE và FS, nhưng không nên viết tắt thành BSE (Backend Software Engineer) vì dễ gây nhầm lẫn với BS (Bác sĩ).
    "frontend developer": "FE",
    "frontend engineer": "FE",
    "frontend software engineer": "FE",
    "front-end developer": "FE",
    "front-end engineer": "FE",
    "front-end software engineer": "FE",
    # Cụm FS
    "fullstack developer": "FS",
    "fullstack engineer": "FS",
    "fullstack software engineer": "FS",
    "full-stack developer": "FS",
    "full-stack engineer": "FS",
    "full-stack software engineer": "FS",
    # Cụm SE
    "software engineer": "SE",
    "software developer": "SE",
    # Các cụm khác
    "data engineer": "DE",
    "data scientist": "DS",
    "data analyst": "DA",
    "data science engineer": "DSE",
    "ai engineer": "AI",
    "machine learning engineer": "MLE",
    "machine learning scientist": "MLS",
    "artificial intelligence engineer": "AIE",
    "deep learning engineer": "DLE",
    "deep learning scientist": "DLS",
    "devops engineer": "DevOps",
    "qa engineer": "QA",
    "quality assurance engineer": "QA",
    "test engineer": "TE",
    "test automation engineer": "TAE",
    "security engineer": "SE",
    "business analyst": "BA",
    "product manager": "PdM",
    "project manager": "PM",
    "ui/ux designer": "UI/UX",
    "mobile developer": "MOB",
    "android developer": "AND",
    "ios developer": "IOS",
    "kỹ sư": "KS",
    "kỹ sư phần mềm": "KSPM",
    "kỹ sư phần mềm cao cấp": "KSPMCC",
    "trưởng nhóm": "TN",
    "trưởng nhóm phát triển": "TNPT",
    "trưởng nhóm phát triển phần mềm": "TNPTPM",
    "trưởng nhóm phát triển phần mềm cao cấp": "TNPTPMCC",
}

def strip_accents(text: str) -> str:
    """Loại bỏ dấu tiếng Việt và các ký tự Unicode khác. Lưu ý: không loại bỏ ký tự đặc biệt như @, #, $, %, &, *, (, ), -, _, +, =, {, }, [, ], |, \, :, ;, ", ', <, >, ,, ., ?, /

    Và đ/Đ không tự tách được nên phải tách thủ công bằng cách thay thế đ -> d và Đ -> D trước khi gọi hàm unicodedata.normalize."""
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text

def extract_title_subtitle(md_text:str) -> tuple[str | None, str | None]:
    """Trích tiêu đề và phụ đề từ Markdown.

    Tiêu đề: dòng đầu tiên bắt đầu bằng # (Markdown heading level 1).
    Phụ đề: dòng tiếp theo không rỗng, không phải heading, không phải comment HTML.
    """
    title = subtitle = None
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("<!--"):
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            # Tìm phụ đề
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith("#") and not next_line.startswith("<!--"):
                    subtitle = next_line
                    break
            break
        if title is None:
            if line.startswith(("|", "-", ">", "`")):
                continue
            title = re.sub(r"^#+\s*", "", line).strip()
        else:
            if line.startswith(("|", "```", "---")):
                break
            sub = re.sub(r"^#{1,6}\s*", "", line)
            sub = re.sub(r"[*_`]", "", sub).strip()
            if sub:
                subtitle = sub
            break
    return title or None, subtitle or None

def split_document_header(md_text: str) -> tuple[str, str | None, str | None, str | None, str | None, str]:
    """Tách phần header Markdown ở đầu tài liệu ra khỏi body.

    Trả về:
        - title: dòng H1 đầu tiên
        - subtitle: dòng tiếp theo hợp lệ
        - contact: dòng tiếp theo không rỗng, thường là email/phone
        - address: dòng tiếp theo nếu có, thường là địa chỉ
        - links: dòng tiếp theo nếu có, thường là LinkedIn/GitHub
        - body: phần Markdown còn lại sau khi bỏ các dòng header

    Helper này được dùng cho preview CV để tránh render lặp tên/chức danh/liên hệ.
    """
    lines = md_text.splitlines()
    title = None
    subtitle = None
    contact = None
    address = None
    links = None
    body_start_index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            continue
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            body_start_index = i + 1
            break
        if stripped.startswith(("|", "-", ">", "`")):
            continue
        title = re.sub(r"^#+\s*", "", stripped).strip()
        body_start_index = i + 1
        break

    if title is not None:
        header_values: list[str] = []
        for j in range(body_start_index, len(lines)):
            stripped = lines[j].strip()
            if not stripped or stripped.startswith("<!--"):
                continue
            if stripped.startswith("---"):
                body_start_index = j + 1
                break
            if stripped.startswith("#") and header_values:
                body_start_index = j
                break

            header_values.append(stripped)
            body_start_index = j + 1

            if len(header_values) >= 4:
                break

        if header_values:
            subtitle = header_values[0] if len(header_values) > 0 else None
            contact = header_values[1] if len(header_values) > 1 else None
            address = header_values[2] if len(header_values) > 2 else None
            links = header_values[3] if len(header_values) > 3 else None

    body = "\n".join(lines[body_start_index:]).lstrip("\n")
    return title or None, subtitle or None, contact or None, address or None, links or None, body

def abbreviate_role(subtitle: str) -> str:
    """Rút gọn chức danh trong tiêu đề bằng cách thay thế các cụm từ phổ biến bằng viết tắt.

    Ví dụ: "Senior Backend Software Engineer" -> "Senior BE"
    """
    if not subtitle:
        return ""
    key = re.sub(r"\s+", " ", subtitle.lower().strip())
    if key in ROLE_ABBREVIATIONS:
        return ROLE_ABBREVIATIONS[key]

    stop = {"of", "and", "the", "a", "an", "for", "in", "at", "viên", "chuyên"}
    words = [w for w in re.findall(r"[A-Za-zÀ-ỹ]+", strip_accents(subtitle))
             if w.lower() not in stop]
    if not words:
        return ""
    if len(words) == 1:
        return words[0][:6].capitalize() # Lấy tối đa 6 ký tự đầu tiên của từ duy nhất, viết hoa chữ cái đầu
    return "".join(w[0].upper() for w in words[:4])  # Lấy chữ cái đầu của tối đa 4 từ đầu tiên, viết hoa tất cả

def suggest_output_filename(
    md_text: str,
    default: str = "document",
    *,
    title: str | None = None,
    subtitle: str | None = None,
) -> str:
    """Gợi ý tên file đầu ra dựa trên tiêu đề và phụ đề trong Markdown.

    Nếu không tìm thấy tiêu đề, trả về "output.pdf".
    Nếu chỉ có tiêu đề, trả về "title.pdf".
    Nếu có tiêu đề và phụ đề, trả về "title_subtitle.pdf" (với subtitle được rút gọn).
    """
    if title is None or subtitle is None:
        extracted_title, extracted_subtitle = extract_title_subtitle(md_text)
        title = title or extracted_title
        subtitle = subtitle or extracted_subtitle
    name = "".join(w.capitalize() for w in strip_accents(title).split()) if title else ""
    role = abbreviate_role(subtitle) if subtitle else ""
    out = "_".join(p for p in [name, role] if p)
    out = re.sub(r"[^A-Za-z0-9._-]", "", out) # Loại bỏ ký tự đặc biệt, chỉ giữ lại chữ cái, số, dấu chấm, gạch dưới và gạch ngang
    return out[:80] or default