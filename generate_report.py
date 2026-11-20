#!/usr/bin/env python3
"""
Report Generator
Reads summary.csv and results/*.jsonl, injects actual evaluation numbers and tables
into report_template.md, and writes out the final report document.
"""

import os
import sys
import pandas as pd

TEMPLATE_PATH = "report_template.md"
OUTPUT_REPORT = "FINAL_REPORT.md"
SUMMARY_CSV = "summary.csv"


def generate_report():
    if not os.path.exists(TEMPLATE_PATH):
        print(f"[ERROR] Template '{TEMPLATE_PATH}' not found.")
        sys.exit(1)

    if not os.path.exists(SUMMARY_CSV):
        print(f"[ERROR] '{SUMMARY_CSV}' not found. Run summarize.py first.")
        sys.exit(1)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    summary_df = pd.read_csv(SUMMARY_CSV)
    try:
        summary_md = summary_df.to_markdown(index=False)
    except Exception:
        summary_md = summary_df.to_string(index=False)

    content = content.replace("<!-- INSERT_SUMMARY_TABLE_HERE -->", summary_md)

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[SUCCESS] Final report written to '{OUTPUT_REPORT}'.")
    print(f"You can convert '{OUTPUT_REPORT}' to PDF using your preferred markdown-to-pdf tool, VS Code Markdown PDF extension, or pandoc.")


if __name__ == "__main__":
    generate_report()
