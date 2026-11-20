#!/usr/bin/env python3
"""
Failure Analysis Script for By-Target Data Transformation
Parses results/<strategy>.jsonl files to diagnose failure modes as required
for Section 4 of the report (Instructions.pdf Page 9).
Identifies 3-5 concrete failure modes with code excerpts and validator feedback.
"""

import os
import sys
import json
import pandas as pd

RESULTS_DIR = "results"


def analyze_failures():
    if not os.path.exists(RESULTS_DIR):
        print(f"[ERROR] Directory '{RESULTS_DIR}' does not exist.")
        sys.exit(1)

    records = []
    for fname in os.listdir(RESULTS_DIR):
        if fname.endswith(".jsonl"):
            strat = fname.replace(".jsonl", "")
            with open(os.path.join(RESULTS_DIR, fname), "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            rec = json.loads(line)
                            rec["strategy"] = strat
                            records.append(rec)
                        except Exception:
                            pass

    if not records:
        print("[ERROR] No result records found.")
        sys.exit(1)

    df = pd.DataFrame(records)
    df["ap_correct"] = df["autopipeline"].apply(lambda x: x.get("is_correct", False))
    df["hm_correct"] = df["hard_match"].apply(lambda x: x.get("is_correct", False))
    df["exec_success"] = df["execution"].apply(lambda x: x.get("success", False))

    print("\n========================================================")
    print("FAILURE MODE DIAGNOSIS & CONCRETE EXAMPLES")
    print("========================================================")

    # Mode 1: Execution Crashes or Timeouts
    crashes = df[~df["exec_success"]]
    print(f"\n[FAILURE MODE 1] Execution Crashes / Timeouts ({len(crashes)} occurrences)")
    if len(crashes) > 0:
        sample = crashes.iloc[0]
        print(f"Example Case: {sample['case']} (Strategy: {sample['strategy']}, Length: {sample['pipeline_length']})")
        print(f"Error Message: {sample['execution'].get('error')}")
        code_p = sample.get("code_path")
        if code_p and os.path.exists(code_p):
            with open(code_p) as f:
                print(f"Code Excerpt:\n{f.read()[:300]}...\n")

    # Mode 2: Column Naming Discrepancies (AP True, HM False)
    naming_gap = df[df["ap_correct"] & ~df["hm_correct"]]
    print(f"\n[FAILURE MODE 2] Column Naming & Schema Casing Discrepancies ({len(naming_gap)} occurrences)")
    print("Content matches correctly under AutoPipeline multiset matcher, but Hard Match fails on column names.")
    if len(naming_gap) > 0:
        sample = naming_gap.iloc[0]
        print(f"Example Case: {sample['case']} (Strategy: {sample['strategy']}, Length: {sample['pipeline_length']})")
        print(f"Hard Match Diagnostic: {sample['hard_match'].get('matched_cols')}")
        code_p = sample.get("code_path")
        if code_p and os.path.exists(code_p):
            with open(code_p) as f:
                print(f"Code Excerpt:\n{f.read()[:300]}...\n")

    # Mode 3: Semantic Content Mismatch (AP False, Exec True)
    content_fail = df[df["exec_success"] & ~df["ap_correct"]]
    print(f"\n[FAILURE MODE 3] Semantic / Value Transformation Errors ({len(content_fail)} occurrences)")
    print("Code ran to completion, but output values or row count did not match target.")
    if len(content_fail) > 0:
        sample = content_fail.iloc[0]
        print(f"Example Case: {sample['case']} (Strategy: {sample['strategy']}, Length: {sample['pipeline_length']})")
        print(f"AutoPipeline Diagnostic: {sample['autopipeline'].get('matched_cols')}")
        code_p = sample.get("code_path")
        if code_p and os.path.exists(code_p):
            with open(code_p) as f:
                print(f"Code Excerpt:\n{f.read()[:300]}...\n")

    # Mode 4: Self-Consistency Impact
    print("\n[ANALYSIS] Impact of Self-Consistency Sampling")
    strat_perf = df.groupby("strategy")["ap_correct"].mean() * 100.0
    print(strat_perf.to_string())

    print("\n[DONE] Failure analysis complete. Use these excerpts for Section 4 of your report.")


if __name__ == "__main__":
    analyze_failures()
