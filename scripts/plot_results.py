"""Create the precision/recall figure referenced by README.md.

The script reads the evaluation CSV produced by the notebook and writes a
small, publication-friendly PNG. The two starred points are the approximate
ICWMF@10 values reported in Figure 3 of the reference paper.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = ROOT / "cache" / "part1" / "part4_evaluation" / "evaluation_metrics.csv"
OUTPUT_PATH = ROOT / "results" / "precision_recall_current.png"


def main() -> None:
    if not METRICS_PATH.is_file():
        raise FileNotFoundError(
            f"Evaluation file not found: {METRICS_PATH}. "
            "Run the notebook before generating the figure."
        )

    metrics = pd.read_csv(METRICS_PATH)
    selected = metrics[metrics["metric"].str.match(r"^(Precision|Recall)@\d+$")].copy()
    selected[["metric_type", "cutoff"]] = selected["metric"].str.extract(
        r"^(Precision|Recall)@(\d+)$"
    )
    selected["cutoff"] = selected["cutoff"].astype(int)
    values = selected.pivot(index="cutoff", columns="metric_type", values="mean").sort_index()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=160)

    ax.plot(
        values.index,
        values["Precision"],
        marker="o",
        linewidth=2,
        label="Current precision",
    )
    ax.plot(
        values.index,
        values["Recall"],
        marker="o",
        linewidth=2,
        label="Current recall",
    )

    ax.scatter(
        [10],
        [0.26],
        marker="*",
        s=130,
        color="black",
        label="Paper ICWMF @10 precision ≈ 0.26",
    )
    ax.scatter(
        [10],
        [0.13],
        marker="*",
        s=130,
        color="dimgray",
        label="Paper ICWMF @10 recall ≈ 0.13",
    )

    ax.set_title("Current cached experiment on Gowalla")
    ax.set_xlabel("Recommendation cutoff (n)")
    ax.set_ylabel("Mean metric")
    ax.set_xticks(values.index)
    ax.set_ylim(0, 0.32)
    ax.legend(fontsize=8, loc="center right")
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
