| Model | Input | Variant | mIoU test | Δ mIoU | Latency b=1, ms (median / p90) | Speedup | FPS, b=8 | Memory b=1, MB (weights + activations) | Params, M | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| DeepLabV3-ResNet50 | 360x480 | fp32 | 0.6565 | +0.0000 | 13.76 / 13.77 | ×1.00 | 82.0 | 75 (38 + 37) | 9.93 | 27.1 |
| DeepLabV3-ResNet50 | 360x480 | fp16 | 0.6565 | -0.0001 | 8.28 / 8.30 | ×1.66 | 148.2 | 58 (38 + 20) | 9.93 | 27.1 |
| DeepLabV3-ResNet50 | 360x480 | half | 0.6565 | -0.0001 | 7.82 / 7.84 | ×1.76 | 150.4 | 37 (19 + 18) | 9.93 | 27.1 |
| DeepLabV3-ResNet50 | 360x480 | fp16+compile | 0.6565 | -0.0001 | 5.13 / 5.17 | ×2.68 | 192.7 | — | 9.93 | 27.1 |
