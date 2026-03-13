from typing import Tuple

from utils.text_utils import lower_clean


def validate_n1_nwc(status_value: object) -> Tuple[str, str]:
    status = lower_clean(status_value)

    if status in {"", "valid"}:
        return "VALID", "N1 NWC status is empty/valid."
    if status in {"a", "!"}:
        return "INVALID", "N1 NWC status indicates retired or suspicious lead."
    if status in {"r", "no info", "no company match"}:
        return "RECHECK", "N1 NWC status requires manual recheck."

    return "INVALID", f"N1 NWC status '{status}' is not recognized."
