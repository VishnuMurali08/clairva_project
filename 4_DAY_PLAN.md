# Project Plan — AsiaInteract

## Day 1 — Setup + Data + Schema
- [ ] Run `python scripts/setup.py`
- [ ] Install VS Code extensions (Python, Jupyter, Rainbow CSV)
- [ ] Create virtual env: `python -m venv venv` → `pip install -r requirements.txt`
- [ ] Download UCF101: HandshakeGreeting + TaiChi + Fencing (~200MB)
- [ ] Place .avi files in `data/raw_videos/`
- [ ] Run `python scripts/frame_extractor.py`
- [ ] Run `python scripts/annotation_template.py`
- [ ] Manually annotate 15–20 clips in `annotations/annotations_v1.csv`
- [ ] Review `schemas/label_taxonomy.json` and adjust if needed

**End of Day 1 deliverable:** annotations_v1.csv with 15+ labelled clips

---

## Day 2 — QA Framework
- [ ] Annotate 10 more clips (aim for 25 total)
- [ ] Run `python scripts/qa_framework.py`
  - Simulates annotator B automatically
  - Computes Cohen's Kappa scores
  - Runs batch consistency checks
- [ ] Read `qa_reports/qa_report_v1.md`
- [ ] Fix any consistency violations flagged
- [ ] Review the decision tree: `guidelines/ambiguity_decision_tree.md`

**End of Day 2 deliverable:** qa_report_v1.md with Kappa scores

---

## Day 3 — Quality Impact Analysis + Guidelines
- [ ] Run `python scripts/quality_impact.py`
- [ ] Review 5 charts in `outputs/charts/`
- [ ] Read `outputs/quality_impact_report.md`
- [ ] Read `guidelines/annotation_guidelines.md` — customise for your clips
- [ ] Read `guidelines/buyer_spec_example.md` — add your own example
- [ ] Open `notebooks/03_quality_impact.ipynb` for deeper exploration

**End of Day 3 deliverable:** All outputs/ and guidelines/ complete

---

## Day 4 — Polish + GitHub
- [ ] Update `README.md` with your actual results (Kappa scores, clip counts)
- [ ] Update `FINDINGS.md` with your real observations
- [ ] Create GitHub repo (github.com → New repository → "asiainteract")
- [ ] Push all files: `git init → git add . → git commit → git push`
- [ ] Test: can someone understand the project from README in 5 minutes?
- [ ] Draft Clairva application email with GitHub link

**End of Day 4 deliverable:** Public GitHub repo ready to share

---

## VS Code Extensions to Install
1. Python (by Microsoft)
2. Jupyter (by Microsoft)
3. Rainbow CSV (by mechatroner)
4. Pylance (by Microsoft)
5. JSON Tools (by Erik Lynd)
