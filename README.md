# Dask Multi-GPU Scaling Lab

用於評估 Dask-CUDA partition、排程、shuffle 與通訊成本的 scaling efficiency 工具。

## 執行

直接開啟 `index.html`，調整 GPU 數量、單卡基準、partition 和通訊占比。

## 實機延伸

使用 LocalCUDACluster、Dask Dashboard、RMM logging 與 UCX 量測替換模擬參數。

