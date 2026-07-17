#!/usr/bin/env python3
"""Generate ``images/fig_stall_exp016.pdf`` from the Exp016 evaluation.

The embedded values are the ``final_distance`` entries of the 22 unsuccessful
episodes in:

``rl_uav_aerostack2/runs/eval/exp016_final_100ep/episodes.csv``

Embedding the verified sample keeps the thesis repository self-contained.  If
the source CSV is available, the script validates episode identity, terminal
reason, step count, and every distance before producing the figure.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np


SUCCESS_THRESHOLD_M = 0.4
BIN_WIDTH_M = 0.1

# (episode_index, final_distance) in the order recorded by episodes.csv.
FAILED_EPISODES = (
    (2, 0.9073886714807049),
    (6, 0.7048111395830257),
    (7, 0.6676978698700409),
    (17, 0.5272511140526436),
    (22, 0.8256618828912791),
    (25, 1.1051679484869648),
    (26, 0.8154286029524261),
    (27, 0.8556121251670296),
    (29, 0.7469500927451749),
    (30, 1.1183863952860729),
    (34, 0.6456565606764457),
    (40, 0.4197757669984775),
    (45, 0.9512690243672473),
    (52, 1.0798360980976636),
    (59, 0.9419427285414653),
    (63, 0.6244561486074726),
    (69, 1.0638846189625788),
    (78, 0.8590866687545196),
    (81, 0.6902535560367093),
    (84, 0.5876874514070077),
    (96, 0.5206763098580175),
    (98, 0.6709390928133924),
)

DEFAULT_SOURCE_CSV = Path(
    "/home/jordi/TFM/rl_uav_aerostack2/"
    "runs/eval/exp016_final_100ep/episodes.csv"
)
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "images/fig_stall_exp016.pdf"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-csv", type=Path, default=DEFAULT_SOURCE_CSV)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--require-source",
        action="store_true",
        help="fail instead of using the embedded sample when the CSV is absent",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate data and bin counts without writing the PDF",
    )
    return parser.parse_args()


def validate_source(source_csv: Path, *, required: bool) -> None:
    if not source_csv.is_file():
        if required:
            raise FileNotFoundError(f"source CSV not found: {source_csv}")
        print(
            f"warning: source CSV not found; using verified embedded sample: {source_csv}",
            file=sys.stderr,
        )
        return

    with source_csv.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    failures = [row for row in rows if row["success"].strip().lower() == "false"]
    actual = tuple(
        (int(row["episode_index"]), float(row["final_distance"])) for row in failures
    )
    expected_ids = tuple(episode_id for episode_id, _ in FAILED_EPISODES)
    actual_ids = tuple(episode_id for episode_id, _ in actual)

    if len(rows) != 100:
        raise ValueError(f"expected 100 episodes, found {len(rows)}")
    if actual_ids != expected_ids:
        raise ValueError(f"failure episode IDs differ: {actual_ids} != {expected_ids}")
    if not np.array_equal(
        np.asarray([distance for _, distance in actual]),
        np.asarray([distance for _, distance in FAILED_EPISODES]),
    ):
        raise ValueError("embedded final_distance values differ from the source CSV")
    if any(row["terminal_reason"] != "max_steps" for row in failures):
        raise ValueError("not all failed episodes terminated because of max_steps")
    if any(int(row["steps"]) != 200 for row in failures):
        raise ValueError("not all failed episodes reached 200 steps")


def histogram_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    distances = np.asarray([distance for _, distance in FAILED_EPISODES])
    excesses = distances - SUCCESS_THRESHOLD_M
    edges = np.arange(0.0, 0.8 + BIN_WIDTH_M / 2, BIN_WIDTH_M)
    counts, _ = np.histogram(excesses, bins=edges)

    if len(excesses) != 22 or int(counts.sum()) != 22:
        raise AssertionError("the histogram must contain exactly the 22 failed episodes")
    if not np.array_equal(counts, np.asarray([1, 3, 5, 2, 4, 3, 2, 2])):
        raise AssertionError(f"unexpected histogram counts: {counts.tolist()}")
    return excesses, edges, counts


def decimal_comma(value: float, _position: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def generate_figure(output: Path, edges: np.ndarray, counts: np.ndarray) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 9.5,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2), constrained_layout=True)
    widths = np.diff(edges)
    bars = ax.bar(
        edges[:-1],
        counts,
        width=widths,
        align="edge",
        color="#E67E22",
        edgecolor="white",
        linewidth=0.9,
        zorder=3,
    )

    ax.axvline(0.0, color="#4D4D4D", linestyle="--", linewidth=1.2, zorder=4)
    ax.text(
        0.008,
        5.58,
        "umbral de éxito",
        color="#4D4D4D",
        fontsize=8,
        ha="left",
        va="top",
    )
    ax.bar_label(bars, labels=[str(value) for value in counts], padding=2, fontsize=8.5)

    ax.set_xlabel(r"Exceso sobre el umbral, $d_{\mathrm{final}} - 0{,}4\,\mathrm{m}$")
    ax.set_ylabel("Episodios fallidos")
    ax.set_xlim(-0.02, 0.8)
    ax.set_ylim(0, 6.35)
    ax.xaxis.set_major_locator(MultipleLocator(0.1))
    ax.xaxis.set_major_formatter(FuncFormatter(decimal_comma))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.7, alpha=0.85, zorder=0)
    ax.tick_params(axis="both", length=3, color="#666666")

    ax.text(
        0.98,
        0.94,
        r"$n = 22$ · todos: max_steps (200 pasos) · 0 fallos de seguridad",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8.2,
        color="#333333",
        bbox={"facecolor": "white", "edgecolor": "#CCCCCC", "boxstyle": "round,pad=0.3"},
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output,
        format="pdf",
        metadata={
            "Title": "Distribución del exceso terminal en los fallos de Exp016",
            "Author": "",
            "Subject": "22 episodios fallidos de la evaluación determinista de Exp016",
            "Keywords": "Exp016, final_distance, max_steps",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    plt.close(fig)


def main() -> None:
    args = _parse_args()
    validate_source(args.source_csv, required=args.require_source)
    excesses, edges, counts = histogram_data()

    print(f"failed episodes: {len(excesses)}")
    print(f"excess range: {excesses.min():.6f}--{excesses.max():.6f} m")
    print(f"bin edges: {edges.tolist()}")
    print(f"bin counts: {counts.tolist()}")

    if not args.check_only:
        generate_figure(args.output, edges, counts)
        print(f"wrote: {args.output}")


if __name__ == "__main__":
    main()
