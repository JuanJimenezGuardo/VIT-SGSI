from __future__ import annotations

import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from time import perf_counter

from django.utils import timezone

from .models import Job, Risk


@dataclass(frozen=True)
class RiskResult:
    risk_id: int
    score: int
    level: str


def _risk_level(score: int) -> str:
    if score >= 16:
        return "CRITICAL"
    if score >= 10:
        return "HIGH"
    if score >= 5:
        return "MEDIUM"
    return "LOW"


def _compute_one(item: dict) -> RiskResult:
    score = int(item["probability"]) * int(item["impact"])
    return RiskResult(
        risk_id=int(item["id"]),
        score=score,
        level=_risk_level(score),
    )


def _compute_chunk(chunk: list[dict]) -> list[RiskResult]:
    return [_compute_one(item) for item in chunk]


def _build_summary(results: list[RiskResult]) -> dict:
    if not results:
        return {
            "total_risks": 0,
            "average_score": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "top_risks": [],
        }

    by_level = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for result in results:
        by_level[result.level] += 1

    top = sorted(results, key=lambda x: x.score, reverse=True)[:5]
    return {
        "total_risks": len(results),
        "average_score": round(sum(r.score for r in results) / len(results), 2),
        "critical": by_level["CRITICAL"],
        "high": by_level["HIGH"],
        "medium": by_level["MEDIUM"],
        "low": by_level["LOW"],
        "top_risks": [
            {"risk_id": r.risk_id, "score": r.score, "level": r.level} for r in top
        ],
    }


def _run_sequential(risk_items: list[dict]) -> tuple[list[RiskResult], float]:
    start = perf_counter()
    results = [_compute_one(item) for item in risk_items]
    elapsed_ms = (perf_counter() - start) * 1000
    return results, elapsed_ms


def _run_parallel(risk_items: list[dict], worker_count: int) -> tuple[list[RiskResult], float]:
    if not risk_items:
        return [], 0.0

    safe_workers = max(1, min(worker_count, len(risk_items)))
    chunk_size = math.ceil(len(risk_items) / safe_workers)
    chunks = [risk_items[i : i + chunk_size] for i in range(0, len(risk_items), chunk_size)]

    start = perf_counter()
    parallel_results: list[RiskResult] = []
    with ThreadPoolExecutor(max_workers=safe_workers) as pool:
        for chunk_result in pool.map(_compute_chunk, chunks):
            parallel_results.extend(chunk_result)
    elapsed_ms = (perf_counter() - start) * 1000
    return parallel_results, elapsed_ms


def execute_recalc_job(job_id, worker_count: int = 4) -> Job:
    job = Job.objects.select_related("project").get(pk=job_id)
    job.status = "RUNNING"
    job.progress = 5
    job.started_at = timezone.now()
    job.save(update_fields=["status", "progress", "started_at", "updated_at"])

    try:
        risk_items = list(
            Risk.objects.filter(project=job.project, is_archived=False).values(
                "id", "probability", "impact"
            )
        )
        job.progress = 20
        job.save(update_fields=["progress", "updated_at"])

        seq_results, tseq_ms = _run_sequential(risk_items)
        job.progress = 55
        job.save(update_fields=["progress", "updated_at"])

        par_results, tpar_ms = _run_parallel(risk_items, worker_count=worker_count)
        job.progress = 85
        job.save(update_fields=["progress", "updated_at"])

        seq_index = sorted((r.risk_id, r.score, r.level) for r in seq_results)
        par_index = sorted((r.risk_id, r.score, r.level) for r in par_results)
        if seq_index != par_index:
            raise ValueError("Los resultados secuenciales y paralelos no coinciden")

        speedup = round((tseq_ms / tpar_ms), 3) if tpar_ms > 0 else None
        efficiency = round(speedup / worker_count, 3) if speedup and worker_count > 0 else None

        job.status = "SUCCESS"
        job.progress = 100
        job.completed_at = timezone.now()
        job.tseq_ms = round(tseq_ms, 3)
        job.tpar_ms = round(tpar_ms, 3)
        job.speedup = speedup
        job.result = {
            "workers": worker_count,
            "efficiency": efficiency,
            "summary": _build_summary(par_results),
        }
        job.save(
            update_fields=[
                "status",
                "progress",
                "completed_at",
                "tseq_ms",
                "tpar_ms",
                "speedup",
                "result",
                "updated_at",
            ]
        )
        return job
    except Exception as exc:
        job.status = "FAILED"
        job.completed_at = timezone.now()
        job.result = {"error": str(exc)}
        job.save(update_fields=["status", "completed_at", "result", "updated_at"])
        return job
