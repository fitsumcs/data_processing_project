import pytest

from validators.status_validator import validate_n1_nwc


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        ("", "VALID"),
        ("valid", "VALID"),
        ("a", "INVALID"),
        ("!", "INVALID"),
        ("r", "RECHECK"),
        ("no info", "RECHECK"),
        ("no company match", "RECHECK"),
        ("unknown", "INVALID"),
    ],
)
def test_validate_n1_nwc_mapping(status, expected):
    result, _ = validate_n1_nwc(status)
    assert result == expected
