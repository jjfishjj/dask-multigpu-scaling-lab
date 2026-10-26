# Dask Multi-GPU Scaling Lab

提供可測試的 scaling-efficiency 分析器與真實 Dask-CUDA／CuPy 工作負載，分開觀察單卡時間、分散式時間、worker 數與 partition 大小。

## 快速驗證

```bash
python -m unittest discover -s tests -v
python src/scaling_model.py --workers 4 --single-seconds 100 --distributed-seconds 30
```

## NVIDIA 多 GPU 實機

在支援版本的 CUDA／RAPIDS 環境安裝 `requirements-gpu.txt`：

```bash
python src/run_dask_gpu.py --workers 4 --elements 100000000 --chunk-size 5000000
```

程式建立 `LocalCUDACluster`、以 RMM pool 配置記憶體並透過 UCX 執行；輸出 worker、資料量、chunk 與耗時 JSON。自架 GPU Runner 可手動執行 `gpu.yml`。

## 驗收重點

以同一資料量先量單卡，再逐步增加 GPU；同時觀察 Dask Dashboard、spill、task graph、UCX transport 與 NCCL／網路結果，避免把 partition 過小造成的 scheduler overhead 誤判成 GPU 不夠快。

