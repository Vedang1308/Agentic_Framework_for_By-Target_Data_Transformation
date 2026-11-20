"""
Strategy 2: Few-shot Chain-of-Thought (CoT)
Greedy decoding (temperature=0), 1 LLM call per case.
Supplies 2-4 worked examples (source sample, target sample, reasoning, code)
from the fixed held-out demonstration split.
"""

import os
import json
import time
from prompting import SYSTEM_PROMPT, build_user_prompt, extract_python_code


def generate(case_dir: str, client, model: str, log_dir: str = None, **kwargs) -> dict:
    """
    Synthesize transform.py for case_dir using Few-shot CoT.
    Returns dict with keys: 'code', 'raw_completion', 'usage', 'latency', 'prompt'.
    """
    num_demos = kwargs.get("num_demos", 3)
    user_prompt = build_user_prompt(case_dir, include_few_shot=True, num_demos=num_demos)
    
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        max_tokens=kwargs.get("max_tokens", 4000),
        extra_headers={"x-obleth-boons": "off"}
    )
    
    latency = time.time() - start_time
    choice = response.choices[0]
    raw_completion = choice.message.content or ""
    
    code = extract_python_code(raw_completion)
    
    usage_info = {
        "prompt_tokens": getattr(response.usage, "prompt_tokens", 0) if response.usage else 0,
        "completion_tokens": getattr(response.usage, "completion_tokens", 0) if response.usage else 0,
        "total_tokens": getattr(response.usage, "total_tokens", 0) if response.usage else 0,
    }
    
    return {
        "code": code,
        "raw_completion": raw_completion,
        "usage": usage_info,
        "latency": latency,
        "prompt": user_prompt,
    }
