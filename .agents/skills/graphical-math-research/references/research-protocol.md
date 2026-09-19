# Research protocol

Use this reference when classifying a result or updating research notes.

## Evidence classes

- `visual_observation`: a labelled render suggests a pattern in the displayed
  domain. It may depend on clipping, sampling, or chosen parameters.
- `numerical_evidence`: evaluated values support a claim for finitely many cases.
- `conjecture`: a quantified statement proposed for proof or refutation.
- `counterexample`: an explicit state falsifies a conjecture.
- `lean_proved`: Lean accepts the stated theorem without placeholders.

Never silently promote one class to another. A theorem may explain a visual
observation; the image does not prove the theorem.

## Projection questions

For each projection record:

1. Which variables remain visible?
2. Which variables or distinctions are discarded?
3. What is a fiber in this view?
4. Where does its cardinality, dimension, multiplicity, or topology change?
5. Which exceptional case would an algebraic cancellation hide?

## Research note entry

Record the date, state id, question, projection, evidence class, observation,
limitation, Lean link or open conjecture, and next experiment. Prefer a short,
auditable entry over a narrative that mixes several research steps.
