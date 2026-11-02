# Конспекты статей

Каждый конспект — около страницы в одном формате: **проблема → что предлагают авторы → как
устроен метод → ограничения**, плюс короткий раздел «что проверено у нас» со ссылками на код и
результаты. Подробные разборы, код и эксперименты — в отчётах подзадач.

| # | Материал | Конспект | Ключевая идея |
|---|---|---|---|
| 1 | Long et al. *Fully Convolutional Networks for Semantic Segmentation*, CVPR 2015 | [01_fcn](01_fcn.md) | классификатор → полностью свёрточная сеть, транспонированная свёртка, skip-связи |
| 2 | Ronneberger et al. *U-Net*, MICCAI 2015 | [02_unet](02_unet.md) | симметричный encoder–decoder, конкатенация признаков на каждом уровне |
| 3 | Zhang et al. *Dive into Deep Learning*, Fine-Tuning | [03_fine_tuning](03_fine_tuning.md) | перенос предобученных весов, новый выходной слой, разные скорости обучения |
| 4 | Fang et al. *DepGraph: Towards Any Structural Pruning*, CVPR 2023 | [04_depgraph](04_depgraph.md) | граф зависимостей и групповое удаление каналов |
| 5 | Vaswani et al. *Attention Is All You Need*, NeurIPS 2017 | [05_transformer](05_transformer.md) | scaled dot-product и multi-head attention, encoder-блок |
| 6 | Dosovitskiy et al. *An Image is Worth 16×16 Words*, ICLR 2021 | [06_vit](06_vit.md) | изображение как последовательность патчей для стандартного трансформера |
| 7 | Xie et al. *SegFormer*, NeurIPS 2021 | [07_segformer](07_segformer.md) | иерархический энкодер без позиционных эмбеддингов и All-MLP-декодер |
| 8 | PyTorch Profiler | [08_profiler](08_profiler.md) | выбор оптимизации по измерениям: что ограничивает модель |

Линия развития: FCN (1) задаёт плотное предсказание свёрточной сетью → U-Net (2) точнее
восстанавливает детали → дообучение (3) и прунинг (4) адаптируют и сжимают готовую CNN →
attention (5) и ViT (6) переносят трансформер на изображения → SegFormer (7) делает его
пригодным для сегментации → профилирование (8) сравнивает CNN и трансформер на реальном железе.
