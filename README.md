# Agentic Framework for By-Target Data Transformation
**CSE 598: Distributed and Scalable Machine Learning (DISML)**  
**Coding Assignment 4: Table-to-Table (TbT) Transformation Pipeline Synthesis**  
**Author:** Vedang Avaghade  
**Institution:** Arizona State University  

---

> **Note on Submission & Code Archive:**  
> The complete submission archive (`A4_vavaghad.zip`, 2.94 MB) containing all code, candidate scripts, execution logs, and benchmark evaluation outputs is available at:  
> [Google Drive Code Archive (A4_vavaghad.zip)](https://drive.google.com/file/d/1HAi_VNF-OSupRAzMxHxeJombxGW8wUri/view?usp=sharing)  
> `https://drive.google.com/file/d/1HAi_VNF-OSupRAzMxHxeJombxGW8wUri/view?usp=sharing`

---

## 1. Overview

This repository implements an LLM-based agentic framework that, given a **source table** (`training_0.csv`) and a **target table** (`target.csv`), synthesizes executable Python/Pandas code (`transform.py`) that transforms the source into the target. The generated code is evaluated on unseen evaluation data (`test_0.csv`) across the 105-case Smart Building benchmark.

### Implemented Prompting Strategies:
1. **Strategy 1: Zero-shot Chain-of-Thought (CoT)** — Greedy decoding ($T=0$), visible operator reasoning plan before code generation.
2. **Strategy 2: Few-shot Chain-of-Thought (CoT)** — Greedy decoding ($T=0$), prepended with 3 worked demonstrations from the 5 fixed held-out cases.
3. **Strategy 3: Zero-shot CoT + Self-Consistency (SC)** — Samples $k=5$ candidates ($T=0.7$), executes each candidate against the source sample, hashes output DataFrames, and votes for the largest cluster.
4. **Strategy 4 (BONUS): Few-shot CoT + Self-Consistency (SC)** — Combines few-shot demonstration prompting with behavioral execution voting ($k=5$).

### Fixed Demonstration Split:
Per assignment specification, 5 cases were held out as demonstrations:
`length1_1`, `length2_1`, `length3_1`, `length4_1`, `length5_1`.  
All reported metrics evaluate exclusively on the remaining **100 test cases**.

---

## 2. Sol Supercomputer Setup Guide

### Step 2.1: Allocate an Interactive Session on Sol
Connect to Sol and request an interactive node:
```bash
# Request an interactive session with 4 CPUs, 16GB RAM, and 4 hours
interactive -p general -q public -t 4:00:00 -c 4 --mem=16G
```
*(If using a GPU queue or already inside an interactive session, you can proceed directly).*

### Step 2.2: Clone the Repository to Sol
```bash
git clone https://github.com/Vedang1308/Agentic_Framework_for_By-Target_Data_Transformation.git
cd Agentic_Framework_for_By-Target_Data_Transformation
```

### Step 2.3: Load Python and Set Up Virtual Environment
```bash
# Load Mamba / Python module on Sol
module load mamba/latest

# Create and activate a clean Python 3.10 environment
conda create -n tbt_env python=3.10 -y
conda activate tbt_env

# Install project requirements
pip install -r requirements.txt
```

---

## 3. Dataset Setup on Sol

The benchmark dataset must be extracted to `benchmarks/smartbuilding-pipelines-v2-split/`.

### Option A: Automatic Download via `setup_data.py` (Recommended)
Run the automated downloader script:
```bash
python setup_data.py
```
This automatically downloads `smartbuilding-pipelines-v2-split.zip` from Google Drive and unpacks all 105 cases into `benchmarks/smartbuilding-pipelines-v2-split/`.

### Option B: Transfer from Local Machine via SCP
From your local machine (in a new terminal):
```bash
scp "smartbuilding-pipelines-v2-split.zip" <your_asurite>@sol.rc.asu.edu:~/Agentic_Framework_for_By-Target_Data_Transformation/
```
Then on Sol, run:
```bash
python setup_data.py
```

---

## 4. API Configuration

Export your ASU Research Computing Voyager API credentials:
```bash
export OPENAI_API_KEY="<your-voyager-api-key-here>"
export OPENAI_BASE_URL="https://openai.rc.asu.edu/v1"
```

---

## 5. Running the Benchmark

You can run individual strategies or all strategies in sequence. All completions are cached under `logs/`, so interrupted runs resume automatically without re-prompting or wasting quota.

### Run All Strategies in Sequence:
```bash
python run_benchmark.py --strategy all --model qwen36-27b --cases all
```

### Or Run Individual Strategies:

#### Strategy 1: Zero-shot CoT
```bash
python run_benchmark.py --strategy zero_shot_cot --model qwen36-27b --cases all
```

#### Strategy 2: Few-shot CoT
```bash
python run_benchmark.py --strategy few_shot_cot --model qwen36-27b --cases all
```

#### Strategy 3: Zero-shot CoT + Self-Consistency ($k=5$)
```bash
python run_benchmark.py --strategy zero_shot_sc --model qwen36-27b --cases all --k 5
```

#### Strategy 4 (Bonus): Few-shot CoT + Self-Consistency ($k=5$)
```bash
python run_benchmark.py --strategy few_shot_sc --model qwen36-27b --cases all --k 5
```

---

## 6. Summarizing Results & Generating Tables

After running the benchmark, summarize the results across all 6 required metrics:
```bash
python summarize.py
```
This command:
1. Calculates:
   - Exact-match accuracy (`autopipeline`) — **headline official metric**
   - Exact-match accuracy (`hard_match`) — auxiliary metric
   - Mean partial credit (`hard_match`)
   - Execution rate
   - Token usage and wall-clock time
   - Performance breakdown by pipeline length (`length1`, `length2`, ...)
2. Generates `summary.csv`.
3. Saves LaTeX tables in `results/table_summary.tex`.
4. Generates the bar chart: `figures/accuracy_by_length.png`.

---

## 7. Diagnosing Failure Modes

Extract the top 4 failure modes with real prompt excerpts, wrong code, and validator diagnostics for Section 4 of the report:
```bash
python analyze_failures.py
```

---

## 8. Generating the Report

Generate the finalized Markdown report integrating the actual experimental numbers:
```bash
python generate_report.py
```
The output `FINAL_REPORT.md` is populated with the complete 7-section analysis, SQLMorpher comparison, and tables, ready for conversion to PDF (`A4_<asurite>.pdf`).

---

## 9. Packaging Submission for Gradescope

Create the clean, compliant Gradescope zip file (`A4_<asurite>.zip`):
```bash
python package_submission.py --asurite <YOUR_ASURITE_ID>
```
Example:
```bash
python package_submission.py --asurite vwaghad
```
The script validates that all required files (`strategies/`, `prompting.py`, `run_benchmark.py`, `summarize.py`, `README.md`, `demos/`, `results/`, `generated/`, `logs/`, `summary.csv`) are present and verifies that NO benchmark CSVs or API keys are bundled.

Upload:
* `A4_<asurite>.zip` to Gradescope Code Submission
* `A4_<asurite>.pdf` to Gradescope Report Submission
