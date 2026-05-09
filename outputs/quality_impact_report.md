# Data Quality Impact Report
Dataset: WalkingWithDog, TaiChi, Fencing (UCF101 subset)

## Key Metrics
- Total annotated clips: 15
- Unique coarse labels: 6
- Unique fine-grained labels: 10
- Label granularity multiplier: 1.7x
- Ambiguity rate: 40.0%

## VLM Learning Impact

### With coarse labels only (action):
- Model can learn: what physical action is happening
- Model cannot learn: why (intent), emotional tone, cultural norms
- Risk: robot or agent misreads the context of an interaction

### With fine-grained labels (all layers):
- Model can learn: action + intent + emotion + cultural context
- Benefit: richer world model, better human-robot interaction
- Trade-off: higher annotation cost, more annotator training needed

## Behavioural Consequence Examples

### Example 1 — WalkingWithDog
Scenario: A robot observes a person walking with a dog.

| Label type | What the model infers | Correct? |
|---|---|---|
| Coarse (action=walk) | Physical movement detected | Partially |
| Fine (intent=bond, emotion=happy, context=western) | Human-animal bonding interaction | Yes |
| Fine (intent=navigate, emotion=neutral, context=western) | Routine outdoor transit | Yes |

Without intent labels, the model cannot tell whether the person is
bonding with the dog or simply using it as a walking companion.
This distinction matters for a social robot deciding whether to approach or not.

### Example 2 — TaiChi
Scenario: A robot observes a person performing slow controlled movements.

| Label type | What the model infers | Correct? |
|---|---|---|
| Coarse (action=movement_sequence) | Generic movement detected | Partially |
| Fine (intent=exercise, emotion=calm, context=east_asian) | Solo Tai Chi practice | Yes |
| Fine (intent=perform, emotion=neutral, context=east_asian) | Formal demonstration | Yes |

Without cultural context labels, the model treats Tai Chi the same as
any slow movement sequence, losing the cultural meaning entirely.

### Example 3 — Fencing
Scenario: A robot observes a forward lunge movement.

| Label type | What the model infers | Correct? |
|---|---|---|
| Coarse (action=lunge) | Forward thrust detected | Partially |
| Fine (intent=attack, emotion=tense, action_subtype=offensive) | Committed attack | Yes |
| Fine (intent=attack, emotion=tense, action_subtype=feint) | Deceptive feint move | Yes |

Without action_subtype labels, the model cannot distinguish a real attack
from a feint — a critical distinction for any embodied AI in competitive settings.

## Charts Generated
- outputs/charts/01_label_granularity.png
- outputs/charts/02_ambiguity_rate.png
- outputs/charts/03_confidence_dist.png
- outputs/charts/04_vlm_impact.png
- outputs/charts/05_cultural_context.png