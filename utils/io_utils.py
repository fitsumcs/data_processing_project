from pathlib import Path
from typing import Tuple

import pandas as pd


def load_input_dataframe(input_path: str) -> pd.DataFrame:
    return pd.read_excel(input_path)


def write_outputs(df: pd.DataFrame, output_dir: str, base_name: str) -> Tuple[str, str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    xlsx_path = output_path / f"{base_name}_processed.xlsx"
    csv_path = output_path / f"{base_name}_processed.csv"

    df.to_excel(xlsx_path, index=False)
    df.to_csv(csv_path, index=False)
    return str(xlsx_path), str(csv_path)
