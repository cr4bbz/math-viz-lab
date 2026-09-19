# Visualization rules

Read this reference before creating or changing a renderer.

## Required semantics

- Give every coordinate axis a variable name and, when relevant, a unit.
- Label projections, fixed variables, fibers, exceptional points, and level sets.
- Provide a legend when color, line style, or marker shape encodes meaning.
- Pair color with text, line style, or shape; never rely on color alone.
- State the plotted domain and make clipping visible through axes.
- Keep logically corresponding colors and symbols stable across states.

## Comparability

- Panels intended for direct comparison must have equal physical width and
  height, enforced by a test rather than visual inspection alone.
- Use identical scales when magnitude comparison is intended. If scales differ,
  label the difference prominently.
- Preserve earlier renders and generate a named successor when the state changes.

## Reproducibility

- Use a repository-native renderer with explicit parameter inputs.
- Fix random seeds, SVG hash salts, metadata timestamps, and output dimensions.
- Export vector graphics when the content is mathematical line art.
- Do not use HTML or browser layout in this repository.
- Rendered files must be reproducible from the manifest and selected state.

## Native interaction

- A multi-step renderer must open an overview of every projection step by
  default, rather than requiring one process invocation per step.
- Provide labelled native controls for the parameters shared across views and
  update all affected panels together.
- Keep a command-line route to a single detailed step and a deterministic
  export route for every static figure.
- Display current widget values, but treat them as exploratory. Persist a
  mathematically relevant setting as a named YAML state before relying on it in
  later work.

## Didactic layer

Each render must expose the symbolic or logical statement being visualized and
the associated Lean definition/theorem or the label `open conjecture`. Use a
second panel for a logical decomposition when it adds explanatory value.
