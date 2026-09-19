# Experiment manifest

Read this reference when creating an experiment, changing manifest structure, or
adding a new kind of state.

## Authority

`experiment.yaml` identifies the mathematical object, current default state,
source files, reproducible outputs, evidence ledger, and validation commands. It
does not contain long explanations; those belong in `ResearchNotes.md`.

State files under `states/` are immutable research snapshots. Create a new state
when parameters, projection, question, or expected phenomenon changes.

## Required top-level fields

- `schema_version`: currently `1`.
- `experiment`: stable `id`, title, and lifecycle status.
- `object`: family or relation, ambient spaces, and zero/solution locus.
- `paths`: repository-relative renderer, Lean source, notes, states, and renders.
- `view`: projection sequence and default state.
- `research`: question plus separately classified evidence collections.
- `render`: deterministic format and labelling invariants.
- `validation`: executable commands that establish mechanical correctness.

All paths are relative to the repository root and must remain inside it. Use the
template in `assets/experiment-template.yaml` and validate after editing.

## State identity

Each state requires:

- `schema_version` and matching `experiment_id`;
- a unique kebab-case `state_id`;
- `projection`, `parameters`, and a focused `question`;
- `expected` for the phenomenon under investigation;
- `evidence_status`, which must not claim more than the recorded evidence;
- an optional `lean_theorem` only when the named theorem exists and has passed
  the experiment's Lean validation.
