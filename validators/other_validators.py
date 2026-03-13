from typing import Tuple

from utils.req_parser import ParsedReq
from utils.text_utils import lower_clean


def validate_geo(location_value: object, parsed_req: ParsedReq, geo_mode: str = "normal") -> Tuple[str, str]:
    location = lower_clean(location_value)
    if parsed_req.geo_allowed and not location:
        return "INVALID", "Location is missing while Geo requirement exists."

    if not parsed_req.geo_allowed and not parsed_req.geo_excluded:
        return "INVALID", "Rule undefined"

    for excluded in parsed_req.geo_excluded:
        if excluded and excluded in location:
            return "INVALID", f"Location contains excluded area '{excluded}'."

    if not parsed_req.geo_allowed:
        return "VALID", "Location passed exclusion-based Geo rule."

    matched_allowed = [a for a in parsed_req.geo_allowed if a and a in location]
    if not matched_allowed:
        return "INVALID", "Location does not match allowed Geo requirements."

    if geo_mode == "strict":
        geo_raw = lower_clean(parsed_req.fields.get("geo", ""))
        has_detailed_hint = " only" in geo_raw or "-" in geo_raw
        if has_detailed_hint:
            matched_count = sum(1 for t in parsed_req.geo_allowed if t and t in location)
            if matched_count < 2:
                return "INVALID", "Strict Geo mode requires both country and city/region match."

    return "VALID", "Location matches Geo requirements."


def validate_other_auto(company: object, email: object, prooflink: object) -> Tuple[str, str]:
    company_text = lower_clean(company)
    email_text = lower_clean(email)
    prooflink_text = lower_clean(prooflink)

    missing = []
    if not company_text:
        missing.append("company")
    if not email_text:
        missing.append("email")
    if not prooflink_text:
        missing.append("prooflink")

    if missing:
        return "INVALID", f"Missing required fields: {', '.join(missing)}."

    if "@" not in email_text:
        return "INVALID", "Email format is invalid."

    return "VALID", "Company and lead core fields are present."


def validate_n2_out_of_business(status: object, company: object) -> Tuple[str, str]:
    status_text = lower_clean(status)
    company_text = lower_clean(company)
    if not company_text:
        return "INVALID", "Company is missing for N2 company validation."

    if status_text in {"out of business", "bad data", "a", "no company data"}:
        return "INVALID", "N2 status indicates out of business or bad data."

    if not status_text:
        return "INVALID", "N2 requires explicit bad-data status but status is empty."

    return "VALID", "N2 row does not indicate out-of-business/bad-data flags."


def invalid_undefined_rule() -> Tuple[str, str]:
    return "INVALID", "Rule undefined"
