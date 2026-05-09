"""
quality_impact.py — DAY 3
Compares coarse vs fine-grained labels and visualises the impact on VLM learning.
Dataset: WalkingWithDog, TaiChi, Fencing (UCF101 subset)
Generates charts saved to outputs/charts/.
Run: python scripts/quality_impact.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


os.makedirs("outputs/charts", exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 120})
COLORS = {"coarse": "#378ADD", "fine": "#1D9E75", "accent": "#D85A30"}


# ── Load data ─────────────────────────────────────────────────────────────────

def load_data(path="annotations/annotations_v1.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing: {path}. Run annotation_template.py first.")
    df = pd.read_csv(path)
    # Coarse = action only.  Fine = action + intent + emotion + cultural_context
    df["coarse_label"] = df["action"]
    df["fine_label"]   = (
        df["action"] + "/" +
        df["intent"].fillna("unknown") + "/" +
        df["emotion"].fillna("unknown")
    )
    return df


# ── Chart 1: Label granularity comparison ─────────────────────────────────────

def chart_label_granularity(df):
    coarse_unique = df["coarse_label"].nunique()
    fine_unique   = df["fine_label"].nunique()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    fig.suptitle("Label Granularity: Coarse vs Fine-Grained", fontsize=13, fontweight="bold", y=1.02)

    for ax, col, title, color in [
        (axes[0], "coarse_label", f"Coarse labels\n({coarse_unique} unique)", COLORS["coarse"]),
        (axes[1], "fine_label",   f"Fine-grained labels\n({fine_unique} unique)", COLORS["fine"]),
    ]:
        counts = df[col].value_counts()
        bars = ax.barh(counts.index, counts.values, color=color, alpha=0.85)
        ax.set_xlabel("Clip count")
        ax.set_title(title, fontsize=11)
        ax.invert_yaxis()
        for bar, v in zip(bars, counts.values):
            ax.text(v + 0.05, bar.get_y() + bar.get_height() / 2,
                    str(v), va="center", fontsize=9)

    plt.tight_layout()
    out = "outputs/charts/01_label_granularity.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Chart saved: {out}")


# ── Chart 2: Ambiguity distribution ──────────────────────────────────────────

def chart_ambiguity(df):
    if "ambiguity_flag" not in df.columns:
        return

    amb_counts = df["ambiguity_flag"].value_counts()
    labels = ["Clear", "Ambiguous"]
    sizes  = [amb_counts.get(False, 0), amb_counts.get(True, 0)]
    colors = [COLORS["fine"], COLORS["accent"]]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        sizes, labels=labels, colors=colors,
        autopct="%1.0f%%", startangle=140,
        textprops={"fontsize": 11}
    )
    ax.set_title("Annotation Ambiguity Rate", fontsize=12, fontweight="bold")
    out = "outputs/charts/02_ambiguity_rate.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Chart saved: {out}")


# ── Chart 3: Confidence distribution ─────────────────────────────────────────

def chart_confidence(df):
    if "confidence" not in df.columns:
        return

    conf_map = {1: "Low", 2: "Medium", 3: "High"}
    counts = df["confidence"].value_counts().sort_index()
    labels = [conf_map.get(i, str(i)) for i in counts.index]
    bar_colors = [COLORS["accent"], COLORS["coarse"], COLORS["fine"]][:len(counts)]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, counts.values, color=bar_colors, alpha=0.85, width=0.5)
    ax.set_ylabel("Number of clips")
    ax.set_title("Annotator Confidence Distribution", fontsize=12, fontweight="bold")
    for bar, v in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.1,
                str(v), ha="center", fontsize=10)
    ax.set_ylim(0, max(counts.values) * 1.3)
    plt.tight_layout()
    out = "outputs/charts/03_confidence_dist.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Chart saved: {out}")


# ── Chart 4: VLM learning impact illustration ─────────────────────────────────

def chart_vlm_impact():
    """
    Illustrates how label granularity affects what a VLM can learn.
    This is the key chart for the Clairva application.
    """
    categories = ["Action\nrecognition", "Intent\nprediction", "Emotion\ndetection", "Cultural\ncontext"]
    coarse_scores = [0.85, 0.30, 0.10, 0.05]
    fine_scores   = [0.87, 0.75, 0.68, 0.60]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))
    bars_c = ax.bar(x - width/2, coarse_scores, width, label="Coarse labels (action only)",
                    color=COLORS["coarse"], alpha=0.85)
    bars_f = ax.bar(x + width/2, fine_scores, width, label="Fine-grained labels (all layers)",
                    color=COLORS["fine"], alpha=0.85)

    ax.set_ylabel("Estimated model capability score")
    ax.set_title("VLM Learning Capability: Coarse vs Fine-Grained Labels",
                 fontsize=12, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=9)
    ax.axhline(y=0.6, color="gray", linestyle="--", alpha=0.5)

    for bars in [bars_c, bars_f]:
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.0%}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", fontsize=9)

    note = ("Note: Scores are illustrative estimates based on label coverage.\n"
            "Coarse labels cannot train intent or emotion prediction layers.")
    ax.text(0.5, -0.18, note, transform=ax.transAxes,
            ha="center", fontsize=8, color="gray")

    plt.tight_layout()
    out = "outputs/charts/04_vlm_impact.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Chart saved: {out}")


# ── Chart 5: Cultural context distribution ────────────────────────────────────

def chart_cultural_context(df):
    if "cultural_context" not in df.columns:
        return

    counts = df["cultural_context"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(counts.index, counts.values,
                  color=[COLORS["fine"], COLORS["coarse"], COLORS["accent"],
                         "#7F77DD", "#D4537E"][:len(counts)],
                  alpha=0.85)
    ax.set_ylabel("Clip count")
    ax.set_title("Cultural Context Distribution in Dataset", fontsize=12, fontweight="bold")
    for bar, v in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.05,
                str(v), ha="center", fontsize=10)
    ax.set_ylim(0, max(counts.values) * 1.3)
    plt.tight_layout()
    out = "outputs/charts/05_cultural_context.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  Chart saved: {out}")


# ── Summary report ────────────────────────────────────────────────────────────

def write_impact_summary(df):
    coarse = df["coarse_label"].nunique()
    fine   = df["fine_label"].nunique()
    amb_pct = round(df["ambiguity_flag"].mean() * 100, 1) if "ambiguity_flag" in df.columns else "N/A"

    lines = [
        "# Data Quality Impact Report",
        "Dataset: WalkingWithDog, TaiChi, Fencing (UCF101 subset)",
        "",
        "## Key Metrics",
        f"- Total annotated clips: {len(df)}",
        f"- Unique coarse labels: {coarse}",
        f"- Unique fine-grained labels: {fine}",
        f"- Label granularity multiplier: {round(fine/coarse, 1)}x",
        f"- Ambiguity rate: {amb_pct}%",
        "",
        "## VLM Learning Impact",
        "",
        "### With coarse labels only (action):",
        "- Model can learn: what physical action is happening",
        "- Model cannot learn: why (intent), emotional tone, cultural norms",
        "- Risk: robot or agent misreads the context of an interaction",
        "",
        "### With fine-grained labels (all layers):",
        "- Model can learn: action + intent + emotion + cultural context",
        "- Benefit: richer world model, better human-robot interaction",
        "- Trade-off: higher annotation cost, more annotator training needed",
        "",
        "## Behavioural Consequence Examples",
        "",
        "### Example 1 — WalkingWithDog",
        "Scenario: A robot observes a person walking with a dog.",
        "",
        "| Label type | What the model infers | Correct? |",
        "|---|---|---|",
        "| Coarse (action=walk) | Physical movement detected | Partially |",
        "| Fine (intent=bond, emotion=happy, context=western) | Human-animal bonding interaction | Yes |",
        "| Fine (intent=navigate, emotion=neutral, context=western) | Routine outdoor transit | Yes |",
        "",
        "Without intent labels, the model cannot tell whether the person is",
        "bonding with the dog or simply using it as a walking companion.",
        "This distinction matters for a social robot deciding whether to approach or not.",
        "",
        "### Example 2 — TaiChi",
        "Scenario: A robot observes a person performing slow controlled movements.",
        "",
        "| Label type | What the model infers | Correct? |",
        "|---|---|---|",
        "| Coarse (action=movement_sequence) | Generic movement detected | Partially |",
        "| Fine (intent=exercise, emotion=calm, context=east_asian) | Solo Tai Chi practice | Yes |",
        "| Fine (intent=perform, emotion=neutral, context=east_asian) | Formal demonstration | Yes |",
        "",
        "Without cultural context labels, the model treats Tai Chi the same as",
        "any slow movement sequence, losing the cultural meaning entirely.",
        "",
        "### Example 3 — Fencing",
        "Scenario: A robot observes a forward lunge movement.",
        "",
        "| Label type | What the model infers | Correct? |",
        "|---|---|---|",
        "| Coarse (action=lunge) | Forward thrust detected | Partially |",
        "| Fine (intent=attack, emotion=tense, action_subtype=offensive) | Committed attack | Yes |",
        "| Fine (intent=attack, emotion=tense, action_subtype=feint) | Deceptive feint move | Yes |",
        "",
        "Without action_subtype labels, the model cannot distinguish a real attack",
        "from a feint — a critical distinction for any embodied AI in competitive settings.",
        "",
        "## Charts Generated",
        "- outputs/charts/01_label_granularity.png",
        "- outputs/charts/02_ambiguity_rate.png",
        "- outputs/charts/03_confidence_dist.png",
        "- outputs/charts/04_vlm_impact.png",
        "- outputs/charts/05_cultural_context.png",
    ]
    path = "outputs/quality_impact_report.md"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Impact report saved: {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nRunning Quality Impact Analysis...\n")
    df = load_data()
    chart_label_granularity(df)
    chart_ambiguity(df)
    chart_confidence(df)
    chart_vlm_impact()
    chart_cultural_context(df)
    write_impact_summary(df)
    print("\nAnalysis complete.")
    print("Open outputs/charts/ to view all 5 charts.")
    print("Open outputs/quality_impact_report.md for the written report.\n")