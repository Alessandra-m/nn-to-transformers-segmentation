| Model | Input | Variant | mIoU test | Δ mIoU | Latency b=1, ms (median / p90) | Speedup | FPS, b=8 | Memory b=1, MB (weights + activations) | Params, M | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| DeepLabV3-ResNet50 | 360x480 | fp32 | 0.0742 | +0.0000 | 13.80 / 13.81 | ×1.00 | 81.8 | 75 (38 + 37) | 9.93 | 27.1 |
| DeepLabV3-ResNet50 | 360x480 | fp16 | 0.0742 | -0.0000 | 8.34 / 8.36 | ×1.65 | 147.7 | 58 (38 + 20) | 9.93 | 27.1 |
| DeepLabV3-ResNet50 | 360x480 | half | 0.0744 | +0.0002 | 7.86 / 7.87 | ×1.76 | 150.4 | 37 (19 + 18) | 9.93 | 27.1 |
| DeepLabV3-ResNet50 | 360x480 | fp16+compile | 0.0742 | -0.0000 | 5.14 / 5.15 | ×2.68 | 194.6 | — | 9.93 | 27.1 |
