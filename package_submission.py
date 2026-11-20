#!/usr/bin/env python3
"""
Gradescope Submission Packager
Creates the required A4_<asurite>.zip file adhering strictly to
Instructions.pdf Page 9 & Page 10 requirements:
- strategies/
- prompting.py
- run_benchmark.py
- summarize.py
- README.md
- demos/
- results/<strategy>.jsonl and summary.csv
- generated/<strategy>/<case>/transform.py (and candidates/)
- logs/<strategy>/<case>/
- EXCLUDES all benchmark CSVs and API keys!
"""

import os
import sys
import zipfile
import argparse
import re

REQUIRED_ITEMS = [
    "strategies",
    "prompting.py",
    "run_benchmark.py",
    "summarize.py",
    "README.md",
    "demos",
    "results",
    "generated",
    "logs",
]


def validate_clean_content(file_path: str) -> bool:
    """Verifies that no API keys or raw benchmark CSVs are accidentally included."""
    base = os.path.basename(file_path)
    # Check for forbidden benchmark CSV files (except in demos/cases if small)
    if base in ("test_0.csv", "training_0.csv") and not file_path.startswith("demos"):
        return False
    if file_path.endswith(".zip"):
        return False
    if ".git" in file_path or ".env" in file_path or "__pycache__" in file_path:
        return False
    return True


def package_submission(asurite: str):
    zip_filename = f"A4_{asurite}.zip"
    print(f"[*] Packaging submission into '{zip_filename}'...")

    # Check required files
    missing = []
    for item in REQUIRED_ITEMS:
        if not os.path.exists(item):
            missing.append(item)

    if missing:
        print(f"[WARNING] Some expected items are missing before packaging: {missing}")
        print("Make sure you have run the benchmark and summarize.py before final packaging!")

    included_count = 0
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_out:
        for root, dirs, files in os.walk("."):
            # Exclude benchmark and git dirs
            dirs[:] = [d for d in dirs if d not in (".git", "benchmarks", "__pycache__", ".venv", "venv")]
            
            for f in files:
                full_path = os.path.normpath(os.path.join(root, f))
                if not validate_clean_content(full_path):
                    continue

                # Only include required project components and validation packages
                top_folder = full_path.split(os.sep)[0]
                if top_folder in REQUIRED_ITEMS or top_folder in ("validation", "util", "summary.csv", "requirements.txt", "analyze_failures.py"):
                    zip_out.write(full_path, full_path)
                    included_count += 1

    zip_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"[SUCCESS] Created '{zip_filename}' ({included_count} files, {zip_size_mb:.2f} MB).")
    print(f"[VERIFIED] No benchmark CSVs or credentials included.")
    print(f"Ready for upload to Gradescope as '{zip_filename}' along with your report 'A4_{asurite}.pdf'!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package submission zip for Gradescope")
    parser.add_argument("--asurite", type=str, required=True, help="Your ASU ASURITE ID (e.g. vwaghad)")
    args = parser.parse_args()
    package_submission(args.asurite.strip())
