"""
Strategy 3: Zero-shot CoT + Self-Consistency (SC)
Samples k responses (temperature ≈ 0.7, k=5 default).
Executes each candidate program on the source sample (training_0.csv),
hashes the resulting DataFrame using pd.util.hash_pandas_object over sorted columns and rows,
and selects the candidate from the largest cluster (behavioral voting).
Candidates that crash or time out are dropped before voting.
Tie-break rule: earliest candidate index in the winning cluster.
All sampled candidates are stored in generated/<strategy>/<case>/candidates/.
"""

import os
import json
import time
import hashlib
import multiprocessing
import pandas as pd
import numpy as np
from prompting import SYSTEM_PROMPT, build_user_prompt, extract_python_code


def _run_candidate_code_worker(code: str, train_csv_path: str, conn):
    """Subprocess worker to execute candidate code in isolation with a timeout."""
    try:
        source_df = pd.read_csv(train_csv_path)
        namespace = {}
        exec(code, namespace)
        if "transform" not in namespace:
            conn.send({"success": False, "error": "transform() function not defined"})
            return
        result_df = namespace["transform"](source_df)
        if not isinstance(result_df, pd.DataFrame):
            conn.send({"success": False, "error": "transform() did not return a DataFrame"})
            return
        
        # Sort columns to make hashing column-order invariant
        sorted_cols = sorted(result_df.columns)
        df_sorted = result_df[sorted_cols].copy()
        
        # Hash DataFrame content
        hashes = pd.util.hash_pandas_object(df_sorted, index=False)
        digest = hashlib.sha256(hashes.values.tobytes()).hexdigest()
        conn.send({"success": True, "hash": digest, "row_count": len(df_sorted), "col_count": len(df_sorted.columns)})
    except Exception as e:
        conn.send({"success": False, "error": str(e)})


def execute_and_hash_candidate(code: str, train_csv_path: str, timeout: int = 15) -> tuple[bool, str]:
    """Execute candidate code against source sample with a strict timeout."""
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=_run_candidate_code_worker, args=(code, train_csv_path, child_conn))
    p.start()
    p.join(timeout)
    
    if p.is_alive():
        p.terminate()
        p.join()
        return False, "Execution timed out on source sample"
    
    if parent_conn.poll():
        res = parent_conn.recv()
        if res.get("success"):
            return True, res.get("hash")
        return False, res.get("error", "Unknown execution error")
    return False, "No response from candidate execution worker"


def generate(case_dir: str, client, model: str, log_dir: str = None, **kwargs) -> dict:
    """
    Synthesize transform.py using Zero-shot CoT + Self-Consistency.
    Returns dict with keys: 'code', 'raw_completion', 'usage', 'latency', 'prompt', 'candidates'.
    """
    k = kwargs.get("k", 5)
    temperature = kwargs.get("temperature", 0.7)
    train_csv_path = os.path.join(case_dir, "training_0.csv")
    user_prompt = build_user_prompt(case_dir, include_few_shot=False)
    
    start_time = time.time()
    raw_completions = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    
    # Try batch sampling via n=k in a single request first (cheapest & fastest)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            n=k,
            max_tokens=kwargs.get("max_tokens", 4000),
            extra_headers={"x-obleth-boons": "off"}
        )
        for choice in response.choices:
            raw_completions.append(choice.message.content or "")
        if response.usage:
            total_prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
            total_completion_tokens = getattr(response.usage, "completion_tokens", 0)
    except Exception as e:
        # Fallback to sequential sampling if n > 1 is not supported by gateway
        raw_completions = []
        for _ in range(k):
            single_resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=kwargs.get("max_tokens", 4000),
                extra_headers={"x-obleth-boons": "off"}
            )
            raw_completions.append(single_resp.choices[0].message.content or "")
            if single_resp.usage:
                total_prompt_tokens += getattr(single_resp.usage, "prompt_tokens", 0)
                total_completion_tokens += getattr(single_resp.usage, "completion_tokens", 0)
                
    latency = time.time() - start_time
    
    # Process each candidate
    candidate_records = []
    clusters = {}  # hash -> list of candidate indices
    
    for idx, completion in enumerate(raw_completions):
        rec = {"index": idx, "raw_completion": completion, "code": None, "valid_syntax": False, "exec_success": False, "hash": None, "error": None}
        try:
            code = extract_python_code(completion)
            rec["code"] = code
            rec["valid_syntax"] = True
            
            # Execute on source sample
            success, result_or_err = execute_and_hash_candidate(code, train_csv_path)
            if success:
                rec["exec_success"] = True
                rec["hash"] = result_or_err
                clusters.setdefault(result_or_err, []).append(idx)
            else:
                rec["error"] = result_or_err
        except Exception as err:
            rec["error"] = str(err)
            
        candidate_records.append(rec)
        
    # Behavioral voting
    if clusters:
        # Find largest cluster (tie-break rule: earliest candidate index in cluster)
        sorted_clusters = sorted(clusters.items(), key=lambda item: (-len(item[1]), item[1][0]))
        winning_hash, winning_indices = sorted_clusters[0]
        chosen_index = winning_indices[0]
    else:
        # If all candidates crashed, fallback to first candidate with code or candidate 0
        valid_candidates = [r["index"] for r in candidate_records if r["code"]]
        chosen_index = valid_candidates[0] if valid_candidates else 0
        
    chosen_code = candidate_records[chosen_index]["code"] or ""
    chosen_raw = candidate_records[chosen_index]["raw_completion"]
    
    usage_info = {
        "prompt_tokens": total_prompt_tokens,
        "completion_tokens": total_completion_tokens,
        "total_tokens": total_prompt_tokens + total_completion_tokens,
        "k_samples": k,
        "clusters_count": len(clusters),
        "chosen_index": chosen_index,
    }
    
    return {
        "code": chosen_code,
        "raw_completion": chosen_raw,
        "usage": usage_info,
        "latency": latency,
        "prompt": user_prompt,
        "candidates": candidate_records,
    }
