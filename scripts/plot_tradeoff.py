"""График «задержка — mIoU» по сводной таблице (results/summary_table.csv).

Модели без дообучения после прунинга (mIoU ≈ 0.07) не показаны: они сжали бы ось.
Запуск из корня репозитория: python scripts/plot_tradeoff.py
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import NullFormatter

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
SERIES = [  # (подпись, модель, прунинг, цвет)
    ("DeepLabV3-R50", "DeepLabV3-R50", "—", "#2a78d6"),
    ("DeepLabV3-R50, прунинг r=0.3", "DeepLabV3-R50", "r=0.3 + 15 эпох", "#eb6834"),
    ("DeepLabV3-R50, прунинг r=0.5", "DeepLabV3-R50", "r=0.5 + 15 эпох", "#1baf7a"),
    ("SegFormer-B0", "SegFormer-B0", "—", "#eda100"),
]
MARKERS = {"fp32": "o", "fp16": "s", "half": "^", "fp16+compile": "D"}


def main():
    rows = list(csv.DictReader(open(RES / "summary_table.csv")))
    plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2})
    fig, ax = plt.subplots(figsize=(8.5, 5), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)

    for label, model, prune, color in SERIES:
        pts = sorted((float(r["latency_ms"]), float(r["miou"]), r["variant"]) for r in rows
                     if r["model"] == model and r["prune"] == prune)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=2, zorder=2)
        for x, y, v in pts:
            ax.scatter(x, y, s=64, marker=MARKERS[v], color=color, edgecolors=SURFACE,
                       linewidths=2, zorder=3)
        x, y, _ = pts[-1]  # подпись у самой медленной точки
        ax.annotate(label, (x, y), xytext=(8, 0), textcoords="offset points", va="center",
                    fontsize=9, color=INK)

    ax.set_xscale("log")
    ax.set_xticks([3, 5, 10, 20, 40])
    ax.set_xticklabels(["3", "5", "10", "20", "40"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(2.8, 75)
    ax.set_xlabel("Задержка, мс (batch 1, 360×480, RTX 3050), лог. шкала")
    ax.set_ylabel("mIoU test")
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.set_title("Качество и задержка: модели и режимы точности", loc="left", fontsize=12, color=INK)

    handles = [Line2D([], [], marker=m, ls="", color=INK2, markersize=7, label=v)
               for v, m in MARKERS.items()]
    ax.legend(handles=handles, title="Точность", loc="lower right", frameon=False, fontsize=9,
              title_fontsize=9)
    fig.tight_layout()
    fig.savefig(RES / "miou_vs_latency.png", dpi=150, facecolor=SURFACE)
    print("saved", RES / "miou_vs_latency.png")


if __name__ == "__main__":
    main()
