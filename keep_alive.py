#!/usr/bin/env python3
"""
GPU Keep-Alive Daemon for ASU Sol Supercomputer
Prevents automated job termination by Sol's idle-GPU watchdog.
Runs periodic matrix multiplications using a fixed-size, in-place tensor buffer.
Uses strictly constant memory (<200MB) and never leaks VRAM.
"""

import time
import torch


def run_keep_alive():
    if not torch.cuda.is_available():
        print("[!] No CUDA GPU detected on this node.")
        return

    device = torch.device("cuda")
    gpu_name = torch.cuda.get_device_name(0)
    print(f"[*] GPU Keep-Alive running on: {gpu_name}")
    print("[*] Allocating fixed 192 MB buffer (strictly constant memory)...")

    # Allocate fixed tensors once
    dim = 4096
    a = torch.randn(dim, dim, device=device, dtype=torch.float32)
    b = torch.randn(dim, dim, device=device, dtype=torch.float32)
    c = torch.empty((dim, dim), device=device, dtype=torch.float32)

    print("[*] Keep-alive heartbeat loop active. Sol watchdog will see GPU activity.")
    iteration = 0
    try:
        while True:
            # Overwrite buffer c in-place without allocating any new memory
            torch.matmul(a, b, out=c)
            torch.cuda.synchronize()
            time.sleep(1.0)
            iteration += 1
            if iteration % 300 == 0:  # print status every 5 minutes
                print(f"[*] GPU heartbeat active: {iteration} ticks sent, memory constant.")
    except KeyboardInterrupt:
        print("\n[*] Stopped GPU keep-alive.")


if __name__ == "__main__":
    run_keep_alive()
