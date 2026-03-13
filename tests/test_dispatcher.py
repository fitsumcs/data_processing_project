import pandas as pd

from main import _build_column_map, _validate_row


def _row(**kwargs):
    defaults = {
        "sub status": "",
        "status": "",
        "req": "",
        "title": "",
        "prooflink": "",
        "email": "",
        "company": "",
        "location": "",
    }
    defaults.update(kwargs)
    return pd.Series(defaults)


def _cmap():
    return _build_column_map(
        ["sub status", "status", "req", "title", "prooflink", "email", "company", "location"]
    )


def test_dispatcher_routes_n1_to_recheck():
    result, _ = _validate_row(_row(**{"sub status": "N1: NWC", "status": "no info"}), _cmap(), "normal")
    assert result == "RECHECK"


def test_dispatcher_routes_prooflink_rule():
    result, _ = _validate_row(
        _row(
            **{
                "sub status": "N/A: Prooflink",
                "prooflink": "https://www.linkedin.com/in/test-user",
                "email": "test@company.com",
            }
        ),
        _cmap(),
        "normal",
    )
    assert result == "VALID"


def test_dispatcher_handles_unknown_sub_status():
    result, comment = _validate_row(_row(**{"sub status": "N9: Unknown"}), _cmap(), "normal")
    assert result == "INVALID"
    assert comment == "Rule undefined"


def test_dispatcher_handles_missing_sub_status():
    result, comment = _validate_row(_row(**{"sub status": ""}), _cmap(), "normal")
    assert result == "INVALID"
    assert comment == "Sub status is missing."
