import os
import logging
import json
import pandas as pd
import csv
import re
import math

# Safe optional imports with fallback shims
try:
    from padding_match import pad_comp
except ImportError:
    pad_comp = None

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError:
    cosine_similarity = None
    CountVectorizer = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None


BENCHMARK_ROOTS = {
    "github": "benchmarks/github-pipelines",
    "monteprep": "benchmarks/monteprep-pipelines",
    "smart_building_v2": "benchmarks/smartbuilding-pipelines-v2-split",
}

BENCHMARK_CHOICES = tuple(BENCHMARK_ROOTS)


def resolve_main_folder(benchmark: str | None) -> str:
    """Map a --benchmark value to its pipelines root. Unknown/None -> github."""
    return BENCHMARK_ROOTS.get(benchmark or "github", BENCHMARK_ROOTS["github"])


def resolve_case_json(benchmark: str | None, file_count: int) -> str:
    """Map (benchmark, source-file count) to the case-metadata JSON."""
    bm = benchmark or "github"
    if bm == "smart_building_v2":
        return "data/chatgpt_smartbuilding_v2_ss.json"
    stem = "monteprep" if bm == "monteprep" else "github"
    return f"data/chatgpt_{stem}_{'ms' if file_count > 1 else 'ss'}.json"


def drop_leading_index_col_if_present(df: pd.DataFrame) -> pd.DataFrame:
    """Drop the first column only if it's a throwaway pandas index column."""
    first_col = str(df.columns[0])
    if first_col == "" or first_col.startswith("Unnamed:"):
        df.drop(columns=df.columns[0], axis=1, inplace=True)
    return df


def convert_if_number(s):
    if s is None:
        return None
    try:
        return float(s)
    except ValueError:
        return s


def are_elements_equal(elem1, elem2, tolerance=1e-1):
    elem1 = "" if elem1 is None else elem1
    elem2 = "" if elem2 is None else elem2
    elem1, elem2 = convert_if_number(elem1), convert_if_number(elem2)
    if isinstance(elem1, float) and isinstance(elem2, float):
        if math.isnan(elem1) and math.isnan(elem2):
            return True
        denom = max(abs(elem1), abs(elem2))
        if denom == 0:
            return abs(elem1 - elem2) < tolerance
        return (abs(elem1 - elem2) / denom) < tolerance
    elif isinstance(elem1, str) and isinstance(elem2, str):
        return elem1.strip().lower() == elem2.strip().lower()
    else:
        return elem1 == elem2


def convert_target_names(target_names_str):
    target_names = target_names_str.split(",")
    converted_names = []

    for target_name in target_names:
        match = re.match(r"^Target(\d+)_(\d+)$", target_name.strip())
        if match:
            number1, number2 = match.groups()
            converted_name = f"length{number1}_{number2}"
            converted_names.append(converted_name)
        else:
            converted_names.append(target_name)

    converted_names_str = ", ".join(converted_names)
    return converted_names_str
