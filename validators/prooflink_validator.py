from typing import Tuple

from utils.text_utils import extract_domain, lower_clean, normalize_text


def validate_prooflink(prooflink: object, email: object) -> Tuple[str, str]:
    pl = lower_clean(prooflink)
    if not pl:
        return "INVALID", "Prooflink is missing."

    if "linkedin.com/in/" in pl:
        return "VALID", "Valid LinkedIn profile prooflink."
    if "zoominfo.com/p/" in pl:
        return "VALID", "Valid ZoomInfo profile prooflink."

    pl_domain = extract_domain(prooflink)
    email_domain = extract_domain(email)
    if pl_domain and email_domain and (
        pl_domain == email_domain
        or pl_domain.endswith("." + email_domain)
        or email_domain.endswith("." + pl_domain)
    ):
        return "VALID", "Prooflink domain matches corporate email domain."

    prooflink_text = normalize_text(prooflink)
    return (
        "INVALID",
        f"Prooflink '{prooflink_text}' is not LinkedIn/ZoomInfo and domain does not match email.",
    )
