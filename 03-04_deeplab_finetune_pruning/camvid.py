from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import tv_tensors
from torchvision.io import ImageReadMode, read_image
from torchvision.transforms import v2

DATA_ROOT = Path(__file__).resolve().parent.parent / "data" / "CamVid"

CLASSES = ["Sky", "Building", "Pole", "Road", "Pavement", "Tree",
           "SignSymbol", "Fence", "Car", "Pedestrian", "Bicyclist"]
NUM_CLASSES = len(CLASSES)      # 11
IGNORE_INDEX = 11               

PALETTE = [(128, 128, 128), (128, 0, 0), (192, 192, 128), (128, 64, 128),
           (60, 40, 222), (128, 128, 0), (192, 128, 128), (64, 64, 128),
           (64, 0, 128), (64, 64, 0), (0, 128, 192), (0, 0, 0)]

MEAN = [0.485, 0.456, 0.406]    
STD = [0.229, 0.224, 0.225]

TRAIN_CROP = (352, 480)        


def get_transforms(train):
    to_float = v2.ToDtype({tv_tensors.Image: torch.float32,
                           tv_tensors.Mask: torch.int64}, scale=True)
    if not train:
        return v2.Compose([to_float, v2.Normalize(MEAN, STD)])

    return v2.Compose([
        v2.RandomResizedCrop(TRAIN_CROP, scale=(0.5, 1.0), ratio=(1.2, 1.5), antialias=True),
        v2.RandomHorizontalFlip(p=0.5),
        v2.RandomApply([v2.RandomAffine(degrees=10, fill={tv_tensors.Image: 0,
                                                          tv_tensors.Mask: IGNORE_INDEX})], p=0.3),
        v2.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3),
        to_float,
        v2.Normalize(MEAN, STD),
    ])


def denorm(img):
    img = img * torch.tensor(STD)[:, None, None] + torch.tensor(MEAN)[:, None, None]
    return (img.clamp(0, 1).permute(1, 2, 0).numpy() * 255).astype(np.uint8)


class CamVid(Dataset):
    def __init__(self, root=DATA_ROOT, split="train", transforms=None):
        root = Path(root)
        self.images = sorted((root / split).glob("*.png"))
        self.masks = sorted((root / f"{split}annot").glob("*.png"))
        assert len(self.images) > 0, f"нет изображений в {root / split}"
        # маски: индексы классов с тем же именем (SegNet-Tutorial) или RGB-цвета с суффиксом _L
        names = [p.name.replace("_L.png", ".png") for p in self.masks]
        assert [p.name for p in self.images] == names, \
            f"{split}: имена картинок и масок не совпадают"
        self.colors = None
        if (root / "class_palette.csv").exists():
            rows = np.loadtxt(root / "class_palette.csv", delimiter=",", skiprows=1,
                              usecols=(1, 2, 3), dtype=np.int64)[:NUM_CLASSES]
            self.colors = torch.from_numpy((rows[:, 0] << 16) | (rows[:, 1] << 8) | rows[:, 2])
        self.transforms = transforms

    def read_mask(self, path):
        m = read_image(str(path), ImageReadMode.UNCHANGED)
        if m.shape[0] == 1:
            return m[0]
        code = (m[0].long() << 16) | (m[1].long() << 8) | m[2].long()
        mask = torch.full(code.shape, IGNORE_INDEX, dtype=torch.uint8)
        for i, c in enumerate(self.colors):
            mask[code == c] = i
        return mask

    def __len__(self):
        return len(self.images)

    def __getitem__(self, i):
        img = tv_tensors.Image(read_image(str(self.images[i]), ImageReadMode.RGB))
        mask = tv_tensors.Mask(self.read_mask(self.masks[i]))
        if self.transforms is not None:
            img, mask = self.transforms(img, mask)
        return img, mask


def make_loader(split, batch_size=4, num_workers=4, root=DATA_ROOT):
    ds = CamVid(root, split, get_transforms(train=False))
    return DataLoader(ds, batch_size=batch_size, shuffle=False,
                      num_workers=num_workers, pin_memory=True)


def get_loaders(batch_size=4, num_workers=4, root=DATA_ROOT):
    train_ds = CamVid(root, "train", get_transforms(train=True))
    val_ds = CamVid(root, "val", get_transforms(train=False))
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                          num_workers=num_workers, pin_memory=True,
                          drop_last=True, persistent_workers=num_workers > 0)
    val_dl = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                        num_workers=num_workers, pin_memory=True,
                        persistent_workers=num_workers > 0)
    return train_dl, val_dl
