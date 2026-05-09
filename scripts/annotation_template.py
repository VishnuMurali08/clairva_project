"""
annotation_template.py — DAY 1
Generates the annotation CSV template and JSON label taxonomy.
Dataset: TaiChi, Fencing, WalkingWithDog (UCF101 subset)
Run after frame_extractor.py.
"""

import pandas as pd
import json
import os


# ── Label taxonomy ────────────────────────────────────────────────────────────

TAXONOMY = {
    "action": [
        "walk", "wave", "point", "nod", "pull", "lead",
        "lunge", "strike", "dodge", "parry", "retreat",
        "movement_sequence", "spin", "kick", "crouch", "jump"
    ],
    "action_subtype": [
        "formal", "casual", "aggressive", "defensive", "slow_controlled",
        "fast", "offensive", "feint", "ceremonial", "playful"
    ],
    "intent": [
        "navigate", "exercise", "bond", "compete",
        "attack", "defend", "perform",
        "celebrate", "comfort", "threaten", "unknown"
    ],
    "emotion": [
        "happy", "sad", "angry", "neutral", "calm",
        "tense", "excited", "fearful", "surprised", "uncertain"
    ],
    "diarization": [
        "person_A", "person_B", "both", "person_and_animal", "unknown"
    ],
    "cultural_context": [
        "western", "SEA", "south_asian", "east_asian",
        "middle_eastern", "african", "latin", "unknown"
    ],
    "confidence": [1, 2, 3],   # 1=low  2=medium  3=high
}

# ── Example rows to guide you ─────────────────────────────────────────────────
# These 6 rows cover all 3 dataset categories.
# Add your own rows below these in the CSV after running this script.

EXAMPLES = [
    {
        "video_id":         "WalkingWithDog_001",
        "annotator_id":     "annotator_A",
        "start_time_sec":   0.0,
        "end_time_sec":     4.0,
        "action":           "walk",
        "action_subtype":   "casual",
        "intent":           "navigate",
        "emotion":          "calm",
        "diarization":      "person_and_animal",
        "cultural_context": "western",
        "confidence":       3,
        "ambiguity_flag":   False,
        "notes":            "Person walking dog on leash, relaxed pace, outdoor setting",
    },
    {
        "video_id":         "WalkingWithDog_002",
        "annotator_id":     "annotator_A",
        "start_time_sec":   0.0,
        "end_time_sec":     5.0,
        "action":           "walk",
        "action_subtype":   "playful",
        "intent":           "bond",
        "emotion":          "happy",
        "diarization":      "person_and_animal",
        "cultural_context": "western",
        "confidence":       2,
        "ambiguity_flag":   True,
        "notes":            "Person jogging with dog — ambiguous between navigate and bond intent",
    },
    {
        "video_id":         "TaiChi_001",
        "annotator_id":     "annotator_A",
        "start_time_sec":   0.0,
        "end_time_sec":     5.0,
        "action":           "movement_sequence",
        "action_subtype":   "slow_controlled",
        "intent":           "exercise",
        "emotion":          "calm",
        "diarization":      "person_A",
        "cultural_context": "east_asian",
        "confidence":       3,
        "ambiguity_flag":   False,
        "notes":            "Traditional Tai Chi form, solo practitioner",
    },
    {
        "video_id":         "TaiChi_002",
        "annotator_id":     "annotator_A",
        "start_time_sec":   0.0,
        "end_time_sec":     6.0,
        "action":           "movement_sequence",
        "action_subtype":   "ceremonial",
        "intent":           "perform",
        "emotion":          "neutral",
        "diarization":      "both",
        "cultural_context": "east_asian",
        "confidence":       2,
        "ambiguity_flag":   True,
        "notes":            "Two people performing in sync — could be exercise or performance",
    },
    {
        "video_id":         "Fencing_001",
        "annotator_id":     "annotator_A",
        "start_time_sec":   1.0,
        "end_time_sec":     3.0,
        "action":           "lunge",
        "action_subtype":   "offensive",
        "intent":           "attack",
        "emotion":          "tense",
        "diarization":      "person_A",
        "cultural_context": "western",
        "confidence":       2,
        "ambiguity_flag":   True,
        "notes":            "Intent ambiguous — could be feint or real attack",
    },
    {
        "video_id":         "Fencing_002",
        "annotator_id":     "annotator_A",
        "start_time_sec":   0.0,
        "end_time_sec":     1.5,
        "action":           "parry",
        "action_subtype":   "defensive",
        "intent":           "defend",
        "emotion":          "tense",
        "diarization":      "person_B",
        "cultural_context": "western",
        "confidence":       2,
        "ambiguity_flag":   True,
        "notes":            "Hard to tell if parry or counter-attack initiated",
    },
]


def create_annotation_csv(path="annotations/annotations_v1.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(EXAMPLES)
    df.to_csv(path, index=False)
    print(f"Annotation template created: {path}")
    print(f"   {len(df)} example rows included (2 WalkingWithDog, 2 TaiChi, 2 Fencing)")
    print(f"   Add your own rows starting from row {len(df) + 2} in the CSV")
    return df


def create_taxonomy(path="schemas/label_taxonomy.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(TAXONOMY, f, indent=2)
    print(f"Label taxonomy created:      {path}")
    return TAXONOMY


def create_annotation_schema(path="schemas/annotation_schema.json"):
    """Full JSON Schema for validating annotation rows."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "AsiaInteract Annotation Schema",
        "description": "Schema for multi-person and person-animal interaction video annotations",
        "type": "object",
        "required": [
            "video_id", "annotator_id", "start_time_sec", "end_time_sec",
            "action", "intent", "emotion", "diarization", "cultural_context",
            "confidence"
        ],
        "properties": {
            "video_id":         {"type": "string",  "description": "Unique video clip identifier e.g. WalkingWithDog_001"},
            "annotator_id":     {"type": "string",  "description": "Who created this annotation"},
            "start_time_sec":   {"type": "number",  "minimum": 0},
            "end_time_sec":     {"type": "number",  "minimum": 0},
            "action":           {"type": "string",  "enum": TAXONOMY["action"]},
            "action_subtype":   {"type": "string",  "enum": TAXONOMY["action_subtype"]},
            "intent":           {"type": "string",  "enum": TAXONOMY["intent"]},
            "emotion":          {"type": "string",  "enum": TAXONOMY["emotion"]},
            "diarization":      {"type": "string",  "enum": TAXONOMY["diarization"]},
            "cultural_context": {"type": "string",  "enum": TAXONOMY["cultural_context"]},
            "confidence":       {"type": "integer", "enum": [1, 2, 3]},
            "ambiguity_flag":   {"type": "boolean"},
            "notes":            {"type": "string"},
        },
        "additionalProperties": False
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"JSON schema created:         {path}")
    return schema


if __name__ == "__main__":
    print("\nGenerating annotation templates...\n")
    create_annotation_csv()
    create_taxonomy()
    create_annotation_schema()
    print("\nAll templates ready.")
    print("Next steps:")
    print("  1. Open annotations/annotations_v1.csv in VS Code")
    print("  2. Watch your video clips in data/frames/")
    print("  3. Fill in one row per clip using schemas/label_taxonomy.json as reference\n")