# QA Report — AsiaInteract
Generated: 2026-05-09 12:54

## 1. Dataset Summary
- Total clips annotated: 15
- Categories: WalkingWithDog, TaiChi, Fencing
- Annotators: annotator_A (real), annotator_B (simulated)
- Simulated disagreements introduced: 8

## 2. Inter-Annotator Agreement (Cohen's Kappa)

| Label Column | Kappa | Interpretation |
|---|---|---|
| action | 0.8266 | almost perfect |
| intent | 0.8404 | almost perfect |
| emotion | 0.8396 | almost perfect |
| cultural_context | 0.7521 | substantial |

### Kappa Scale Reference
- 0.81 to 1.00 = Almost perfect
- 0.61 to 0.80 = Substantial
- 0.41 to 0.60 = Moderate
- 0.21 to 0.40 = Fair
- Below 0.20   = Slight / poor

## 3. Batch Consistency Issues
Found 0 rule violations:

No consistency issues found.

## 4. Simulated Disagreements (for reference)

| Video | Column | Annotator A | Annotator B |
|---|---|---|---|
| v_WalkingWithDog_g01_c02 | cultural_context | western | unknown |
| v_Fencing_g01_c01 | emotion | tense | uncertain |
| v_Fencing_g01_c02 | action | parry | dodge |
| v_TaiChi_g01_c05 | cultural_context | east_asian | SEA |
| v_TaiChi_g01_c01 | intent | exercise | perform |
| v_WalkingWithDog_g01_c05 | emotion | happy | excited |
| v_WalkingWithDog_g01_c01 | intent | navigate | exercise |
| v_TaiChi_g01_c02 | action | movement_sequence | spin |

## 5. Recommended Actions
- Review clips with kappa below 0.60 and add clearer label definitions
- Update annotation guidelines for ambiguous action/intent pairs
- Re-annotate consistency-flagged clips with a second pass
- Add a policy requiring notes for all confidence=1 annotations