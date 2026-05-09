# FINDINGS - Data Quality Lessons Learned

This document directly answers Clairva's application question:
> "A short note on a dataset you have worked with and what you learned about data quality."

---

## Dataset
UCF101 subset — WalkingWithDog, TaiChi, Fencing (~100 clips)

---

## Finding 1: Label granularity is a model capability decision

When I annotated clips with coarse labels (action only), the dataset told a
VLM what happened physically. When I added intent, emotion, and cultural
context layers, the same clips could now train a model to understand *why*
something happened and *what it means socially*.

The difference is not cosmetic. A model trained on coarse labels can classify
a walk as a physical movement. A model trained on fine-grained labels can
distinguish a person walking a dog to bond with it from a person walking a
dog as routine exercise — which changes how a social robot should respond
to that person in a park or public space.

**Lesson:** Every label is a model capability decision. Before labelling,
ask: "What does this model need to *do* with this information?"

---

## Finding 2: Ambiguity is data, not a problem to eliminate

My initial instinct was to remove or skip ambiguous clips (intent unclear,
cultural context uncertain). After reflection, I kept them and flagged them.

Ambiguous clips are exactly the real-world cases a model will encounter in
deployment. A social robot in a Singapore office *will* see interactions
where intent is unclear. If the training data never includes ambiguous cases
with documented reasoning, the model has no basis for handling uncertainty.

**Lesson:** Ambiguity should be captured, not hidden. The annotator's
reasoning about ambiguous cases is as valuable as clear-cut labels.

---

## Finding 3: Cultural context labels require cultural knowledge

Several clips I labelled as "western" were likely SEA-context interactions
I simply did not recognise — a slight bow that I defaulted to "western nod"
because I was not familiar with the specific cultural signal.

This showed me that annotation quality for culturally-grounded datasets
requires annotators who actually have that cultural knowledge. For Clairva's
Asia/Global South focus, having annotators from those regions is not a
nice-to-have — it is a quality requirement.

**Lesson:** Taxonomy design must account for annotator knowledge gaps.
If you cannot reliably assign a label, the label should be `unknown`
with a note — not a best guess.

---

## Summary Table

| Lesson | Impact on model | Fix applied |
|---|---|---|
| Coarse labels limit model capability | VLM cannot learn intent/emotion | Added 4 annotation layers |
| Ambiguity is informative | Model needs uncertainty handling | Kept flagged clips + documented reasoning |
| Cultural knowledge gap | Mislabelled cultural context | Used `unknown` when unsure; noted candidates |
