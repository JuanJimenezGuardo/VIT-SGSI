"""Demo script: sequential risk recalculation."""

from __future__ import annotations

import argparse
import json
from time import perf_counter


def compute_risk_score(probability: int, impact: int, cpu_iterations: int = 0) -> int:
    base_score = probability * impact
    # Simula carga CPU de un cálculo de riesgo más complejo.
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


def recalc_risks_sequential(risks: list[dict], cpu_iterations: int = 0) -> list[dict]:
    results: list[dict] = []
    for risk in risks:
        inherent_score = compute_risk_score(
            int(risk["inherent_probability"]),
            int(risk["inherent_impact"]),
            cpu_iterations=cpu_iterations,
        )
        residual_score = adjust_residual_score(
            str(risk["treatment"]),
            inherent_score,
        )
        results.append(
            {
                "id": int(risk["id"]),
                "inherent_score": inherent_score,
                "residual_score": residual_score,
            }
        )
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
    parser = argparse.ArgumentParser(description="Sequential recalculation demo")
    parser.add_argument("--size", type=int, default=10000, help="Number of risks")
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
    output = recalc_risks_sequential(risks, cpu_iterations=args.cpu_iterations)
    elapsed = perf_counter() - start

    print(f"Sequential risks processed: {len(output)}")
    print(f"Sequential time: {elapsed:.6f} s")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(output, handle, indent=2)
        print(f"Saved output: {args.json_out}")


if __name__ == "__main__":
    main()
