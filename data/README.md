# Данные: CamVid

Один датасет для всех экспериментов с обучением (подзадачи 3, 4, 7, 8) с фиксированным разбиением
**367 train / 101 val / 233 test**, 11 классов + `unlabelled` (игнорируется в loss и mIoU),
кадры 360×480.

```bash
git clone https://github.com/stonewst/CamVid-for-Segmentation.git data/CamVid
```

```
data/CamVid/
├── class_palette.csv       # name,r,g,b для 11 классов + unlabelled
├── train/  trainannot/     # 367 кадров
├── val/    valannot/       # 101 кадр
└── test/   testannot/      # 233 кадра
```

Маска `<stem>_L.png` — RGB, цвет кодирует класс. Оба загрузчика
(`03-04_deeplab_finetune_pruning/camvid.py` и `07-08_segformer_profiling/camvid_dataset.py`)
переводят её в индексы по `class_palette.csv`. Это то же разбиение и та же разметка, что
CamVid из [SegNet-Tutorial](https://github.com/alexgkendall/SegNet-Tutorial/tree/master/CamVid)
(там маски уже индексные), его `camvid.py` тоже читает.

Выбор эпохи — по val, итоговые числа — test в исходном разрешении 360×480.
