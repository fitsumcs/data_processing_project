from validators.prooflink_validator import validate_prooflink


def test_validate_prooflink_linkedin_is_valid():
    result, comment = validate_prooflink(
        "https://www.linkedin.com/in/jane-doe-123",
        "jane@company.com",
    )
    assert result == "VALID"
    assert "LinkedIn" in comment


def test_validate_prooflink_zoominfo_is_valid():
    result, comment = validate_prooflink(
        "https://www.zoominfo.com/p/Jane-Doe/1234",
        "jane@company.com",
    )
    assert result == "VALID"
    assert "ZoomInfo" in comment


def test_validate_prooflink_domain_match_is_valid():
    result, comment = validate_prooflink(
        "https://careers.company.com/team/jane",
        "jane@company.com",
    )
    assert result == "VALID"
    assert "domain matches corporate email" in comment


def test_validate_prooflink_non_matching_domain_is_invalid():
    result, comment = validate_prooflink(
        "https://random-site.org/profile/jane",
        "jane@company.com",
    )
    assert result == "INVALID"
    assert "does not match email" in comment
