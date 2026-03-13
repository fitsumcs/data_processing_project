from utils.req_parser import ParsedReq
from validators.title_validator import validate_title_against_req


def test_title_validator_valid_when_keyword_and_level_match():
    parsed = ParsedReq(
        raw="",
        keywords=["security", "operations"],
        job_level="Director +",
    )
    result, _ = validate_title_against_req("Director of Security Operations", parsed)
    assert result == "VALID"


def test_title_validator_invalid_when_level_missing():
    parsed = ParsedReq(
        raw="",
        keywords=["security"],
        job_level="Director +",
    )
    result, comment = validate_title_against_req("Security Specialist", parsed)
    assert result == "INVALID"
    assert "job level" in comment


def test_title_validator_invalid_when_keyword_missing():
    parsed = ParsedReq(
        raw="",
        keywords=["procurement"],
        job_level="Manager +",
    )
    result, comment = validate_title_against_req("Director of Engineering", parsed)
    assert result == "INVALID"
    assert "keywords" in comment
