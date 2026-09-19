import Mathlib.NumberTheory.LSeries.ZetaZeros
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues
import Mathlib.Tactic

/-!
# Visualisierbare Grundlagen der Riemannschen Vermutung

Diese Datei formalisiert Begriffe und bewiesene Hintergrundsätze. Die
Riemannsche Vermutung selbst bleibt das bereits in mathlib definierte offene
Prädikat `RiemannHypothesis`; es wird hier ausdrücklich nicht bewiesen.
-/

namespace MathVizLab

/-- Der offene kritische Streifen `0 < re(s) < 1`. -/
def InCriticalStrip (s : ℂ) : Prop := 0 < s.re ∧ s.re < 1

/-- Die kritische Gerade `re(s)=1/2`. -/
def OnCriticalLine (s : ℂ) : Prop := s.re = 1 / 2

/-- Eine Nullstelle, nachdem die trivialen negativen geraden Nullstellen und
der ausgezeichnete Punkt `1` ausgeschlossen wurden. -/
def NontrivialZetaZero (s : ℂ) : Prop :=
  riemannZeta s = 0 ∧ (¬ ∃ n : ℕ, s = -2 * (n + 1)) ∧ s ≠ 1

/-- Unsere didaktische Formulierung ist äquivalent zur mathlib-Definition der
Riemannschen Vermutung. Dies beweist nicht die Vermutung. -/
theorem riemannHypothesis_iff_nontrivial_zeros_on_line :
    RiemannHypothesis ↔
      ∀ s : ℂ, NontrivialZetaZero s → OnCriticalLine s := by
  constructor
  · intro h s hs
    exact h s hs.1 hs.2.1 hs.2.2
  · intro h s hz htrivial hone
    exact h s ⟨hz, htrivial, hone⟩

/-- Parametrisierung der kritischen Geraden. -/
noncomputable def criticalLinePoint (t : ℝ) : ℂ :=
  (1 / 2 : ℂ) + (t : ℂ) * Complex.I

@[simp] theorem criticalLinePoint_on_line (t : ℝ) :
    OnCriticalLine (criticalLinePoint t) := by
  norm_num [OnCriticalLine, criticalLinePoint]

/-- Spiegelung an `s ↦ 1-s` erhält die kritische Gerade. -/
theorem onCriticalLine_one_sub_iff (s : ℂ) :
    OnCriticalLine (1 - s) ↔ OnCriticalLine s := by
  change 1 - s.re = 1 / 2 ↔ s.re = 1 / 2
  constructor <;> intro h <;> linarith

/-- Die negativen geraden Zahlen sind die trivialen Nullstellen. -/
theorem negative_even_is_zeta_zero (n : ℕ) :
    riemannZeta (-2 * (n + 1)) = 0 :=
  riemannZeta_neg_two_mul_nat_add_one n

/-- Rechts des kritischen Streifens einschließlich seiner Randgeraden bei
`re(s)=1` besitzt ζ keine Nullstellen. -/
theorem zeta_nonzero_of_one_le_re {s : ℂ} (hs : 1 ≤ s.re) :
    riemannZeta s ≠ 0 :=
  riemannZeta_ne_zero_of_one_le_re hs

/-- Die Nullstellenmenge ist in jedem kompakten Beobachtungsfenster endlich. -/
theorem compact_inter_zetaZeros_finite {K : Set ℂ} (hK : IsCompact K) :
    (K ∩ riemannZetaZeros).Finite :=
  hK.inter_riemannZetaZeros_finite

/-- Der Basel-Wert ist zugleich der spezielle Zeta-Wert bei `s=2`. -/
theorem zeta_two_bridge :
    riemannZeta 2 = (Real.pi : ℂ) ^ 2 / 6 :=
  riemannZeta_two

end MathVizLab
