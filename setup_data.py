#!/usr/bin/env python3
"""
Benchmark Dataset Setup Script
Downloads (if needed) and extracts the Smart Building TbT benchmark (105 cases)
to benchmarks/smartbuilding-pipelines-v2-split/ as required by Instructions.pdf.
"""

import os
import sys
import zipfile
import shutil

GDRIVE_FILE_ID = "1Jzx_ocgxIUiShyLOr6pzodXnKeEcSnII"
ZIP_NAME = "smartbuilding-pipelines-v2-split.zip"
TARGET_DIR = os.path.join("benchmarks", "smartbuilding-pipelines-v2-split")

def setup_benchmark():
    os.makedirs("benchmarks", exist_ok=True)
    
    # 1. Check if target directory already exists and is complete
    if os.path.exists(TARGET_DIR):
        case_folders = [d for d in os.listdir(TARGET_DIR) if os.path.isdir(os.path.join(TARGET_DIR, d)) and d.startswith("length")]
        if len(case_folders) >= 105:
            print(f"[OK] Benchmark already extracted to {TARGET_DIR} ({len(case_folders)} cases verified).")
            return

    # 2. Check if local zip exists
    if not os.path.exists(ZIP_NAME):
        print(f"[*] Benchmark archive '{ZIP_NAME}' not found locally.")
        print(f"[*] Downloading from Google Drive (ID: {GDRIVE_FILE_ID})...")
        try:
            import gdown
            url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
            gdown.download(url, ZIP_NAME, quiet=False)
        except Exception as e:
            print(f"[ERROR] Automatic download via gdown failed: {e}")
            print(f"Please manually download the zip from:")
            print(f"https://drive.google.com/file/d/{GDRIVE_FILE_ID}/view?pli=1")
            print(f"or scp '{ZIP_NAME}' to this directory and re-run this script.")
            sys.exit(1)

    # 3. Extract the zip file
    print(f"[*] Extracting '{ZIP_NAME}' to 'benchmarks/'...")
    with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall("benchmarks")

    # Clean up the zip file to reclaim 1 GB of disk space
    if os.path.exists(ZIP_NAME):
        print(f"[*] Removing temporary archive '{ZIP_NAME}' to reclaim disk space...")
        os.remove(ZIP_NAME)

    # In case the zip extracted directly to benchmarks/smartbuilding-pipelines-v2-split/
    if os.path.exists(TARGET_DIR):
        case_folders = [d for d in os.listdir(TARGET_DIR) if os.path.isdir(os.path.join(TARGET_DIR, d)) and d.startswith("length")]
        print(f"[SUCCESS] Extracted {len(case_folders)} benchmark cases to {TARGET_DIR}.")
    else:
        print(f"[WARNING] Extracted, but {TARGET_DIR} not found. Checking structure...")
        # Check if extracted to benchmarks directly
        print(os.listdir("benchmarks"))

if __name__ == "__main__":
    setup_benchmark()
