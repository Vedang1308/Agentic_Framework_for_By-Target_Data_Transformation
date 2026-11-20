"""
Validator Entry Point
Implements validate_autopipeline_style as defined in Instructions.pdf Page 7.
Provides unified validation for both 'autopipeline' (official) and 'hard_match' (auxiliary).
"""

import pandas as pd
from validation.hard_match import compare_lists_matching, compare_tables_matching


def validate_autopipeline_style(sql_result_df: pd.DataFrame, target_df: pd.DataFrame, method: str = "hard_match"):
    """
    method:
    - "hard_match": compare_lists_matching — per-column partial credit, matches
      columns by NAME.
    - "autopipeline": compare_tables_matching — binary (all-or-nothing), matches
      columns by DATA CONTENT (robust to naming/casing).
    Returns (accuracy, is_correct, similarity_scores, matched_or_error_info).
    """
    if not isinstance(sql_result_df, pd.DataFrame):
        return 0.0, False, [], ["Error: returned object is not a pandas DataFrame"]
    if not isinstance(target_df, pd.DataFrame):
        return 0.0, False, [], ["Error: target object is not a pandas DataFrame"]

    # Make independent copies to avoid mutating input frames during matching
    pred_df = sql_result_df.copy()
    gold_df = target_df.copy()

    if method == "hard_match":
        target_cols_by_lower = {c.lower(): c for c in gold_df.columns}
        rename = {
            c: target_cols_by_lower[c.lower()]
            for c in pred_df.columns
            if c not in gold_df.columns and c.lower() in target_cols_by_lower
        }
        if rename:
            pred_df = pred_df.rename(columns=rename)
        return compare_lists_matching(pred_df, gold_df)
    elif method == "autopipeline":
        return compare_tables_matching(pred_df, gold_df)
    raise ValueError(f"Unknown validation method: {method!r}")
