| Model | Input | Variant | mIoU test | Δ mIoU | Latency b=1, ms (median / p90) | Speedup | FPS, b=8 | Memory b=1, MB (weights + activations) | Params, M | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| DeepLabV3-ResNet50 | 360x480 | fp32 | 0.6811 | +0.0000 | 22.80 / 22.82 | ×1.00 | 47.0 | 124 (72 + 52) | 18.95 | 51.4 |
| DeepLabV3-ResNet50 | 360x480 | fp16 | 0.6811 | +0.0000 | 13.65 / 13.66 | ×1.67 | 86.6 | 102 (72 + 29) | 18.95 | 51.4 |
| DeepLabV3-ResNet50 | 360x480 | half | 0.6811 | -0.0000 | 13.09 / 13.10 | ×1.74 | 87.7 | 63 (36 + 27) | 18.95 | 51.4 |
| DeepLabV3-ResNet50 | 360x480 | fp16+compile | 0.6811 | -0.0000 | 9.73 / 9.89 | ×2.34 | 105.8 | — | 18.95 | 51.4 |
