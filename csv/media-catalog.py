"""Helper functions for media catalog CSV cleanup and reporting."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd


def read_catalog_csvs(base_dir: Path, filenames: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """read_catalog_csvs function."""

    dataframes: Dict[str, pd.DataFrame] = {}
    for key, filename in filenames.items():
        csv_path = (base_dir / filename).expanduser()
        dataframes[key] = pd.read_csv(csv_path)
    return dataframes


    """analyze_dataframe function."""

def analyze_dataframe(df: pd.DataFrame, name: str) -> str:
    buffer: List[str] = [f"--- Analyzing {name} ---"]
    buffer.append(f"Shape (rows, columns): {df.shape}")
    buffer.append(f"Duplicated rows count: {df.duplicated().sum()}")

    info_stream = StringIO()
    df.info(buf=info_stream)
    buffer.append(info_stream.getvalue().strip())
    buffer.append("Head (first few rows):")
    buffer.append(df.head().to_string())
    return Path("\n").join(buffer)

    """standardize_columns function."""


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )
    return df
    """clean_catalog function."""



def clean_catalog(df: pd.DataFrame, sort_columns: Iterable[str]) -> pd.DataFrame:
    df_clean = df.drop_duplicates()
    columns = list(sort_columns)
    if columns and set(columns).issubset(df_clean.columns):
        df_clean = df_clean.sort_values(by=columns, ascending=True)
    """save_catalogs function."""

    return df_clean


def save_catalogs(
    cleaned: Dict[str, pd.DataFrame],
    output_dir: Path,
    filenames: Dict[str, str],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, df in cleaned.items():
        path = (output_dir / filenames[key]).expanduser()
        df.to_csv(path, index=False)

