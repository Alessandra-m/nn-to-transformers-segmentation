| Model | Input | Variant | mIoU test | Δ mIoU | Latency b=1, ms (median / p90) | Speedup | FPS, b=8 | Memory b=1, MB (weights + activations) | Params, M | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| DeepLabV3-ResNet50 | 360x480 | fp32 | 0.0759 | +0.0000 | 22.89 / 22.90 | ×1.00 | 47.0 | 124 (72 + 52) | 18.95 | 51.4 |
| DeepLabV3-ResNet50 | 360x480 | fp16 | 0.0759 | +0.0000 | 13.65 / 13.66 | ×1.68 | 86.5 | 102 (72 + 29) | 18.95 | 51.4 |
| DeepLabV3-ResNet50 | 360x480 | half | 0.0757 | -0.0002 | 13.09 / 13.10 | ×1.75 | 87.9 | 63 (36 + 27) | 18.95 | 51.4 |
| DeepLabV3-ResNet50 | 360x480 | fp16+compile | 0.0759 | -0.0000 | 9.63 / 9.74 | ×2.38 | 106.2 | — | 18.95 | 51.4 |
