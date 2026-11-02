"""Сводная таблица моделей из замеров benchmark.py (07-08_segformer_profiling/results/perf/summary_*.json).

Ускорение и Δ mIoU — относительно fp32 исходной модели той же архитектуры.
Запуск из корня репозитория: python scripts/summary_table.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERF = ROOT / "07-08_segformer_profiling" / "results" / "perf"
OUT = ROOT / "results"

# tag -> (модель, базовая модель для сравнения, сокращение, подзадача)
RUNS = [
    ("summary_deeplab", "DeepLabV3-R50", "deeplab", "—", "3"),
    ("summary_deeplab_r0.3_pruned", "DeepLabV3-R50", "deeplab", "r=0.3, без дообучения", "4"),
    ("summary_deeplab_r0.3_ft", "DeepLabV3-R50", "deeplab", "r=0.3 + 15 эпох", "4"),
    ("summary_deeplab_r0.5_pruned", "DeepLabV3-R50", "deeplab", "r=0.5, без дообучения", "4"),
    ("summary_deeplab_r0.5_ft", "DeepLabV3-R50", "deeplab", "r=0.5 + 15 эпох", "4"),
    ("summary_segformer", "SegFormer-B0", "segformer", "—", "7"),
]


def main():
    rows, base = [], {}
    for tag, model, arch, prune, task in RUNS:
        data = json.loads((PERF / f"{tag}.json").read_text())
        env = data["meta"]["env"]
        for r in data["rows"]:
            if "error" in r:
                continue
            lat = r["latency_b1"]["median_ms"]
            if prune == "—" and r["variant"] == "fp32":
                base[arch] = (lat, r["miou"])
            # сразу после прунинга важно только качество, скорость та же, что после дообучения
            if "без дообучения" in prune and r["variant"] != "fp32":
                continue
            mem = None if r["memory_b1_MB"] is None else r["weights_MB"] + r["memory_b1_MB"]
            rows.append(dict(task=task, model=model, arch=arch, prune=prune, variant=r["variant"],
                             miou=r["miou"], latency_ms=lat, p90_ms=r["latency_b1"]["p90_ms"],
                             memory_MB=mem, params_M=r["params_M"], gmacs=r["gmacs"]))
    for r in rows:
        b_lat, b_miou = base[r["arch"]]
        r["speedup"] = b_lat / r["latency_ms"]
        r["delta_miou"] = round(r["miou"] - b_miou, 4) + 0.0

    OUT.mkdir(exist_ok=True)
    with open(OUT / "summary_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[k for k in rows[0] if k != "arch"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    head = ["Подзадача", "Модель", "Прунинг", "Точность", "mIoU test", "Δ mIoU",
            "Задержка b=1, мс (медиана / p90)", "Ускорение", "Память b=1, МБ", "Параметры, млн", "GMACs"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        lines.append("| " + " | ".join([
            r["task"], r["model"], r["prune"], r["variant"], f"{r['miou']:.4f}", f"{r['delta_miou']:+.4f}",
            f"{r['latency_ms']:.2f} / {r['p90_ms']:.2f}", f"×{r['speedup']:.2f}",
            "—" if r["memory_MB"] is None else f"{r['memory_MB']:.0f}",
            f"{r['params_M']:.2f}", f"{r['gmacs']:.1f}",
        ]) + " |")
    note = (f"\n{env['gpu']}, torch {env['torch']}, CUDA {env['cuda']}. Вход 360×480, batch 1, "
            "30 прогревочных + 200 замеренных проходов, CUDA events и synchronize на каждой итерации. "
            "Память — веса + пиковый прирост за проход; для fp16+compile (CUDA Graphs) не измеряется. "
            "Ускорение и Δ mIoU — к fp32 исходной модели той же архитектуры.\n")
    (OUT / "summary_table.md").write_text("\n".join(lines) + "\n" + note)
    print("\n".join(lines) + "\n" + note)


if __name__ == "__main__":
    main()
