# AsiaInteract - Annotated Human Interaction Dataset

## Overview
An end-to-end annotation pipeline for multi-person interaction video,
built as a portfolio project for the Clairva AI Data Scientist role.

This project demonstrates:
- Annotation schema and taxonomy design
- Temporal annotation pipeline
- QA framework with inter-annotator agreement
- Data quality impact analysis
- Real-world ambiguity handling
- Annotation guidelines and buyer spec translation

## Dataset
UCF101 subset — 3 interaction categories:
- HandshakeGreeting (~25 clips)
- TaiChi (~25 clips)
- Fencing (~25 clips)

## Project Structure
```
asiainteract/
├── data/
│   ├── raw_videos/       ← Place UCF101 .avi files here
│   └── frames/           ← Auto-generated extracted frames
├── schemas/
│   ├── annotation_schema.json    ← Master JSON schema
│   └── label_taxonomy.json       ← Allowed label values
├── annotations/
│   ├── annotations_v1.csv        ← Annotator A labels
│   ├── annotations_v2.csv        ← Annotator B labels (simulated)
│   └── annotations_merged.csv    ← Final merged labels
├── qa_reports/
│   ├── qa_report_v1.md           ← QA findings report
│   └── kappa_scores.csv          ← Inter-annotator agreement scores
├── guidelines/
│   ├── annotation_guidelines.md  ← Full annotator guidelines
│   ├── ambiguity_decision_tree.md← Edge case handling
│   └── buyer_spec_example.md     ← AI lab spec → annotation guideline
├── notebooks/
│   ├── 01_data_exploration.ipynb ← Explore UCF101 clips
│   ├── 02_qa_analysis.ipynb      ← QA metrics and charts
│   └── 03_quality_impact.ipynb   ← Coarse vs fine label comparison
├── outputs/
│   └── charts/                   ← Generated visualisations
├── scripts/
│   ├── setup.py                  ← Run first: creates folders
│   ├── frame_extractor.py        ← Day 1: extract video frames
│   ├── annotation_template.py    ← Day 1: generate CSV template
│   ├── qa_framework.py           ← Day 2: Cohen Kappa + checks
│   └── quality_impact.py         ← Day 3: label comparison analysis
├── FINDINGS.md                   ← Key data quality lessons learned
├── requirements.txt
└── .vscode/settings.json
```

## Quick Start
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup
python scripts/setup.py

# 4. Place UCF101 videos in data/raw_videos/

# 5. Extract frames
python scripts/frame_extractor.py

# 6. Generate annotation template
python scripts/annotation_template.py

# 7. Fill in annotations/annotations_v1.csv manually

# 8. Run QA framework
python scripts/qa_framework.py

# 9. Run quality impact analysis
python scripts/quality_impact.py
```

## Key Findings
See [FINDINGS.md](FINDINGS.md) for data quality lessons learned.

## Author
Portfolio project for Clairva AI Data Scientist application — 2026
