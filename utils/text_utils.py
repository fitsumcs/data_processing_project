import re
from typing import List
from urllib.parse import urlparse


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none"}:
        return ""
    return text


def lower_clean(value: object) -> str:
    return normalize_text(value).lower()


def strip_html(raw: str) -> str:
    return re.sub(r"<[^>]+>", " ", normalize_text(raw))


def split_keywords(text: str) -> List[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []
    parts = re.split(r"[;,/|\n]+", cleaned)
    return [p.strip().lower() for p in parts if p.strip()]


def extract_domain(value: object) -> str:
    raw = normalize_text(value).lower()
    if not raw:
        return ""

    if "@" in raw and "://" not in raw:
        return raw.split("@", 1)[1].strip().lstrip("www.")

    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    parsed = urlparse(raw)
    return parsed.netloc.lower().lstrip("www.")
