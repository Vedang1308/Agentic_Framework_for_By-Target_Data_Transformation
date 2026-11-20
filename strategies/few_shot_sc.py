"""
Strategy 4: Few-shot CoT + Self-Consistency (Bonus Strategy)
Combines Few-shot demonstrations with Self-Consistency sampling (k=5, temperature ≈ 0.7).
Executes each candidate on the source sample (training_0.csv),
hashes resulting DataFrames, and performs behavioral cluster voting.
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
from strategies.zero_shot_sc import execute_and_hash_candidate, _extract_choice_text


def generate(case_dir: str, client, model: str, log_dir: str = None, **kwargs) -> dict:
    """
    Synthesize transform.py using Few-shot CoT + Self-Consistency.
    Returns dict with keys: 'code', 'raw_completion', 'usage', 'latency', 'prompt', 'candidates'.
    """
    k = kwargs.get("k", 5)
    temperature = kwargs.get("temperature", 0.7)
    num_demos = kwargs.get("num_demos", 3)
    reasoning_effort = kwargs.get("reasoning_effort", "none")
    max_tokens = kwargs.get("max_tokens", 4000)
    train_csv_path = os.path.join(case_dir, "training_0.csv")
    user_prompt = build_user_prompt(case_dir, include_few_shot=True, num_demos=num_demos)
    
    start_time = time.time()
    raw_completions = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    
    # Try batch sampling via n=k first
    try:
        create_kwargs = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "n": k,
            "max_tokens": max_tokens,
            "extra_headers": {"x-obleth-boons": "off"}
        }
        if reasoning_effort is not None:
            create_kwargs["reasoning_effort"] = reasoning_effort
            
        response = client.chat.completions.create(**create_kwargs)
        for choice in response.choices:
            raw_completions.append(_extract_choice_text(choice))
        if response.usage:
            total_prompt_tokens = getattr(response.usage, "prompt_tokens", 0)
            total_completion_tokens = getattr(response.usage, "completion_tokens", 0)
    except Exception as e:
        raw_completions = []
        for _ in range(k):
            single_kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "extra_headers": {"x-obleth-boons": "off"}
            }
            if reasoning_effort is not None:
                single_kwargs["reasoning_effort"] = reasoning_effort
            single_resp = client.chat.completions.create(**single_kwargs)
            raw_completions.append(_extract_choice_text(single_resp.choices[0]))
            if single_resp.usage:
                total_prompt_tokens += getattr(single_resp.usage, "prompt_tokens", 0)
                total_completion_tokens += getattr(single_resp.usage, "completion_tokens", 0)
                
    latency = time.time() - start_time
    
    # Process each candidate
    candidate_records = []
    clusters = {}
    
    for idx, completion in enumerate(raw_completions):
        rec = {"index": idx, "raw_completion": completion, "code": None, "valid_syntax": False, "exec_success": False, "hash": None, "error": None}
        try:
            code = extract_python_code(completion)
            rec["code"] = code
            rec["valid_syntax"] = True
            
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
        sorted_clusters = sorted(clusters.items(), key=lambda item: (-len(item[1]), item[1][0]))
        winning_hash, winning_indices = sorted_clusters[0]
        chosen_index = winning_indices[0]
    else:
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
