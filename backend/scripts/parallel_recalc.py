"""Demo script: parallel risk recalculation with process pool."""

from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor
from time import perf_counter


def compute_risk_score(probability: int, impact: int, cpu_iterations: int = 0) -> int:
    base_score = probability * impact
    acc = 0
    for i in range(cpu_iterations):
        acc += ((base_score + i) * (i % 7 + 1)) % 13
    return base_score + (acc % 3)


def adjust_residual_score(treatment: str, inherent_score: int) -> int:
    strategy = treatment.strip().upper()
    if strategy == "MITIGATE":
        return max(1, inherent_score - 4)
    if strategy == "TRANSFER":
        return max(1, inherent_score - 3)
    if strategy == "AVOID":
        return 1
    return inherent_score


def process_chunk(args: tuple[list[dict], int]) -> list[dict]:
    chunk, cpu_iterations = args
    partial: list[dict] = []
    for risk in chunk:
        inherent_score = compute_risk_score(
            int(risk["inherent_probability"]),
            int(risk["inherent_impact"]),
            cpu_iterations=cpu_iterations,
        )
        residual_score = adjust_residual_score(str(risk["treatment"]), inherent_score)
        partial.append(
            {
                "id": int(risk["id"]),
                "inherent_score": inherent_score,
                "residual_score": residual_score,
            }
        )
    return partial


def split_chunks(data: list[dict], workers: int) -> list[list[dict]]:
    if not data:
        return []
    chunk_size = max(1, len(data) // workers)
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def recalc_risks_parallel(risks: list[dict], workers: int = 4, cpu_iterations: int = 0) -> list[dict]:
    safe_workers = max(1, min(workers, len(risks) if risks else 1))
    chunks = split_chunks(risks, safe_workers)

    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=safe_workers) as executor:
        payload = [(chunk, cpu_iterations) for chunk in chunks]
        for partial in executor.map(process_chunk, payload):
            results.extend(partial)
    return results


def build_dataset(size: int) -> list[dict]:
    treatments = ["MITIGATE", "ACCEPT", "TRANSFER", "AVOID"]
    return [
        {
            "id": i,
            "inherent_probability": (i % 5) + 1,
            "inherent_impact": ((i + 2) % 5) + 1,
            "treatment": treatments[i % len(treatments)],
        }
        for i in range(1, size + 1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Parallel recalculation demo")
    parser.add_argument("--size", type=int, default=10000, help="Number of risks")
    parser.add_argument(
        "--workers",
        type=int,
        default=max(2, (os.cpu_count() or 2) // 2),
        help="Workers in process pool",
    )
    parser.add_argument(
        "--cpu-iterations",
        type=int,
        default=0,
        help="Extra deterministic CPU workload per risk",
    )
    parser.add_argument(
        "--json-out",
        type=str,
        default="",
        help="Optional output path for JSON result",
    )
    args = parser.parse_args()

    risks = build_dataset(args.size)

    start = perf_counter()
    output = recalc_risks_parallel(
        risks,
        workers=args.workers,
        cpu_iterations=args.cpu_iterations,
    )
    elapsed = perf_counter() - start

    print(f"Parallel risks processed: {len(output)}")
    print(f"Parallel workers: {args.workers}")
    print(f"Parallel time: {elapsed:.6f} s")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(output, handle, indent=2)
        print(f"Saved output: {args.json_out}")


if __name__ == "__main__":
    main()
