from dataclasses import dataclass, field
from typing import Dict, List

from utils.text_utils import normalize_text, split_keywords, strip_html


@dataclass
class ParsedReq:
    raw: str
    fields: Dict[str, str] = field(default_factory=dict)
    geo_allowed: List[str] = field(default_factory=list)
    geo_excluded: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    job_level: str = ""
    company_size: str = ""
    industry: str = ""
    comments: str = ""


def _parse_geo(geo_text: str) -> tuple[List[str], List[str]]:
    geo = normalize_text(geo_text).lower()
    if not geo:
        return [], []

    excluded: List[str] = []
    allowed = geo

    if "exclude" in geo:
        left, right = geo.split("exclude", 1)
        allowed = left
        excluded = split_keywords(right.replace("(", " ").replace(")", " "))

    # split on common separators while preserving short location tokens
    allowed = (
        allowed.replace("(", " ")
        .replace(")", " ")
        .replace(" only", " ")
        .replace(" and ", ",")
        .replace("&", ",")
        .replace(" - ", ",")
        .replace(":", ",")
    )
    allowed_tokens = split_keywords(allowed)
    return allowed_tokens, excluded


def parse_req(req_value: object) -> ParsedReq:
    raw = normalize_text(req_value)
    parsed = ParsedReq(raw=raw)
    if not raw:
        return parsed

    for segment in [s.strip() for s in raw.split("|") if s.strip()]:
        if ":" not in segment:
            continue
        key, value = segment.split(":", 1)
        key_norm = key.strip().lower().replace(" ", "_")
        parsed.fields[key_norm] = value.strip()

    parsed.job_level = normalize_text(parsed.fields.get("job_level", ""))
    parsed.company_size = normalize_text(parsed.fields.get("company_size", ""))
    parsed.industry = normalize_text(parsed.fields.get("industry", ""))
    parsed.comments = strip_html(parsed.fields.get("comments", ""))

    keywords_value = parsed.fields.get("keywords", "")
    if normalize_text(keywords_value).lower() == "see comment":
        parsed.keywords = split_keywords(parsed.comments)
    else:
        parsed.keywords = split_keywords(keywords_value)

    geo_allowed, geo_excluded = _parse_geo(parsed.fields.get("geo", ""))
    parsed.geo_allowed = geo_allowed
    parsed.geo_excluded = geo_excluded

    return parsed
