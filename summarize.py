#!/usr/bin/env python3
"""
Benchmark Summary and Analysis Script
Reads results/<strategy>.jsonl files and generates:
1. summary.csv with the 6 core metrics per strategy
2. Breakdown tables by pipeline length (Markdown and LaTeX formatted)
3. Bar charts comparing exact accuracy per strategy across pipeline lengths
"""

import os
import sys
import json
import pandas as pd
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

RESULTS_DIR = "results"
FIGURES_DIR = "figures"


def load_results():
    """Loads all jsonl results from results/ directory."""
    if not os.path.exists(RESULTS_DIR):
        print(f"[ERROR] '{RESULTS_DIR}' directory does not exist. Run benchmark first.")
        sys.exit(1)

    all_records = []
    for fname in os.listdir(RESULTS_DIR):
        if fname.endswith(".jsonl"):
            strategy_name = fname.replace(".jsonl", "")
            fpath = os.path.join(RESULTS_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            record = json.loads(line)
                            record["strategy"] = strategy_name
                            all_records.append(record)
                        except Exception:
                            pass

    if not all_records:
        print("[ERROR] No valid result records found in results/*.jsonl.")
        sys.exit(1)

    return all_records


def compute_metrics(records):
    """Computes headline metrics and length breakdown per strategy."""
    df = pd.DataFrame(records)

    # Flatten nested fields
    df["ap_correct"] = df["autopipeline"].apply(lambda x: x.get("is_correct", False))
    df["ap_acc"] = df["autopipeline"].apply(lambda x: x.get("accuracy", 0.0))
    df["hm_correct"] = df["hard_match"].apply(lambda x: x.get("is_correct", False))
    df["hm_acc"] = df["hard_match"].apply(lambda x: x.get("accuracy", 0.0))
    df["exec_success"] = df["execution"].apply(lambda x: x.get("success", False))
    df["prompt_tokens"] = df["usage"].apply(lambda x: x.get("prompt_tokens", 0))
    df["completion_tokens"] = df["usage"].apply(lambda x: x.get("completion_tokens", 0))
    df["total_tokens"] = df["usage"].apply(lambda x: x.get("total_tokens", 0))

    strategies = df["strategy"].unique()
    summary_rows = []

    for strat in strategies:
        strat_df = df[df["strategy"] == strat]
        n_cases = len(strat_df)
        
        ap_exact = strat_df["ap_correct"].mean() * 100.0
        hm_exact = strat_df["hm_correct"].mean() * 100.0
        hm_mean_partial = strat_df["hm_acc"].mean() * 100.0
        exec_rate = strat_df["exec_success"].mean() * 100.0
        total_prompt_tok = strat_df["prompt_tokens"].sum()
        total_compl_tok = strat_df["completion_tokens"].sum()
        total_tok = strat_df["total_tokens"].sum()
        total_time = strat_df["latency"].sum()

        summary_rows.append({
            "Strategy": strat,
            "Cases": n_cases,
            "Autopipeline Exact Match (%)": round(ap_exact, 2),
            "Hard Match Exact Match (%)": round(hm_exact, 2),
            "Hard Match Mean Partial (%)": round(hm_mean_partial, 2),
            "Execution Rate (%)": round(exec_rate, 2),
            "Prompt Tokens": int(total_prompt_tok),
            "Completion Tokens": int(total_compl_tok),
            "Total Tokens": int(total_tok),
            "Total Time (s)": round(total_time, 2),
        })

    summary_df = pd.DataFrame(summary_rows)

    # Length breakdown
    length_rows = []
    lengths = sorted(df["pipeline_length"].unique())
    for length in lengths:
        for strat in strategies:
            sub = df[(df["pipeline_length"] == length) & (df["strategy"] == strat)]
            if len(sub) > 0:
                length_rows.append({
                    "Pipeline Length": f"length{length}",
                    "Strategy": strat,
                    "Count": len(sub),
                    "Autopipeline Exact (%)": round(sub["ap_correct"].mean() * 100.0, 2),
                    "Hard Match Mean Partial (%)": round(sub["hm_acc"].mean() * 100.0, 2),
                })
    length_df = pd.DataFrame(length_rows)

    return summary_df, length_df, df


def generate_plot(length_df, summary_df):
    """Generates bar chart of exact-match accuracy per strategy by pipeline length."""
    if not HAS_MATPLOTLIB:
        print("[NOTICE] matplotlib not available, skipping plot generation.")
        return

    os.makedirs(FIGURES_DIR, exist_ok=True)
    plot_path = os.path.join(FIGURES_DIR, "accuracy_by_length.png")

    # Pivot length_df for plotting
    pivot_df = length_df.pivot(index="Pipeline Length", columns="Strategy", values="Autopipeline Exact (%)")
    
    # Sort index naturally
    def sort_len(idx_str):
        val = idx_str.replace("length", "")
        return int(val) if val.isdigit() else 999

    pivot_df = pivot_df.reindex(sorted(pivot_df.index, key=sort_len))

    plt.figure(figsize=(12, 6))
    ax = pivot_df.plot(kind="bar", width=0.8, figsize=(12, 6), edgecolor="black")
    plt.title("Exact-Match Accuracy (autopipeline) by Pipeline Length", fontsize=14, fontweight="bold")
    plt.xlabel("Pipeline Length (Complexity)", fontsize=12)
    plt.ylabel("Exact-Match Accuracy (%)", fontsize=12)
    plt.ylim(0, 105)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend(title="Prompting Strategy", fontsize=10)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"[OK] Bar chart saved to {plot_path}")


def main():
    records = load_results()
    summary_df, length_df, raw_df = compute_metrics(records)

    # 1. Save summary.csv
    summary_csv_path = "summary.csv"
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"\n[OK] Wrote overall metrics to {summary_csv_path}")

    # 2. Print Markdown Main Table
    print("\n" + "=" * 80)
    print("TABLE 1: Overall Benchmark Performance Across Prompting Strategies")
    print("=" * 80)
    try:
        print(summary_df.to_markdown(index=False))
    except Exception:
        print(summary_df.to_string(index=False))

    # 3. Print Length Breakdown Table
    print("\n" + "=" * 80)
    print("TABLE 2: Breakdown by Pipeline Length (Autopipeline Exact Match %)")
    print("=" * 80)
    try:
        pivot_table = length_df.pivot(index="Pipeline Length", columns="Strategy", values="Autopipeline Exact (%)")
        print(pivot_table.to_markdown())
    except Exception:
        print(length_df.to_string(index=False))

    # 4. Save LaTeX table for report
    latex_table_path = os.path.join(RESULTS_DIR, "table_summary.tex")
    with open(latex_table_path, "w") as f:
        f.write(summary_df.to_latex(index=False))
    print(f"[OK] Saved LaTeX table to {latex_table_path}")

    # 5. Generate plot
    generate_plot(length_df, summary_df)


if __name__ == "__main__":
    main()
