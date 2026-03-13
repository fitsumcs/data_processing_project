# Lead Data Validation Project

Python project for validating lead rows from `DataCheck_DemoCode.xlsx` using `sub status`-driven rules and `req` comparison logic.

## Tech Stack

- Python 3.10+
- Pandas
- OpenPyXL (Excel engine)

## Project Structure

```text
data-processing/
├── main.py
├── validators/
│   ├── title_validator.py
│   ├── prooflink_validator.py
│   ├── status_validator.py
│   └── other_validators.py
├── utils/
│   ├── req_parser.py
│   ├── text_utils.py
│   └── io_utils.py
├── tests/
│   ├── test_status_validator.py
│   ├── test_prooflink_validator.py
│   ├── test_req_parser_and_geo.py
│   ├── test_title_validator.py
│   └── test_dispatcher.py
├── data/
│   ├── input/
│   │   └── DataCheck_DemoCode.xlsx
│   └── output/
├── requirements.txt
└── README.md
```

## How It Works

1. Load input sheet from `data/input`.
2. Parse each row's `req` into normalized sections (`Geo`, `Job_level`, `Keywords`, etc.).
3. Select validator by `sub status`.
4. Write row-level `Result` and `Comment`.
5. Export processed file as both XLSX and CSV to `data/output`.

## Implemented Rule Coverage

### `N/A: Title/PL Summary`
- Validate `title` against parsed requirement signals:
  - keyword matching (case-insensitive heuristic)
  - job-level matching (e.g., `Director +`, `Manager +`)
- Output:
  - `VALID` if checks pass
  - `INVALID` with short reason otherwise

### `N/A: Other (auto)` / `N/A: Other` / `N/A: Other (company)`
- Validate required core fields: `company`, `email`, `prooflink`.
- Basic email format check.

### `N/A: Prooflink`
- `VALID` if prooflink is:
  - `linkedin.com/in/`, or
  - `zoominfo.com/p/`, or
  - a site whose domain matches corporate email domain.
- Else `INVALID` with explanation.

### `N1: NWC`
- Status mapping:
  - empty or `valid` -> `VALID`
  - `a` or `!` -> `INVALID`
  - `r`, `no info`, `no company match` -> `RECHECK`
  - unknown status -> `INVALID`

### `N/A: Country/GEO`
- Parse Geo allowance and exclusions from `req`.
- Compare against `location`.
- Configurable strictness:
  - `normal` (default): pass with allowed location match unless excluded token is present.
  - `strict`: require stronger match when both broad and detailed location tokens exist.

### `N2: Out of Business/Bad data` (and company variant)
- Status-driven bad-data checks.
- Missing company or bad status flags lead to `INVALID`.

### Any Undefined Sub-status
- Output `INVALID` with `Comment = Rule undefined`.

## Run

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run validation:

```bash
python3 main.py --input data/input/DataCheck_DemoCode.xlsx --output-dir data/output --geo-mode normal
```

Strict Geo mode:

```bash
python3 main.py --input data/input/DataCheck_DemoCode.xlsx --output-dir data/output --geo-mode strict
```

Run unit tests:

```bash
pytest -q
```

## Test Evidence

- Command executed:

```bash
python3 -m pytest -q
```

- Result: `23 passed`
- Coverage focus:
  - Req parsing (`Geo`, `keywords`, `job_level`)
  - `N1: NWC` status mapping
  - Prooflink validation paths
  - Geo validation (`normal` and `strict`)
  - Title validator edge behavior
  - Dispatcher routing smoke checks

## Output Files

Generated in `data/output`:
- `DataCheck_DemoCode_processed.xlsx`
- `DataCheck_DemoCode_processed.csv`

Both files contain all original columns plus:
- `Result`
- `Comment`

## Notes and Assumptions

- Some requirement text is free-form and includes HTML, so title/keyword and geo checks are heuristic.
- If business logic is not explicitly defined for a sub-status, row is marked `INVALID` with `Rule undefined`.

## Quality Notes (Suggestions Only)

- `N/A: Title/PL Summary` can produce borderline false `INVALID` rows because requirement text is noisy and semi-structured.
- A future improvement pass can reduce this by adding stronger keyword normalization, synonym mapping, and phrase-level title matching.
- `N/A: Country/GEO` may mark valid metro-area strings as `INVALID` when only country names are listed in requirements.
- A future improvement can add city/metro-to-country reference mapping and alias normalization (for example abbreviations and local naming variants).
- These are optimization suggestions and are not required for the current baseline implementation.

## Country/GEO at 50k-70k Rows (Scalable Approach)

For larger volumes and noisy location text (region/county only):

1. Normalize location values using:
   - ISO country dictionary
   - alias tables (e.g., `UK` -> `United Kingdom`, `UAE` -> `United Arab Emirates`)
   - region/county mapping table to country.
2. Pre-compile `req` Geo rules once per unique requirement text and cache parsed patterns.
3. Use vectorized Pandas string ops for bulk matching where possible.
4. Process in chunks (e.g., 10k rows) for memory stability.
5. Optional multiprocessing by chunk for throughput.
6. Track QA metrics:
   - invalid rate by Geo rule
   - ambiguous-location rate
   - manual-review sample checks for precision/recall.

