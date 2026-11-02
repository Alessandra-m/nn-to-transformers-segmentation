# CV: от свёрточных сетей к трансформерам

Устройство свёрточных и трансформерных моделей компьютерного зрения, их адаптация к новым данным
и первые эксперименты по оптимизации. Подзадачи 1–8 выполнены последовательно. Все эксперименты
с обучением и замерами (3, 4, 7, 8) идут на одном датасете — **CamVid** с фиксированным разбиением
367 / 101 / 233 ([data/README.md](data/README.md)).

## Подзадачи

| # | Тема | Конспект статьи | Папка | Отчёт | Главный результат |
|---|---|---|---|---|---|
| 1 | FCN | [Long et al., 2015](papers/01_fcn.md) | [01_fcn](01_fcn/) | [README](01_fcn/README.md) | FCN и FCN-skip на PyTorch, размеры тензоров для двух входов, выход `[B, C, H, W]` |
| 2 | U-Net | [Ronneberger et al., 2015](papers/02_unet.md) | [02_unet](02_unet/) | [README](02_unet/README.md) | компактная U-Net (482 тыс. параметров), переобучение до IoU 1.00 на train |
| 3 | Дообучение | [D2L, Fine-Tuning](papers/03_fine_tuning.md) | [03-04_deeplab_finetune_pruning](03-04_deeplab_finetune_pruning/) | [REPORT_Fine-Tuning](03-04_deeplab_finetune_pruning/reports/REPORT_Fine-Tuning.md) | DeepLabV3-R50: голова 0.596 → вся модель 0.685 → CE + Lovász **0.695** mIoU test |
| 4 | Прунинг | [DepGraph, Torch-Pruning](papers/04_depgraph.md) | там же | [REPORT_Pruning](03-04_deeplab_finetune_pruning/reports/REPORT_Pruning.md) | r = 0.3: ×1.7 быстрее при −0.014 mIoU; r = 0.5: ×2.8 при −0.038 |
| 5 | Transformer encoder | [Vaswani et al., 2017](papers/05_transformer.md) | [05-06_transformer_vit](05-06_transformer_vit/) | [transformer_encoder](05-06_transformer_vit/report/transformer_encoder.md) | attention, совпадающий со встроенным, encoder-блок, стоимость O(N²) |
| 6 | ViT | [Dosovitskiy et al., 2020](papers/06_vit.md) | там же | [vit](05-06_transformer_vit/report/vit.md) | patch embedding, учебный ViT, предобученный ViT-B/16, число токенов |
| 7 | SegFormer | [Xie et al., 2021](papers/07_segformer.md) | [07-08_segformer_profiling](07-08_segformer_profiling/) | [README](07-08_segformer_profiling/README.md) | SegFormer-B0: **0.691** mIoU test при 3.7 млн параметров (в 10.7 раза меньше DeepLabV3) |
| 8 | Профилирование и оптимизация | [PyTorch Profiler](papers/08_profiler.md) | там же | [PROFILING](07-08_segformer_profiling/PROFILING.md) | `fp16+compile`: SegFormer ×2.1, DeepLabV3 ×2.4 без потери mIoU |

Конспекты статей в едином формате (проблема → предложение → устройство метода → ограничения)
собраны в [papers/](papers/README.md).

## Сводная таблица моделей

| Подзадача | Модель | Прунинг | Точность | mIoU test | Δ mIoU | Задержка b=1, мс (медиана / p90) | Ускорение | Память b=1, МБ | Параметры, млн | GMACs |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | DeepLabV3-R50 | — | fp32 | 0.6952 | +0.0000 | 38.02 / 38.53 | ×1.00 | 228 | 39.64 | 107.8 |
| 3 | DeepLabV3-R50 | — | fp16 | 0.6952 | +0.0000 | 21.82 / 21.83 | ×1.74 | 197 | 39.64 | 107.8 |
| 3 | DeepLabV3-R50 | — | half | 0.6951 | -0.0001 | 20.73 / 20.74 | ×1.83 | 114 | 39.64 | 107.8 |
| 3 | DeepLabV3-R50 | — | fp16+compile | 0.6952 | +0.0000 | 15.82 / 16.05 | ×2.40 | — | 39.64 | 107.8 |
| 4 | DeepLabV3-R50 | r=0.3, без дообучения | fp32 | 0.0759 | -0.6193 | 22.89 / 22.90 | ×1.66 | 124 | 18.95 | 51.4 |
| 4 | DeepLabV3-R50 | r=0.3 + 15 эпох | fp32 | 0.6811 | -0.0141 | 22.80 / 22.82 | ×1.67 | 124 | 18.95 | 51.4 |
| 4 | DeepLabV3-R50 | r=0.3 + 15 эпох | fp16 | 0.6811 | -0.0141 | 13.65 / 13.66 | ×2.78 | 102 | 18.95 | 51.4 |
| 4 | DeepLabV3-R50 | r=0.3 + 15 эпох | half | 0.6811 | -0.0141 | 13.09 / 13.10 | ×2.90 | 63 | 18.95 | 51.4 |
| 4 | DeepLabV3-R50 | r=0.3 + 15 эпох | fp16+compile | 0.6811 | -0.0141 | 9.73 / 9.89 | ×3.91 | — | 18.95 | 51.4 |
| 4 | DeepLabV3-R50 | r=0.5, без дообучения | fp32 | 0.0742 | -0.6210 | 13.80 / 13.81 | ×2.76 | 75 | 9.93 | 27.1 |
| 4 | DeepLabV3-R50 | r=0.5 + 15 эпох | fp32 | 0.6565 | -0.0386 | 13.76 / 13.77 | ×2.76 | 75 | 9.93 | 27.1 |
| 4 | DeepLabV3-R50 | r=0.5 + 15 эпох | fp16 | 0.6565 | -0.0387 | 8.28 / 8.30 | ×4.59 | 58 | 9.93 | 27.1 |
| 4 | DeepLabV3-R50 | r=0.5 + 15 эпох | half | 0.6565 | -0.0387 | 7.82 / 7.84 | ×4.86 | 37 | 9.93 | 27.1 |
| 4 | DeepLabV3-R50 | r=0.5 + 15 эпох | fp16+compile | 0.6565 | -0.0387 | 5.13 / 5.17 | ×7.41 | — | 9.93 | 27.1 |
| 7 | SegFormer-B0 | — | fp32 | 0.6912 | +0.0000 | 7.32 / 7.40 | ×1.00 | 112 | 3.72 | 4.9 |
| 7 | SegFormer-B0 | — | fp16 | 0.6912 | +0.0000 | 7.84 / 7.97 | ×0.93 | 129 | 3.72 | 4.9 |
| 7 | SegFormer-B0 | — | half | 0.6913 | +0.0000 | 5.68 / 5.94 | ×1.29 | 57 | 3.72 | 4.9 |
| 7 | SegFormer-B0 | — | fp16+compile | 0.6912 | +0.0000 | 3.38 / 3.86 | ×2.17 | — | 3.72 | 4.9 |

NVIDIA GeForce RTX 3050, torch 2.14.1+cu130, CUDA 13.0. Вход 360×480, batch 1, 30 прогревочных + 200 замеренных проходов, CUDA events и synchronize на каждой итерации. Память — веса + пиковый прирост за проход; для fp16+compile (CUDA Graphs) не измеряется. Ускорение и Δ mIoU — к fp32 исходной модели той же архитектуры.

**Выводы из таблицы**
- **Качество.** SegFormer-B0 почти догоняет DeepLabV3-R50 (0.691 против 0.695 mIoU) при
  в 10.7 раза меньшем числе параметров и в 22 раза меньших вычислениях.
- **Пониженная точность — бесплатное ускорение** для обеих архитектур: Δ mIoU ≤ 0.0001.
  Но `autocast` fp16 замедляет SegFormer (×0.93): модель ограничена запусками ядер, а не
  вычислениями. Помогает только `fp16+compile` (CUDA Graphs): ×2.17.
- **Прунинг и пониженная точность складываются.** DeepLabV3 r = 0.5 в `fp16+compile` даёт
  5.1 мс (×7.4 к исходной fp32) при −0.039 mIoU. Это быстрее SegFormer-B0 в `half` (5.7 мс),
  но медленнее его `fp16+compile` (3.4 мс), и SegFormer точнее на 0.035.
- **Сразу после прунинга модель не работает** (mIoU 0.07): нужны 15 эпох дообучения (3–4 мин).
- **Лучший компромисс:** SegFormer-B0 `fp16+compile` — 3.4 мс и 0.691 mIoU.

Таблица собирается из замеров `07-08_segformer_profiling/results/perf/summary_*.json`
([CSV](results/summary_table.csv)), все модели — одним скриптом в одном сеансе:

```bash
cd 07-08_segformer_profiling
V="fp32 fp16 half fp16+compile"; R=../03-04_deeplab_finetune_pruning/runs
python benchmark.py --miou --variants $V --models segformer --tag summary_segformer
python benchmark.py --miou --variants $V --models deeplab --tag summary_deeplab
python benchmark.py --miou --variants $V --models deeplab --tag summary_deeplab_r0.3_pruned \
    --deeplab-ckpt $R/full_ce_lovasz_e50_prune_l2_r0.3/pruned.pt
python benchmark.py --miou --variants $V --models deeplab --tag summary_deeplab_r0.3_ft \
    --deeplab-ckpt $R/full_ce_lovasz_e50_prune_l2_r0.3_ft_ce_lovasz_e15/best_model.pt
# r0.5 — аналогично
cd .. && python scripts/summary_table.py
```

## Быстрый старт

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
git clone https://github.com/stonewst/CamVid-for-Segmentation.git data/CamVid
```

Подзадачи 1, 2, 5, 6 не требуют данных и весов:

```bash
cd 01_fcn && python fcn.py && python fcn_skip.py && python compare.py
cd 02_unet && python u_net.py
cd 05-06_transformer_vit && python transformer_encoder.py && python vit_model.py && python vit_pretrained.py
```

Подзадача 7 — предсказание готовыми весами (`weights/segformer-b0-camvid` лежат в репозитории):

```bash
cd 07-08_segformer_profiling
python predict.py ../data/CamVid/test/0001TP_008550.png pred.png --model weights/segformer-b0-camvid
```

Обучение, прунинг и профилирование — в README каждой папки. Чекпоинты DeepLabV3 (`*.pt`,
40–160 МБ) в git не хранятся и воспроизводятся `train.py` и `prune.py` за 3–20 минут на RTX 3050.

## Окружение

NVIDIA GeForce RTX 3050 8 ГБ, Python 3.14, torch 2.14.1 + CUDA 13.0, transformers 5.22.1,
torch-pruning 1.6.1. История коммитов каждой подзадачи сохранена (`git log -- <папка>`).
