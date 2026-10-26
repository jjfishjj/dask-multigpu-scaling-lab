"""Model multi-GPU scaling efficiency and identify the dominant bottleneck."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ScalingResult:
    workers: int
    single_worker_seconds: float
    distributed_seconds: float
    speedup: float
    efficiency_pct: float
    diagnosis: str


def evaluate(workers: int, single_worker_seconds: float, distributed_seconds: float) -> ScalingResult:
    if workers <= 0 or single_worker_seconds <= 0 or distributed_seconds <= 0:
        raise ValueError("workers and timings must be positive")
    speedup = single_worker_seconds / distributed_seconds
    efficiency = speedup / workers * 100
    diagnosis = "healthy" if efficiency >= 70 else "inspect communication and partitioning" if efficiency >= 45 else "communication or scheduler bound"
    return ScalingResult(workers, single_worker_seconds, distributed_seconds, round(speedup, 3), round(efficiency, 2), diagnosis)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("--single-seconds", type=float, required=True)
    parser.add_argument("--distributed-seconds", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(asdict(evaluate(args.workers, args.single_seconds, args.distributed_seconds)), indent=2))


if __name__ == "__main__":
    main()
