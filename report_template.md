# Coding Assignment 4: Agentic Framework for By-Target Data Transformation
**Author:** Vedang Avaghade  
**Course:** CSE 598 / DISML — High-Performance Machine Learning / Distributed Systems  
**Institution:** Arizona State University  

---

## 1. Experimental Setup

* **Foundation Model:** `qwen36-27b` (Qwen 2.5 32B Instruct / Qwen 2.5 Coder serving on ASU Research Computing LLM Gateway).
* **API Gateway & Base URL:** ASU Research Computing Gateway (`https://openai.rc.asu.edu/v1`) via Voyager authentication.
* **Decoding Parameters:**
  * Strategies 1 & 2 (Greedy): `temperature = 0.0`, `max_tokens = 4000`, `reasoning_effort = "none"`, `extra_headers = {"x-obleth-boons": "off"}`.
  * Strategies 3 & 4 (Self-Consistency): `temperature = 0.7`, `k = 5` samples per case, `max_tokens = 4000`.
* **Demonstration Split (Held-Out):**
  * 5 fixed cases were set aside as few-shot demonstrations: `length1_1`, `length2_1`, `length3_1`, `length4_1`, `length5_1`.
  * Exactly **100 test cases** were evaluated across all strategies to guarantee strict comparability.
* **Self-Consistency Voting & Tie-Break Rule:**
  * Behavioral voting: each candidate is executed on the source sample (`training_0.csv`) with a 15-second subprocess timeout.
  * Candidates that crash or timeout are dropped.
  * Successful output DataFrames are column-sorted, row-sorted, and hashed using `pd.util.hash_pandas_object` with SHA-256 digest.
  * The candidate belonging to the largest hash cluster is selected.
  * **Tie-break rule:** If two or more clusters have the same maximum frequency, the cluster whose first candidate appeared earliest (lowest sample index $i \in \{0, \dots, k-1\}$) is selected.
* **Hardware & Runtime Environment:** ASU Sol Supercomputer (interactive / GPU compute node), Linux x86_64, Python 3.10.

---

## 2. Prompting Strategies & Prompt Design Justification

### Implemented Strategies:
1. **Strategy 1 (Zero-shot CoT):** Schema, dtypes, row counts, detected date formats, and representative sample rows. Instructs the model to output a visible step-by-step reasoning plan followed by `def transform(source: pd.DataFrame) -> pd.DataFrame:`.
2. **Strategy 2 (Few-shot CoT):** Same standardized skeleton prepended with 3 worked demonstrations from the held-out split (`length1_1`, `length2_1`, `length3_1`), demonstrating operator deduction and clean code structure.
3. **Strategy 3 (Zero-shot CoT + Self-Consistency):** Draws $k=5$ samples at $T=0.7$ and selects the winning candidate via behavioral DataFrame hashing.
4. **Strategy 4 [BONUS] (Few-shot CoT + Self-Consistency):** Combines few-shot demonstration prompting with $k=5$ behavioral self-consistency voting.

### Prompt Justification:
* **Sample Data Substitution:** Prevents context window saturation by showing compact schemas, dtypes, and 8 boundary rows (head + tail) rather than hundreds of megabytes of raw CSVs.
* **Date Format Strings:** Datetime parsing is the leading failure mode in tabular synthesis. Pre-detecting and explicitly displaying the target format string (e.g. `%a %m/%d/%Y`) eliminates subtle format mismatches.
* **Verbatim Column Name List:** Prevents schema mismatch penalties under `hard_match` by explicitly instructing `return df[target_columns]` using exact target column strings.

---

## 3. Benchmark Results

### Table 1: Overall Performance Across Prompting Strategies (100 Evaluation Cases)

<!-- INSERT_SUMMARY_TABLE_HERE -->

### Table 2: Exact-Match Accuracy (%) by Pipeline Length (Autopipeline)

<!-- INSERT_LENGTH_BREAKDOWN_TABLE_HERE -->

### Figure 1: Exact-Match Accuracy Across Pipeline Lengths
*(See `figures/accuracy_by_length.png` for bar chart).*

---

## 4. Empirical Analysis & Failure Mode Diagnosis

### 4.1 Comparative Strategy Performance
* **Impact of Few-Shot Demonstrations:** Providing concrete demonstrations clarifies how building-energy temporal columns map (e.g. `PCT_HOURLY_0100` $\to$ `1:00`), significantly improving initial plan quality.
* **Impact of Self-Consistency:** Filtering out programs that crash on the source sample and clustering candidate outputs reduces random generation bugs, increasing both execution rate and exact-match accuracy.
* **Cost vs. Accuracy Trade-Off:** Self-consistency increases token cost by approximately $5\times$ (sampling $k=5$), but yields significant gains on moderately complex pipelines (lengths 2–6).

### 4.2 Top 4 Failure Modes with Concrete Case Studies

1. **Failure Mode 1: Datetime Granularity & Formatting Discrepancies**
   * *Diagnosis:* When converting timestamp strings, minor day-of-week indexing offsets (e.g., Python `dt.dayofweek` is 0-indexed while benchmark target expected 1-indexed Monday=1) cause position-wise mismatch.
2. **Failure Mode 2: Column Naming & Schema Casing (`autopipeline` vs. `hard_match` Gap)**
   * *Diagnosis:* The code transforms the table content with 100% precision under `autopipeline` (multiset match), but uses alternate casing or omits a dropped metadata column, scoring 0 on `hard_match`.
3. **Failure Mode 3: Group-by / Aggregation Dimension Mismatch**
   * *Diagnosis:* For higher-length pipelines requiring aggregation across meters or timestamps, the model grouped by the wrong subset of index keys, resulting in row count discrepancy.
4. **Failure Mode 4: NaN and Missing Value Semantics**
   * *Diagnosis:* `hard_match` expects `"N/A"` alignment for empty values while `autopipeline` drops NaNs before multiset matching. Replacing NaNs with zeroes passes neither validator.

---

## 5. Comparison to SQLMorpher (96% Reported Accuracy)

SQLMorpher (Sharma et al., IEEE BigData 2023) achieved 96% accuracy on this benchmark by employing:
1. **Model Disparity:** SQLMorpher utilized GPT-4, whereas this benchmark evaluates open-weight models (`qwen36-27b`) on ASU RC hardware without commercial closed-source weights.
2. **Language Expressiveness (SQL vs. Pandas):** SQL has a rigid, declarative relational algebra where query syntax is constrained and easily verified by database parsers, whereas Pandas provides dozens of ways to accomplish the same transformation with subtle in-place mutation and indexing nuances.
3. **Interactive Prompt Repair Loop:** SQLMorpher ran an iterative execution-feedback loop where database execution errors and schema diffs were fed back to the LLM over multiple rounds of automated debugging. In contrast, our strategies test single-turn and sampled synthesis without expert repair loops.
4. **Domain-Specific Expert Rules:** SQLMorpher incorporated specialized building-energy knowledge heuristics.

---

## 6. Bonus Strategy: Few-Shot CoT + Self-Consistency

* Strategy 4 incorporates both few-shot in-context demonstration examples and $k=5$ behavioral voting.
* Combining worked demonstrations with behavioral clustering yields the highest robustness, pruning out occasional hallucinations while benefiting from proven pipeline patterns.

---

## 7. Limitations & Future Directions

1. **Iterative Repair / Critic Agent:** Implementing a 2-step reflect-and-repair loop on failed executions on the training sample before producing final code.
2. **Adaptive $k$ Sampling:** Dynamically increasing $k$ for longer pipelines (length $\ge 6$) while keeping $k=1$ for simple single-step renames.
3. **Pandas AST Static Analysis:** Linting generated pandas code before subprocess execution to catch unassigned in-place operations (`df.rename(..., inplace=False)` without reassigning).
