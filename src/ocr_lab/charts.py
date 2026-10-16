# pyright: reportUnknownMemberType=false
# Matplotlib exposes untyped **kwargs; model inputs remain validated and typed.
"""Descriptive plots of recorded observations; no fitted benchmark curves."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pydantic import BaseModel

from ocr_lab.domain import JSON
from ocr_lab.evaluation import NAMES

COLORS = ["#168c8c", "#6754ba", "#d57b32", "#316cb0"]


class ModelStats(BaseModel):
    name: str
    calls: int
    exact_images: int
    correct_fields: int
    total_fields: int
    mean_seconds: float
    projected_1000_usd: str


class Observation(BaseModel):
    model: str
    case_id: str
    exact: bool
    correct_fields: int
    total_fields: int
    seconds: float


class Snapshot(BaseModel):
    models: dict[str, ModelStats]
    results: list[Observation]


def canvas(width: float = 11, height: float = 5.8) -> tuple[Figure, Axes]:
    figure, axes = plt.subplots(figsize=(width, height), layout="constrained")
    axes.spines[["top", "right"]].set_visible(False)
    return figure, axes


def save(figure: Figure, root: Path, name: str) -> None:
    folder = root / "figures"
    folder.mkdir(exist_ok=True)
    for extension in ["png", "svg"]:
        figure.savefig(
            folder / f"{name}.{extension}",
            dpi=180,
            bbox_inches="tight",
            metadata={"Creator": "justino.dev"},
        )
    svg = folder / f"{name}.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(figure)


def accuracy(snapshot: Snapshot, root: Path) -> None:
    fig, ax = canvas()
    values = list(snapshot.models.values())
    ax.barh([v.name for v in values], [v.exact_images for v in values], color=COLORS)
    ax.set(
        xlim=(0, 10.8),
        xlabel="Completely correct images / 10",
        title="Whole-image exact match | one call per model and image",
    )
    for index, value in enumerate(values):
        ax.text(value.exact_images + 0.12, index, f"{value.exact_images}/10", va="center")
    save(fig, root, "exact-match")


def cost_quality(snapshot: Snapshot, root: Path) -> None:
    fig, ax = canvas()
    for (model, value), color in zip(snapshot.models.items(), COLORS, strict=True):
        ax.scatter(float(value.projected_1000_usd), value.exact_images, s=170, color=color)
        ax.annotate(
            NAMES[model],
            (float(value.projected_1000_usd), value.exact_images),
            xytext=(8, 12 if "gemini" in model or "luna" in model else -20),
            textcoords="offset points",
        )
    ax.set(
        xscale="log",
        ylim=(5.8, 10),
        xlim=(0.3, 15),
        xlabel="USD / 1,000 requests projected from this image mix (log scale)",
        ylabel="Completely correct images / 10",
        title="Observed cost and exactness | lower cost, higher exactness preferred",
    )
    ax.grid(alpha=0.15)
    save(fig, root, "cost-quality")


def heatmap(snapshot: Snapshot, root: Path) -> None:
    fig, ax = canvas(12, 4.5)
    rows = list(snapshot.models)
    lookup = {(r.model, r.case_id): r for r in snapshot.results}
    cases = [f"{i:02}" for i in range(1, 11)]
    values = [
        [lookup[(m, c)].correct_fields / lookup[(m, c)].total_fields for c in cases] for m in rows
    ]
    image = ax.imshow(values, cmap="YlGnBu", vmin=0, vmax=1, aspect="auto")
    ax.set(
        xticks=range(10),
        xticklabels=cases,
        yticks=range(len(rows)),
        yticklabels=[NAMES[m] for m in rows],
        xlabel="Case ID (see dataset card)",
        title="Field correctness by case | counts include routing and null fields",
    )
    for row, model in enumerate(rows):
        for column, case in enumerate(cases):
            r = lookup[(model, case)]
            ax.text(
                column,
                row,
                f"{r.correct_fields}/{r.total_fields}",
                ha="center",
                va="center",
                color="white" if values[row][column] > 0.7 else "black",
            )
    fig.colorbar(image, ax=ax, label="Fraction of fields correct")
    save(fig, root, "case-heatmap")


def latency(snapshot: Snapshot, root: Path) -> None:
    fig, ax = canvas()
    for (model, value), color in zip(snapshot.models.items(), COLORS, strict=True):
        times = sorted(r.seconds for r in snapshot.results if r.model == model)
        ax.step(
            [0.0, *times],
            [0.0, *[(i + 1) / len(times) for i in range(len(times))]],
            where="post",
            color=color,
            label=value.name,
            linewidth=2,
        )
    ax.set(
        xlabel="End-to-end request duration (seconds)",
        ylabel="Fraction of requests completed",
        ylim=(0, 1.05),
        title="Latency ECDF | 10 observations/model; four concurrent requests",
    )
    ax.grid(alpha=0.2)
    ax.legend(loc="lower right")
    save(fig, root, "latency-ecdf")


def cover(snapshot: Snapshot, root: Path) -> None:
    fig, ax = canvas(12, 5.5)
    fig.set_facecolor("#102536")
    ax.set_facecolor("#102536")
    ax.axis("off")
    ax.text(
        0.03,
        0.81,
        "VISION OCR LAB",
        color="white",
        fontsize=38,
        weight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.03,
        0.64,
        "A small, auditable experiment in structured extraction",
        color="#a9c7d7",
        fontsize=17,
        transform=ax.transAxes,
    )
    ax.text(
        0.03,
        0.46,
        "10 synthetic images  /  4 models  /  40 scored calls",
        color="#5bd6c5",
        fontsize=18,
        transform=ax.transAxes,
    )
    ax.text(
        0.03,
        0.29,
        "Gemini: 9/10 exact images, 153/154 fields",
        color="white",
        fontsize=20,
        transform=ax.transAxes,
    )
    ax.text(
        0.03,
        0.13,
        "Exploratory results, not a general OCR leaderboard.   •   justino.dev",
        color="#a9c7d7",
        fontsize=13,
        transform=ax.transAxes,
    )
    save(fig, root, "cover")


def render(report: dict[str, JSON], root: Path) -> None:
    snapshot = Snapshot.model_validate(report)
    for plot in [accuracy, cost_quality, heatmap, latency, cover]:
        plot(snapshot, root)
