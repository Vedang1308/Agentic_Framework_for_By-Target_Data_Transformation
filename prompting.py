"""
Shared Prompting and Metadata Extraction Module
Handles sample data substitution, schema inspection, datetime detection,
prompt assembly for zero-shot and few-shot CoT, and robust Python code extraction.
"""

import os
import re
import ast
import pandas as pd
import numpy as np
from demos.demonstrations import format_demonstrations_text

SYSTEM_PROMPT = """You are an expert Python and pandas data engineer specializing in Table-to-Table (TbT) transformation synthesis.
Given a source table schema with sample rows and a desired target table schema with sample rows, your task is to synthesize a general Python function that transforms the source DataFrame into the target DataFrame.

Strict Requirements:
1. Provide a clear, visible step-by-step reasoning plan (Chain of Thought) explaining the sequence of operators required (e.g., column selection, date/timestamp parsing and formatting, renaming, reshaping, aggregations, unit conversions, missing value handling).
2. Follow the reasoning plan with a single ```python ... ``` code block defining:
   import pandas as pd

   def transform(source: pd.DataFrame) -> pd.DataFrame:
       \"\"\"Return a DataFrame with the same schema and contents as target.csv.\"\"\"
       ...
3. The function must compute its result SOLELY from the `source` argument. It must NOT open or read target.csv, test_0.csv, training_0.csv, or any file from disk.
4. Do NOT hardcode target rows or literal values from the sample. The transformation must generalize to any unseen test table having the same source schema.
5. The returned DataFrame MUST have column names matching the target table VERBATIM (exact case, whitespace, and punctuation). Always conclude with:
   return df[target_columns]
6. The code must be deterministic, self-contained, and use only standard libraries (pandas, numpy, math, datetime). No network calls or exec calls.
"""


def detect_date_format(series: pd.Series) -> str | None:
    """Attempt to detect common date/datetime format string from sample series."""
    sample_values = [str(x).strip() for x in series.dropna().head(10) if str(x).strip() != ""]
    if not sample_values:
        return None

    # Candidate date formats common in building energy datasets
    candidates = [
        ("%a %m/%d/%Y", r"^[A-Za-z]{3}\s+\d{1,2}/\d{1,2}/\d{4}$"),
        ("%m/%d/%Y", r"^\d{1,2}/\d{1,2}/\d{4}$"),
        ("%Y-%m-%d %H:%M:%S", r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$"),
        ("%Y-%m-%d", r"^\d{4}-\d{2}-\d{2}$"),
        ("%m/%d/%Y %H:%M", r"^\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}$"),
        ("%m/%d/%Y %H:%M:%S", r"^\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}:\d{2}$"),
        ("%d/%m/%Y", r"^\d{2}/\d{2}/\d{4}$"),
    ]

    for fmt, pattern in candidates:
        if all(re.match(pattern, val) for val in sample_values):
            return fmt
    return None


def df_to_markdown_simple(df: pd.DataFrame) -> str:
    """Format DataFrame as a Markdown table without hard dependency on tabulate."""
    try:
        return df.to_markdown(index=False)
    except (ImportError, ModuleNotFoundError):
        headers = [str(c) for c in df.columns]
        rows = [[str(val) for val in row] for row in df.values]
        col_widths = [max(len(h), max((len(r[i]) for r in rows), default=0)) for i, h in enumerate(headers)]
        header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
        sep_line = "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |"
        row_lines = ["| " + " | ".join(r[i].ljust(col_widths[i]) for i in range(len(headers))) + " |" for r in rows]
        return "\n".join([header_line, sep_line] + row_lines)


def extract_case_metadata(case_dir: str, sample_rows: int = 8) -> dict:
    """
    Extract schema, dtypes, summary statistics, row counts, and representative
    sample rows from training_0.csv and target.csv (Sample Data Substitution).
    """
    train_path = os.path.join(case_dir, "training_0.csv")
    target_path = os.path.join(case_dir, "target.csv")

    if not os.path.exists(train_path) or not os.path.exists(target_path):
        raise FileNotFoundError(f"Missing training_0.csv or target.csv in {case_dir}")

    # Read data
    src_df = pd.read_csv(train_path)
    tgt_df = pd.read_csv(target_path)

    # Detect timestamps in source and target
    src_date_cols = {}
    for col in src_df.columns:
        if src_df[col].dtype == object or "date" in col.lower() or "cst" in col.lower() or "time" in col.lower():
            fmt = detect_date_format(src_df[col])
            if fmt:
                src_date_cols[col] = (fmt, src_df[col].dropna().iloc[0] if len(src_df[col].dropna()) > 0 else "")

    tgt_date_cols = {}
    for col in tgt_df.columns:
        if tgt_df[col].dtype == object or "date" in col.lower() or "cst" in col.lower() or "time" in col.lower():
            fmt = detect_date_format(tgt_df[col])
            if fmt:
                tgt_date_cols[col] = (fmt, tgt_df[col].dropna().iloc[0] if len(tgt_df[col].dropna()) > 0 else "")

    # Low-cardinality distinct values in source
    low_card_info = {}
    for col in src_df.columns:
        if src_df[col].nunique() <= 10:
            low_card_info[col] = list(src_df[col].dropna().unique())

    # Build representative samples (head + tail to span boundaries)
    n_head = min(sample_rows // 2, len(src_df))
    n_tail = min(sample_rows - n_head, max(0, len(src_df) - n_head))
    
    if len(src_df) <= sample_rows:
        src_sample = src_df.copy()
    else:
        src_sample = pd.concat([src_df.head(n_head), src_df.tail(n_tail)])

    if len(tgt_df) <= sample_rows:
        tgt_sample = tgt_df.copy()
    else:
        tgt_sample = pd.concat([tgt_df.head(n_head), tgt_df.tail(n_tail)])

    return {
        "case_name": os.path.basename(os.path.normpath(case_dir)),
        "source_row_count": len(src_df),
        "target_row_count": len(tgt_df),
        "source_columns": list(src_df.columns),
        "target_columns": list(tgt_df.columns),
        "source_dtypes": {col: str(dtype) for col, dtype in src_df.dtypes.items()},
        "target_dtypes": {col: str(dtype) for col, dtype in tgt_df.dtypes.items()},
        "source_date_cols": src_date_cols,
        "target_date_cols": tgt_date_cols,
        "low_cardinality": low_card_info,
        "source_sample_markdown": df_to_markdown_simple(src_sample),
        "target_sample_markdown": df_to_markdown_simple(tgt_sample),
    }


def build_user_prompt(case_dir: str, include_few_shot: bool = False, num_demos: int = 3) -> str:
    """
    Constructs the standardized user prompt for the given benchmark case.
    Prompts remain identical across strategies apart from few-shot demonstration prefix.
    """
    meta = extract_case_metadata(case_dir)

    sections = []

    # Optional Few-Shot demonstrations section
    if include_few_shot:
        sections.append(format_demonstrations_text(num_demos))
        sections.append("=" * 60)
        sections.append("Now, synthesize the transformation function for the following case:\n")

    # Problem overview
    sections.append(f"### Benchmark Case: {meta['case_name']}")
    sections.append(f"- Source sample rows: {meta['source_row_count']} rows (Note: test_0.csv may have different row count)")
    sections.append(f"- Target rows: {meta['target_row_count']} rows")
    if meta['source_row_count'] != meta['target_row_count']:
        sections.append(f"- Notice: Row count changes from {meta['source_row_count']} to {meta['target_row_count']}. Check if an aggregation, grouping, or pivoting operation is required.")

    # Target column names verbatim
    target_cols_str = ", ".join([repr(c) for c in meta['target_columns']])
    sections.append(f"\n### Exact Target Columns (Must match verbatim):\n[{target_cols_str}]")

    # Datetime analysis hints
    date_hints = []
    if meta['source_date_cols']:
        for col, (fmt, sample) in meta['source_date_cols'].items():
            date_hints.append(f"Source column '{col}' has date format '{fmt}' (sample: '{sample}')")
    if meta['target_date_cols']:
        for col, (fmt, sample) in meta['target_date_cols'].items():
            date_hints.append(f"Target column '{col}' requires date format '{fmt}' (sample: '{sample}')")
    if date_hints:
        sections.append("\n### Datetime Format Inferences:")
        sections.extend([f"- {h}" for h in date_hints])

    # Schemas and Dtypes
    sections.append("\n### Source Schema and Types:")
    src_types = ", ".join([f"{col} ({dtype})" for col, dtype in meta['source_dtypes'].items()])
    sections.append(src_types)

    sections.append("\n### Target Schema and Types:")
    tgt_types = ", ".join([f"{col} ({dtype})" for col, dtype in meta['target_dtypes'].items()])
    sections.append(tgt_types)

    # Low-cardinality columns
    if meta['low_cardinality']:
        sections.append("\n### Distinct values for categorical / low-cardinality source columns:")
        for col, vals in meta['low_cardinality'].items():
            sections.append(f"- {col}: {vals}")

    # Sample rows
    sections.append("\n### Source Table Sample (training_0.csv):")
    sections.append(meta['source_sample_markdown'])

    sections.append("\n### Desired Target Table Sample (target.csv):")
    sections.append(meta['target_sample_markdown'])

    # Final instructions
    sections.append("\n### Instructions:")
    sections.append("1. Write a step-by-step reasoning plan (Chain of Thought) analyzing the transformation steps needed to transform the source table into the target table.")
    sections.append("2. Conclude with a single ```python ``` code block implementing `def transform(source: pd.DataFrame) -> pd.DataFrame:`.")
    sections.append("3. Make sure to return `df[target_columns]` with the target column names copied verbatim.")

    return "\n".join(sections)


def extract_python_code(completion_text: str) -> str:
    """
    Robust code extraction per Instructions Page 11:
    - Finds the LAST fenced ```python ... ``` block.
    - Validates syntax using ast.parse.
    - Raises ValueError on missing block or syntax error.
    """
    if not completion_text or not completion_text.strip():
        raise ValueError("Empty completion received. The model returned no text. Ensure reasoning_effort='none' or check token budget.")

    # Match all ```python ... ``` blocks (or bare ``` blocks if python tag omitted)
    pattern = r"```(?:python)?\s*([\s\S]*?)```"
    matches = re.findall(pattern, completion_text, re.IGNORECASE)

    if not matches:
        # Fallback: check if the completion is raw code
        if "def transform(" in completion_text:
            code = completion_text.strip()
        else:
            raise ValueError("No fenced ```python code block found in completion.")
    else:
        # Pick the last fenced block
        code = matches[-1].strip()

    # Validate that def transform( is defined
    if "def transform(" not in code:
        raise ValueError("Generated code does not define 'def transform(source: pd.DataFrame)'.")

    # Validate Python syntax
    try:
        ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in extracted code: {e}")

    return code
