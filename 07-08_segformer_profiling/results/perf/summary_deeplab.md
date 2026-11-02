| Model | Input | Variant | mIoU test | Δ mIoU | Latency b=1, ms (median / p90) | Speedup | FPS, b=8 | Memory b=1, MB (weights + activations) | Params, M | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| DeepLabV3-ResNet50 | 360x480 | fp32 | 0.6952 | +0.0000 | 38.02 / 38.53 | ×1.00 | 27.7 | 228 (151 + 77) | 39.64 | 107.8 |
| DeepLabV3-ResNet50 | 360x480 | fp16 | 0.6952 | -0.0000 | 21.82 / 21.83 | ×1.74 | 54.0 | 197 (151 + 46) | 39.64 | 107.8 |
| DeepLabV3-ResNet50 | 360x480 | half | 0.6951 | -0.0001 | 20.73 / 20.74 | ×1.83 | 54.7 | 114 (76 + 38) | 39.64 | 107.8 |
| DeepLabV3-ResNet50 | 360x480 | fp16+compile | 0.6952 | -0.0000 | 15.82 / 16.05 | ×2.40 | 65.0 | — | 39.64 | 107.8 |
