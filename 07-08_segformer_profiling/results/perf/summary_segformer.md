| Model | Input | Variant | mIoU test | Δ mIoU | Latency b=1, ms (median / p90) | Speedup | FPS, b=8 | Memory b=1, MB (weights + activations) | Params, M | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| SegFormer-B0 | 360x480 | fp32 | 0.6912 | +0.0000 | 7.32 / 7.40 | ×1.00 | 170.8 | 112 (14 + 97) | 3.72 | 4.9 |
| SegFormer-B0 | 360x480 | fp16 | 0.6912 | +0.0000 | 7.84 / 7.97 | ×0.93 | 232.4 | 129 (14 + 115) | 3.72 | 4.9 |
| SegFormer-B0 | 360x480 | half | 0.6913 | +0.0000 | 5.68 / 5.94 | ×1.29 | 321.3 | 57 (7 + 50) | 3.72 | 4.9 |
| SegFormer-B0 | 360x480 | fp16+compile | 0.6912 | +0.0000 | 3.38 / 3.86 | ×2.17 | 314.2 | — | 3.72 | 4.9 |
