import argparse
from pathlib import Path
from typing import Dict, Tuple

from utils.io_utils import load_input_dataframe, write_outputs
from utils.req_parser import parse_req
from utils.text_utils import lower_clean, normalize_text
from validators.other_validators import (
    invalid_undefined_rule,
    validate_geo,
    validate_n2_out_of_business,
    validate_other_auto,
)
from validators.prooflink_validator import validate_prooflink
from validators.status_validator import validate_n1_nwc
from validators.title_validator import validate_title_against_req


def _build_column_map(columns) -> Dict[str, str]:
    return {lower_clean(c): c for c in columns}


def _get(row, cmap: Dict[str, str], name: str):
    key = cmap.get(name)
    if not key:
        return ""
    return row.get(key, "")


def _validate_row(row, cmap: Dict[str, str], geo_mode: str) -> Tuple[str, str]:
    sub_status = lower_clean(_get(row, cmap, "sub status"))
    status = _get(row, cmap, "status")
    req = _get(row, cmap, "req")
    title = _get(row, cmap, "title")
    prooflink = _get(row, cmap, "prooflink")
    email = _get(row, cmap, "email")
    company = _get(row, cmap, "company")
    location = _get(row, cmap, "location")

    parsed_req = parse_req(req)

    if sub_status == "n/a: title/pl summary":
        return validate_title_against_req(title, parsed_req)

    if sub_status == "n/a: prooflink":
        return validate_prooflink(prooflink, email)

    if sub_status in {"n/a: other (auto)", "n/a: other", "n/a: other (company)"}:
        return validate_other_auto(company, email, prooflink)

    if sub_status == "n1: nwc":
        return validate_n1_nwc(status)

    if sub_status == "n/a: country/geo":
        return validate_geo(location, parsed_req, geo_mode=geo_mode)

    if sub_status in {"n2: out of business/bad data", "n2: out of business/bad data (company)"}:
        return validate_n2_out_of_business(status, company)

    if not sub_status:
        return "INVALID", "Sub status is missing."

    return invalid_undefined_rule()


def run(input_path: str, output_dir: str, geo_mode: str) -> Tuple[str, str]:
    df = load_input_dataframe(input_path)
    cmap = _build_column_map(df.columns)

    results = []
    comments = []
    for _, row in df.iterrows():
        result, comment = _validate_row(row, cmap, geo_mode=geo_mode)
        results.append(result)
        comments.append(comment)

    # Overwrite/add result columns exactly as requested.
    df["Result"] = results
    df["Comment"] = comments

    base_name = Path(input_path).stem
    return write_outputs(df, output_dir, base_name)


def main():
    parser = argparse.ArgumentParser(description="Validate lead sheet rows against req/sub-status rules.")
    parser.add_argument(
        "--input",
        default="data/input/DataCheck_DemoCode.xlsx",
        help="Input XLSX path.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/output",
        help="Directory for processed XLSX/CSV.",
    )
    parser.add_argument(
        "--geo-mode",
        choices=["normal", "strict"],
        default="normal",
        help="Geo matching strictness.",
    )
    args = parser.parse_args()

    xlsx_path, csv_path = run(args.input, args.output_dir, args.geo_mode)
    print(f"Processed file written to: {normalize_text(xlsx_path)}")
    print(f"Processed file written to: {normalize_text(csv_path)}")


if __name__ == "__main__":
    main()
