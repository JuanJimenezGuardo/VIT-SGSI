"""Benchmark sequential vs parallel risk recalculation for Sprint 3 demo."""

from __future__ import annotations

import argparse
import csv
from statistics import mean
from time import perf_counter

from parallel_recalc import recalc_risks_parallel
from sequential_recalc import recalc_risks_sequential


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


def run_once(size: int, workers: int, cpu_iterations: int) -> dict:
    risks = build_dataset(size)

    t1 = perf_counter()
    seq = recalc_risks_sequential(risks, cpu_iterations=cpu_iterations)
    t2 = perf_counter()

    t3 = perf_counter()
    par = recalc_risks_parallel(risks, workers=workers, cpu_iterations=cpu_iterations)
    t4 = perf_counter()

    if sorted(seq, key=lambda x: x["id"]) != sorted(par, key=lambda x: x["id"]):
        raise ValueError("Sequential and parallel outputs do not match")

    tseq = t2 - t1
    tpar = t4 - t3
    speedup = (tseq / tpar) if tpar > 0 else 0.0
    efficiency = (speedup / workers) if workers > 0 else 0.0

    return {
        "dataset": size,
        "workers": workers,
        "tseq": tseq,
        "tpar": tpar,
        "speedup": speedup,
        "efficiency": efficiency,
    }


def benchmark(
    sizes: list[int],
    workers_list: list[int],
    repetitions: int,
    cpu_iterations: int,
) -> list[dict]:
    rows: list[dict] = []

    for size in sizes:
        for workers in workers_list:
            samples = [run_once(size, workers, cpu_iterations) for _ in range(repetitions)]
            rows.append(
                {
                    "dataset": size,
                    "workers": workers,
                    "tseq": mean([s["tseq"] for s in samples]),
                    "tpar": mean([s["tpar"] for s in samples]),
                    "speedup": mean([s["speedup"] for s in samples]),
                    "efficiency": mean([s["efficiency"] for s in samples]),
                }
            )
    return rows


def print_table(rows: list[dict]) -> None:
    print("\n=== Benchmark Risks (mean values) ===")
    print("dataset | workers | tseq(s) | tpar(s) | speedup | efficiency")
    for row in rows:
        print(
            f"{row['dataset']:>7} | {row['workers']:>7} | "
            f"{row['tseq']:.6f} | {row['tpar']:.6f} | "
            f"{row['speedup']:.4f} | {row['efficiency']:.4f}"
        )


def write_csv(rows: list[dict], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["dataset", "workers", "tseq", "tpar", "speedup", "efficiency"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark risk recalculation")
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=[1000, 5000, 10000],
        help="Dataset sizes",
    )
    parser.add_argument(
        "--workers",
        type=int,
        nargs="+",
        default=[2, 4, 8],
        help="Worker counts",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=3,
        help="Repetitions per scenario",
    )
    parser.add_argument(
        "--cpu-iterations",
        type=int,
        default=0,
        help="Extra deterministic CPU workload per risk",
    )
    parser.add_argument(
        "--csv-out",
        type=str,
        default="",
        help="Optional CSV output path",
    )
    args = parser.parse_args()

    rows = benchmark(args.sizes, args.workers, args.repetitions, args.cpu_iterations)
    print_table(rows)

    if args.csv_out:
        write_csv(rows, args.csv_out)
        print(f"\nSaved CSV: {args.csv_out}")


if __name__ == "__main__":
    main()
