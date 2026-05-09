"""
qa_framework.py — DAY 2
Runs inter-annotator agreement (Cohen's Kappa) and batch consistency checks.
Dataset: WalkingWithDog, TaiChi, Fencing (UCF101 subset)
Requires annotations/annotations_v1.csv to exist.
Run: python scripts/qa_framework.py
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from datetime import datetime
import os


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_annotations(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing: {path}\nRun annotation_template.py first."
        )
    return pd.read_csv(path)


def simulate_annotator_b(df_a, n_changes=8, seed=42):
    """
    Creates a second annotator CSV by randomly altering n_changes labels.
    This simulates realistic disagreement between two human annotators.
    """
    rng = np.random.default_rng(seed)
    df_b = df_a.copy()
    df_b["annotator_id"] = "annotator_B"

    label_cols = ["action", "intent", "emotion", "cultural_context"]

    # Valid alternatives for each label (neighbouring/similar labels)
    # Updated for dataset: WalkingWithDog, TaiChi, Fencing
    alternatives = {
        # action alternatives
        "walk":              "lead",
        "lead":              "walk",
        "pull":              "walk",
        "lunge":             "strike",
        "strike":            "lunge",
        "parry":             "dodge",
        "retreat":           "dodge",
        "movement_sequence": "spin",
        "wave":              "point",
        "point":             "wave",
        # intent alternatives
        "navigate":          "exercise",
        "bond":              "navigate",
        "exercise":          "perform",
        "compete":           "attack",
        "attack":            "threaten",
        "defend":            "compete",
        "perform":           "celebrate",
        # emotion alternatives
        "tense":             "uncertain",
        "calm":              "neutral",
        "happy":             "excited",
        "neutral":           "calm",
        "fearful":           "tense",
        "excited":           "happy",
        # cultural context alternatives
        "western":           "unknown",
        "east_asian":        "SEA",
        "SEA":               "east_asian",
    }

    change_indices = rng.choice(len(df_b), size=min(n_changes, len(df_b)), replace=False)
    changes_made = []

    for idx in change_indices:
        col = rng.choice(label_cols)
        original = df_b.at[idx, col]
        new_val = alternatives.get(original, original)
        if new_val != original:
            df_b.at[idx, col] = new_val
            changes_made.append({
                "row":        int(idx),
                "video_id":   df_b.at[idx, "video_id"],
                "column":     col,
                "original":   original,
                "changed_to": new_val,
            })

    out = "annotations/annotations_v2.csv"
    df_b.to_csv(out, index=False)
    print(f"Simulated annotator B saved: {out}  ({len(changes_made)} changes made)")
    return df_b, changes_made


# ── Cohen's Kappa ─────────────────────────────────────────────────────────────

def compute_kappa(df_a, df_b):
    """Compute Cohen's Kappa for each label column."""
    label_cols = ["action", "intent", "emotion", "cultural_context"]
    shared_ids = set(df_a["video_id"]) & set(df_b["video_id"])

    a = df_a[df_a["video_id"].isin(shared_ids)].sort_values("video_id").reset_index(drop=True)
    b = df_b[df_b["video_id"].isin(shared_ids)].sort_values("video_id").reset_index(drop=True)

    results = {}
    for col in label_cols:
        try:
            k = cohen_kappa_score(a[col], b[col])
            results[col] = round(k, 4)
        except Exception as e:
            results[col] = f"Error: {e}"

    return results


def interpret_kappa(k):
    if isinstance(k, str):
        return "error"
    if k >= 0.81: return "almost perfect"
    if k >= 0.61: return "substantial"
    if k >= 0.41: return "moderate"
    if k >= 0.21: return "fair"
    return "slight / poor"


# ── Batch consistency checks ──────────────────────────────────────────────────
# Rules updated for WalkingWithDog, TaiChi, Fencing dataset

CONSISTENCY_RULES = [
    (
        "Walk action with attack or threaten intent",
        lambda r: r["action"] == "walk" and r["intent"] in ("attack", "threaten")
    ),
    (
        "Attack intent without aggressive or offensive subtype",
        lambda r: r["intent"] == "attack" and r["action_subtype"] not in ("aggressive", "offensive", "feint")
    ),
    (
        "Calm emotion with attack or compete intent",
        lambda r: r["emotion"] == "calm" and r["intent"] in ("attack", "compete")
    ),
    (
        "WalkingWithDog clip without person_and_animal diarization",
        lambda r: r["video_id"].startswith("WalkingWithDog") and r["diarization"] not in ("person_and_animal", "unknown")
    ),
    (
        "TaiChi clip with western cultural context",
        lambda r: r["video_id"].startswith("TaiChi") and r["cultural_context"] == "western"
    ),
    (
        "End time before or equal to start time",
        lambda r: r["end_time_sec"] <= r["start_time_sec"]
    ),
    (
        "Low confidence with no notes",
        lambda r: r["confidence"] == 1 and (pd.isna(r.get("notes", "")) or r.get("notes", "") == "")
    ),
]


def batch_consistency_check(df):
    issues = []
    for _, row in df.iterrows():
        for desc, rule in CONSISTENCY_RULES:
            try:
                if rule(row):
                    issues.append({
                        "video_id": row["video_id"],
                        "rule":     desc,
                        "action":   row.get("action"),
                        "intent":   row.get("intent"),
                        "emotion":  row.get("emotion"),
                    })
            except Exception:
                pass
    return issues


# ── Report writer ─────────────────────────────────────────────────────────────

def write_qa_report(kappa_scores, issues, changes, df_a):
    lines = [
        "# QA Report — AsiaInteract",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 1. Dataset Summary",
        f"- Total clips annotated: {len(df_a)}",
        f"- Categories: WalkingWithDog, TaiChi, Fencing",
        f"- Annotators: annotator_A (real), annotator_B (simulated)",
        f"- Simulated disagreements introduced: {len(changes)}",
        "",
        "## 2. Inter-Annotator Agreement (Cohen's Kappa)",
        "",
        "| Label Column | Kappa | Interpretation |",
        "|---|---|---|",
    ]
    for col, k in kappa_scores.items():
        lines.append(f"| {col} | {k} | {interpret_kappa(k)} |")

    lines += [
        "",
        "### Kappa Scale Reference",
        "- 0.81 to 1.00 = Almost perfect",
        "- 0.61 to 0.80 = Substantial",
        "- 0.41 to 0.60 = Moderate",
        "- 0.21 to 0.40 = Fair",
        "- Below 0.20   = Slight / poor",
        "",
        "## 3. Batch Consistency Issues",
        f"Found {len(issues)} rule violations:",
        "",
    ]

    if issues:
        for i in issues:
            lines.append(f"- {i['video_id']}: {i['rule']}")
            lines.append(f"  action={i['action']}, intent={i['intent']}, emotion={i['emotion']}")
    else:
        lines.append("No consistency issues found.")

    lines += [
        "",
        "## 4. Simulated Disagreements (for reference)",
        "",
        "| Video | Column | Annotator A | Annotator B |",
        "|---|---|---|---|",
    ]
    for c in changes:
        lines.append(f"| {c['video_id']} | {c['column']} | {c['original']} | {c['changed_to']} |")

    lines += [
        "",
        "## 5. Recommended Actions",
        "- Review clips with kappa below 0.60 and add clearer label definitions",
        "- Update annotation guidelines for ambiguous action/intent pairs",
        "- Re-annotate consistency-flagged clips with a second pass",
        "- Add a policy requiring notes for all confidence=1 annotations",
    ]

    os.makedirs("qa_reports", exist_ok=True)
    report_path = "qa_reports/qa_report_v1.md"
    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    kappa_df = pd.DataFrame([
        {"label_column": k, "kappa_score": v, "interpretation": interpret_kappa(v)}
        for k, v in kappa_scores.items()
    ])
    kappa_df.to_csv("qa_reports/kappa_scores.csv", index=False)

    print(f"QA report saved:    qa_reports/qa_report_v1.md")
    print(f"Kappa scores saved: qa_reports/kappa_scores.csv")
    return report_path


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nRunning QA Framework...\n")

    df_a = load_annotations("annotations/annotations_v1.csv")
    print(f"Loaded annotator_A: {len(df_a)} rows")

    df_b, changes = simulate_annotator_b(df_a)

    kappa = compute_kappa(df_a, df_b)
    print("\nCohen's Kappa Scores:")
    for col, k in kappa.items():
        print(f"   {col:20s}: {k}  ({interpret_kappa(k)})")

    issues = batch_consistency_check(df_a)
    print(f"\nConsistency issues found: {len(issues)}")
    for i in issues:
        print(f"   - {i['video_id']}: {i['rule']}")

    write_qa_report(kappa, issues, changes, df_a)

    print("\nQA complete.")
    print("Open qa_reports/qa_report_v1.md to review findings")
    print("Next step: python scripts/quality_impact.py\n")