from typing import List, Tuple

from utils.req_parser import ParsedReq
from utils.text_utils import lower_clean


LEVEL_PATTERNS = {
    "director": ["director", "head", "vp", "vice president", "chief", "cfo", "ceo", "coo", "cto", "cio"],
    "manager": ["manager", "lead", "director", "head", "vp", "chief"],
}


def _extract_level_bucket(job_level: str) -> str:
    text = lower_clean(job_level)
    if "director +" in text or "director+" in text:
        return "director"
    if "manager +" in text or "manager+" in text:
        return "manager"
    return ""


def _keyword_check(title: str, keywords: List[str]) -> bool:
    if not keywords:
        return True

    # Keep this conservative for noisy keyword lists in free-form req text.
    compact_keywords = [k for k in keywords if len(k) >= 4 and k not in {"any", "-", "see comment"}]
    if not compact_keywords:
        return True

    for kw in compact_keywords[:40]:
        if kw in title:
            return True
    return False


def _level_check(title: str, bucket: str) -> bool:
    if not bucket:
        return True
    patterns = LEVEL_PATTERNS.get(bucket, [])
    return any(p in title for p in patterns)


def validate_title_against_req(title_value: object, parsed_req: ParsedReq) -> Tuple[str, str]:
    title = lower_clean(title_value)
    if not title:
        return "INVALID", "Title is missing."

    level_bucket = _extract_level_bucket(parsed_req.job_level)
    keyword_ok = _keyword_check(title, parsed_req.keywords)
    level_ok = _level_check(title, level_bucket)

    if keyword_ok and level_ok:
        return "VALID", "Title matches requirement keywords and level."

    if not keyword_ok and not level_ok:
        return "INVALID", "Title does not match required keywords and level."
    if not keyword_ok:
        return "INVALID", "Title does not match required keywords."
    return "INVALID", "Title does not match required job level."
