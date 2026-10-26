"""Execute a real Dask-CUDA workload and report observed scaling inputs."""

from __future__ import annotations

import argparse
import json
import time

import cupy as cp
import dask.array as da
from dask.distributed import Client, wait
from dask_cuda import LocalCUDACluster


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--elements", type=int, default=100_000_000)
    parser.add_argument("--chunk-size", type=int, default=5_000_000)
    parser.add_argument("--rmm-pool-size", default="2GB")
    args = parser.parse_args()
    cluster = LocalCUDACluster(n_workers=args.workers, rmm_pool_size=args.rmm_pool_size, protocol="ucx")
    with Client(cluster) as client:
        started = time.perf_counter()
        values = da.random.random(args.elements, chunks=args.chunk_size).map_blocks(cp.asarray, dtype=float)
        result = values.mean().persist()
        wait(result)
        mean = float(result.compute())
        elapsed = time.perf_counter() - started
        print(json.dumps({"workers": len(client.scheduler_info()["workers"]), "elements": args.elements, "chunk_size": args.chunk_size, "mean": mean, "elapsed_seconds": round(elapsed, 3)}, indent=2))


if __name__ == "__main__":
    main()
