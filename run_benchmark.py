#!/usr/bin/env python3
"""
Benchmark Runner for By-Target Data Transformation
Implements run_benchmark.py CLI as specified in Instructions.pdf Pages 8-9.

Usage:
  python run_benchmark.py --strategy zero_shot_cot --model qwen36-27b --cases all
  python run_benchmark.py --strategy few_shot_cot --model qwen36-27b --cases all
  python run_benchmark.py --strategy zero_shot_sc --model qwen36-27b --cases all --k 5
  python run_benchmark.py --strategy few_shot_sc --model qwen36-27b --cases all --k 5
  python run_benchmark.py --strategy all --model qwen36-27b --cases all
"""

import os
import sys
import json
import time
import shutil
import argparse
import tempfile
import subprocess
import pickle
import threading
import concurrent.futures
import pandas as pd
from openai import OpenAI
from tqdm import tqdm

from validation.validator import validate_autopipeline_style
from demos.demonstrations import HELD_OUT_CASES
from strategies import STRATEGIES

DEFAULT_BENCHMARK_DIR = os.path.join("benchmarks", "smartbuilding-pipelines-v2-split")
DEFAULT_MODEL = "qwen36-27b"
DEFAULT_TIMEOUT = 120  # seconds


def parse_args():
    parser = argparse.ArgumentParser(description="Run TbT Data Transformation Benchmark")
    parser.add_argument(
        "--strategy",
        type=str,
        default="zero_shot_cot",
        help="Strategy to run: zero_shot_cot, few_shot_cot, zero_shot_sc, few_shot_sc, or 'all'",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Model ID (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--cases",
        type=str,
        default="all",
        help="Cases to evaluate: 'all' (runs on the 100 test cases) or comma-separated list of cases",
    )
    parser.add_argument(
        "--benchmark_dir",
        type=str,
        default=DEFAULT_BENCHMARK_DIR,
        help="Path to benchmark case folders",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Number of self-consistency samples (default: 5)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Execution timeout in seconds (default: {DEFAULT_TIMEOUT}s)",
    )
    parser.add_argument(
        "--reasoning_effort",
        type=str,
        default="none",
        help="Reasoning effort: none (default, avoids empty content), low, medium, high",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=4000,
        help="Max output tokens (default: 4000)",
    )
    parser.add_argument(
        "--include_demos",
        action="store_true",
        help="Include the 5 held-out demo cases in evaluation (default: False)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of concurrent workers (default: 1, recommendation: 2-3 for faster runs)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore cached completions and re-run LLM calls",
    )
    return parser.parse_args()


def get_all_case_folders(benchmark_dir: str, include_demos: bool = False) -> list[str]:
    """Retrieve benchmark case folders sorted naturally by pipeline length."""
    if not os.path.exists(benchmark_dir):
        alt = "smartbuilding-pipelines-v2-split"
        if os.path.exists(alt):
            benchmark_dir = alt
        else:
            raise FileNotFoundError(
                f"Benchmark directory '{benchmark_dir}' not found. Run python setup_data.py first."
            )

    folders = []
    for d in os.listdir(benchmark_dir):
        full_p = os.path.join(benchmark_dir, d)
        if os.path.isdir(full_p) and d.startswith("length"):
            folders.append(d)

    def case_sort_key(name):
        parts = name.replace("length", "").split("_")
        try:
            return (int(parts[0]), int(parts[1]))
        except Exception:
            return (999, name)

    folders.sort(key=case_sort_key)

    if not include_demos:
        folders = [c for c in folders if c not in HELD_OUT_CASES]

    return folders


def execute_generated_code_subprocess(
    code: str, test_csv_path: str, timeout_sec: int = 120
) -> tuple[bool, pd.DataFrame | None, str | None, bool]:
    """
    Executes generated code in a sandboxed subprocess.
    Returns (success, result_df, error_message, is_timeout).
    """
    if not code or not code.strip():
        return False, None, "No code to execute.", False

    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "transform.py")
        runner_path = os.path.join(tmpdir, "run_exec.py")
        out_pickle = os.path.join(tmpdir, "output.pkl")

        with open(code_path, "w") as f:
            f.write(code)

        runner_script = f"""
import sys
import pickle
import pandas as pd
from transform import transform

try:
    source_df = pd.read_csv({repr(os.path.abspath(test_csv_path))})
    res_df = transform(source_df)
    if not isinstance(res_df, pd.DataFrame):
        raise TypeError("transform() returned " + type(res_df).__name__ + ", expected pandas DataFrame")
    with open({repr(out_pickle)}, "wb") as f:
        pickle.dump(res_df, f)
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        with open(runner_path, "w") as f:
            f.write(runner_script)

        try:
            proc = subprocess.run(
                [sys.executable, runner_path],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
            if proc.returncode != 0:
                err_msg = proc.stderr.strip() or proc.stdout.strip() or f"Process exited with code {proc.returncode}"
                return False, None, err_msg, False

            if not os.path.exists(out_pickle):
                return False, None, "No output DataFrame generated.", False

            with open(out_pickle, "rb") as f:
                result_df = pickle.load(f)
            return True, result_df, None, False

        except subprocess.TimeoutExpired:
            return False, None, f"Execution timed out after {timeout_sec} seconds", True
        except Exception as e:
            return False, None, f"Subprocess execution error: {e}", False


def call_with_retry(func, max_retries: int = 5, backoff_factor: float = 2.0):
    """Executes func with exponential backoff on rate-limits (429) or busy gateway (503)."""
    delay = 1.0
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            err_str = str(e)
            if ("429" in err_str or "503" in err_str or "rate" in err_str.lower() or "busy" in err_str.lower()) and attempt < max_retries - 1:
                print(f"[Gateway busy / 429] Retrying in {delay:.1f}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(delay)
                delay *= backoff_factor
            else:
                raise


def run_single_case(
    case_name: str,
    strategy_name: str,
    benchmark_dir: str,
    client: OpenAI,
    model: str,
    timeout: int = 120,
    k: int = 5,
    reasoning_effort: str = "none",
    max_tokens: int = 4000,
    force: bool = False,
) -> dict:
    """Runs a single benchmark case for the chosen strategy."""
    case_dir = os.path.join(benchmark_dir, case_name)
    test_csv = os.path.join(case_dir, "test_0.csv")
    target_csv = os.path.join(case_dir, "target.csv")

    log_dir = os.path.join("logs", strategy_name, case_name)
    gen_dir = os.path.join("generated", strategy_name, case_name)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(gen_dir, exist_ok=True)

    cache_file = os.path.join(log_dir, "completion.json")
    prompt_file = os.path.join(log_dir, "prompt.txt")
    completion_file = os.path.join(log_dir, "completion.txt")
    code_file = os.path.join(gen_dir, "transform.py")

    gen_func = STRATEGIES[strategy_name]

    # Attempt generation with cache check
    gen_error = None
    gen_result = {}
    code = ""

    try:
        if not force and os.path.exists(cache_file) and os.path.exists(code_file):
            with open(cache_file, "r") as f:
                gen_result = json.load(f)
            with open(code_file, "r") as f:
                code = f.read()
            gen_result["code"] = code
        else:
            def _invoke():
                return gen_func(
                    case_dir,
                    client,
                    model,
                    log_dir=log_dir,
                    k=k,
                    reasoning_effort=reasoning_effort,
                    max_tokens=max_tokens,
                )

            gen_result = call_with_retry(_invoke)
            code = gen_result.get("code", "")

            # Write prompt and raw completion logs
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(gen_result.get("prompt", ""))
            with open(completion_file, "w", encoding="utf-8") as f:
                f.write(gen_result.get("raw_completion", ""))
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)

            # If candidates are present (self-consistency), save each to candidates/
            if "candidates" in gen_result and gen_result["candidates"]:
                cand_dir = os.path.join(gen_dir, "candidates")
                os.makedirs(cand_dir, exist_ok=True)
                for c_info in gen_result["candidates"]:
                    c_idx = c_info["index"]
                    c_code = c_info.get("code") or ""
                    with open(os.path.join(cand_dir, f"candidate_{c_idx}.py"), "w", encoding="utf-8") as f:
                        f.write(c_code)

            # Write cache json
            cache_data = {
                "usage": gen_result.get("usage", {}),
                "latency": gen_result.get("latency", 0),
                "strategy": strategy_name,
                "case": case_name,
                "model": model,
            }
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)

    except Exception as e:
        gen_error = str(e)
        gen_result = {
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "latency": 0.0,
            "prompt": "",
            "raw_completion": "",
        }
        code = ""

    # Execute generated code on test_0.csv in sandboxed subprocess
    target_df = pd.read_csv(target_csv)
    if code and not gen_error:
        exec_success, result_df, exec_err, is_timeout = execute_generated_code_subprocess(
            code, test_csv, timeout_sec=timeout
        )
    else:
        exec_success = False
        result_df = None
        exec_err = gen_error or "Generation failed"
        is_timeout = False

    if exec_success and result_df is not None:
        try:
            ap_acc, ap_corr, ap_scores, ap_matches = validate_autopipeline_style(
                result_df, target_df, method="autopipeline"
            )
            hm_acc, hm_corr, hm_scores, hm_matches = validate_autopipeline_style(
                result_df, target_df, method="hard_match"
            )
        except Exception as val_e:
            ap_acc, ap_corr, ap_scores, ap_matches = 0.0, False, [], [f"Validator error: {val_e}"]
            hm_acc, hm_corr, hm_scores, hm_matches = 0.0, False, [], [f"Validator error: {val_e}"]
    else:
        ap_acc, ap_corr, ap_scores, ap_matches = 0.0, False, [], [exec_err or "Execution failure"]
        hm_acc, hm_corr, hm_scores, hm_matches = 0.0, False, [], [exec_err or "Execution failure"]

    # Parse pipeline length
    length_part = case_name.replace("length", "").split("_")[0]
    pipeline_length = int(length_part) if length_part.isdigit() else 1

    safe_hm_scores = []
    if isinstance(hm_scores, list):
        for s in hm_scores:
            try:
                safe_hm_scores.append(float(s))
            except (ValueError, TypeError):
                safe_hm_scores.append(0.0)

    safe_ap_scores = []
    if isinstance(ap_scores, list):
        for s in ap_scores:
            try:
                safe_ap_scores.append(float(s))
            except (ValueError, TypeError):
                safe_ap_scores.append(0.0)

    record = {
        "case": case_name,
        "pipeline_length": pipeline_length,
        "strategy": strategy_name,
        "model": model,
        "autopipeline": {
            "accuracy": float(ap_acc),
            "is_correct": bool(ap_corr),
            "matched_cols": ap_matches if isinstance(ap_matches, list) else [],
        },
        "hard_match": {
            "accuracy": float(hm_acc),
            "is_correct": bool(hm_corr),
            "similarity_scores": safe_hm_scores,
            "matched_cols": hm_matches if isinstance(hm_matches, list) else [],
        },
        "execution": {
            "success": bool(exec_success),
            "error": exec_err,
            "timeout": bool(is_timeout),
        },
        "usage": gen_result.get("usage", {}),
        "latency": gen_result.get("latency", 0.0),
        "prompt_path": prompt_file,
        "completion_path": completion_file,
        "code_path": code_file,
    }
    return record


def run_benchmark_for_strategy(strategy: str, args, client: OpenAI):
    """Runs all requested cases for a given strategy and records to results/<strategy>.jsonl."""
    os.makedirs("results", exist_ok=True)
    results_path = os.path.join("results", f"{strategy}.jsonl")

    # Determine cases
    if args.cases.lower() == "all":
        case_list = get_all_case_folders(args.benchmark_dir, include_demos=args.include_demos)
    else:
        case_list = [c.strip() for c in args.cases.split(",") if c.strip()]

    print(f"\n========================================================")
    print(f"Running Benchmark: Strategy='{strategy}' | Model='{args.model}'")
    print(f"Reasoning Effort: '{args.reasoning_effort}' | Max Tokens: {args.max_tokens}")
    print(f"Total Cases to Evaluate: {len(case_list)}")
    print(f"Results File: {results_path}")
    print(f"========================================================")

    # Read existing completed cases to enable resume
    completed_cases = set()
    if os.path.exists(results_path) and not args.force:
        with open(results_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        obj = json.loads(line)
                        completed_cases.add(obj.get("case"))
                    except Exception:
                        pass
        print(f"Found {len(completed_cases)} existing results in {results_path} (resuming).")

    cases_to_run = [c for c in case_list if args.force or c not in completed_cases]
    file_lock = threading.Lock()

    if args.workers > 1 and len(cases_to_run) > 1:
        print(f"Executing with {args.workers} concurrent workers...")
        pbar = tqdm(total=len(case_list), initial=len(completed_cases), desc=f"Strategy: {strategy}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    run_single_case,
                    case_name=c,
                    strategy_name=strategy,
                    benchmark_dir=args.benchmark_dir,
                    client=client,
                    model=args.model,
                    timeout=args.timeout,
                    k=args.k,
                    reasoning_effort=args.reasoning_effort,
                    max_tokens=args.max_tokens,
                    force=args.force,
                ): c
                for c in cases_to_run
            }
            for fut in concurrent.futures.as_completed(futures):
                c_name = futures[fut]
                try:
                    record = fut.result()
                    with file_lock:
                        with open(results_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps(record) + "\n")
                    status_str = "CORRECT" if record["autopipeline"]["is_correct"] else "INCORRECT"
                    pbar.set_postfix({
                        "case": c_name,
                        "status": status_str,
                        "ap_acc": f"{record['autopipeline']['accuracy']:.2f}",
                        "hm_acc": f"{record['hard_match']['accuracy']:.2f}",
                    })
                except Exception as e:
                    print(f"\n[ERROR] Case '{c_name}' failed: {e}")
                finally:
                    pbar.update(1)
        pbar.close()
    else:
        pbar = tqdm(case_list, desc=f"Strategy: {strategy}")
        for case_name in pbar:
            if case_name in completed_cases and not args.force:
                continue

            try:
                record = run_single_case(
                    case_name=case_name,
                    strategy_name=strategy,
                    benchmark_dir=args.benchmark_dir,
                    client=client,
                    model=args.model,
                    timeout=args.timeout,
                    k=args.k,
                    reasoning_effort=args.reasoning_effort,
                    max_tokens=args.max_tokens,
                    force=args.force,
                )

                # Append JSON line to results file
                with open(results_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")

                status_str = "CORRECT" if record["autopipeline"]["is_correct"] else "INCORRECT"
                pbar.set_postfix({
                    "case": case_name,
                    "status": status_str,
                    "ap_acc": f"{record['autopipeline']['accuracy']:.2f}",
                    "hm_acc": f"{record['hard_match']['accuracy']:.2f}",
                })
            except Exception as e:
                print(f"\n[ERROR] Case '{case_name}' failed with unexpected exception: {e}")
                import traceback
                traceback.print_exc()

    print(f"\n[DONE] Strategy '{strategy}' completed. Results saved to {results_path}")


def main():
    args = parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://openai.rc.asu.edu/v1")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY environment variable is not set.")
        print("Please export OPENAI_API_KEY='<your-api-key>'")
        print("and optionally export OPENAI_BASE_URL='https://openai.rc.asu.edu/v1'")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=base_url)

    if args.strategy.lower() == "all":
        strategies_to_run = ["zero_shot_cot", "few_shot_cot", "zero_shot_sc", "few_shot_sc"]
    else:
        strategies_to_run = [s.strip() for s in args.strategy.split(",") if s.strip()]

    for strat in strategies_to_run:
        if strat not in STRATEGIES:
            print(f"[ERROR] Unknown strategy: '{strat}'. Choose from {list(STRATEGIES.keys())}")
            sys.exit(1)

    for strat in strategies_to_run:
        run_benchmark_for_strategy(strat, args, client)


if __name__ == "__main__":
    main()
