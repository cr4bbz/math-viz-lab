# math-viz-lab agent instructions

## Purpose

This repository is a durable laboratory for graphical mathematics research. A
contribution must connect a mathematical question, reproducible visual evidence,
didactic explanation, and a checked Lean statement.

## Required workflow

- Use the repository skill `$graphical-math-research` for creating, extending,
  comparing, or formalizing an experiment.
- Read an experiment's `experiment.yaml`, selected state file, and research notes
  before changing its mathematics or renderer.
- Treat the manifest and named state files as the shared research state. Do not
  rely on transient GUI state or conversation memory.
- Preserve existing state files. Record a materially new parameter choice,
  projection, or conjecture as a new named state.
- Keep observations, conjectures, and Lean-proved claims explicitly distinct.
- Use deterministic, repository-native renderers. Do not build browser or HTML
  visualizations for this project.
- A multi-step experiment must open a native interactive overview by default:
  render every projection step at the same time and provide labelled controls
  for the parameters that connect those views. A command-line option may still
  open one detailed step, and deterministic static exports remain required.
- Interactive controls are exploratory views of explicit parameters. Display
  their current values, map stable findings to named YAML states, and never let
  transient widget state become the only record of a result.
- Label every plotted variable, axis, projection, fiber, color encoding, and
  exceptional case. Comparable panels must use equal physical dimensions unless
  the manifest documents a mathematical reason not to.
- A rendered image is evidence for exploration, never a proof.

## Validation

Before completing a contribution:

1. Validate all experiment manifests and states.
2. Regenerate affected renders.
3. Run the renderer tests.
4. Run `lake build` for changes that touch mathematical claims or Lean sources.
5. Update the experiment's `ResearchNotes.md` with the question, evidence type,
   conclusion, and next useful projection.

Use the validation commands declared by the experiment manifest. Do not claim a
check passed unless it was executed successfully.

## Repository hygiene

- Work on the current task branch and preserve unrelated user changes.
- Keep reusable mechanics in the repository skill or shared tooling; keep
  experiment-specific mathematics inside its experiment bundle.
- Generated renders may be versioned when the manifest declares them as
  reproducible outputs.
