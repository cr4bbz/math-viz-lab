---
name: graphical-math-research
description: Conduct repository-based graphical mathematics research using versioned experiment manifests, deterministic labelled figures, didactic research notes, and checked Lean claims. Use when creating or extending a math-viz-lab experiment, investigating projections or fibers, comparing visual states, turning observations into conjectures, or formalizing a visual claim. Do not use for unrelated plotting or ordinary Lean work without a visual-research component.
---

# Graphical Math Research

Build a reproducible chain from question to visual evidence to formal statement.
The experiment manifest and named state files are the shared state between the
user and the agent; a GUI state is never authoritative.

## Start

1. Find the relevant `experiments/*/experiment.yaml`.
2. Read that manifest, its `ResearchNotes.md`, and the selected file under
   `states/`. If the user has not selected a state, use `view.default_state` and
   state the choice.
3. Run `scripts/validate_experiment.py` before editing. Fix structural errors
   before interpreting results.
4. Classify the request as exploration, comparison, formalization, or creation of
   a new experiment.

For a new experiment or a manifest change, read
[references/manifest.md](references/manifest.md). Start from
[assets/experiment-template.yaml](assets/experiment-template.yaml) instead of
inventing a new structure.

## Research loop

1. Formulate one concrete mathematical question.
2. Identify the information discarded by the proposed projection and the fiber
   that remains.
3. Create or select a named state recording parameters, projection, question,
   and expected phenomenon. Never overwrite a prior state to represent a new
   case.
4. Produce a deterministic, fully labelled render. For rendering or layout
   changes, read [references/visualization-rules.md](references/visualization-rules.md).
5. Record the result as exactly one of: `visual_observation`,
   `numerical_evidence`, `conjecture`, `counterexample`, or `lean_proved`.
6. When promoting a claim to a theorem, read
   [references/lean-workflow.md](references/lean-workflow.md), formalize it, and
   execute the declared Lean checks.
7. Update `ResearchNotes.md` with the evidence, limitations, and next useful
   projection. Follow [references/research-protocol.md](references/research-protocol.md)
   when the distinction between evidence types is unclear.

## Render and validate

- Use `scripts/render_experiment.py <manifest>` to call the renderer declared by
  the manifest.
- Run `scripts/validate_experiment.py <manifest>` again after changes.
- Execute every command in `validation.commands` that is relevant to the files
  changed. A renderer change always requires its visualization tests.
- Compare regenerated output with prior renders and explain material visual
  changes. Do not treat unchanged pixels as mathematical validation.

## Response contract

Report:

- the investigated question and selected state;
- what the projection reveals and what it suppresses;
- the evidence classification;
- the corresponding Lean theorem or explicitly open conjecture;
- commands actually run and their results;
- the next mathematically motivated state or projection.

Show generated figures directly in the conversation when the host supports local
images. Do not replace the versioned experiment with a browser application.
