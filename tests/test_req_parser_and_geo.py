from utils.req_parser import parse_req
from validators.other_validators import validate_geo


def test_parse_req_extracts_geo_keywords_and_level():
    req = (
        "Geo: US, Canada (exclude Quebec) | "
        "Job_level: Director + | "
        "Keywords: security, risk"
    )
    parsed = parse_req(req)

    assert "us" in parsed.geo_allowed
    assert "canada" in parsed.geo_allowed
    assert "quebec" in parsed.geo_excluded
    assert parsed.job_level == "Director +"
    assert parsed.keywords == ["security", "risk"]


def test_validate_geo_normal_mode_passes_country_match():
    parsed = parse_req("Geo: France, Germany")
    result, _ = validate_geo("Paris, France", parsed, geo_mode="normal")
    assert result == "VALID"


def test_validate_geo_strict_mode_rejects_weak_match():
    parsed = parse_req("Geo: India only - Mumbai, Hyderabad")
    result, comment = validate_geo("India", parsed, geo_mode="strict")
    assert result == "INVALID"
    assert "Strict Geo mode" in comment


def test_validate_geo_fails_on_excluded_location():
    parsed = parse_req("Geo: US, Canada (exclude Quebec)")
    result, comment = validate_geo("Montreal, Quebec, Canada", parsed, geo_mode="normal")
    assert result == "INVALID"
    assert "excluded area" in comment
