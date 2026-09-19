import Lake
open Lake DSL

package mathVizLab where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.34.0"

lean_lib MathVizLab

@[default_target]
lean_exe mathVizLabCheck where
  root := `Main
