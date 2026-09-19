import Mathlib.NumberTheory.ZetaValues
import Mathlib.Tactic

/-!
# Das Basel-Problem und die symmetrische Ganzzahlsumme

Wir unterscheiden die klassische Reihe über positive natürliche Zahlen von der
beidseitigen Reihe über `ℤ \ {0}`. Der Index `0` wird durch einen Nullterm
repräsentiert, damit die in mathlib total definierte Division nicht mit der
mathematischen Definitionsmenge verwechselt wird.
-/

namespace MathVizLab

/-- Der Basel-Summand; `n=0` ist nur ein ausgeschlossener Nullplatzhalter. -/
noncomputable def baselTerm (n : ℕ) : ℝ :=
  if n = 0 then 0 else 1 / (n : ℝ) ^ 2

@[simp] theorem baselTerm_zero : baselTerm 0 = 0 := by
  simp [baselTerm]

theorem baselTerm_of_pos {n : ℕ} (hn : 0 < n) :
    baselTerm n = 1 / (n : ℝ) ^ 2 := by
  simp [baselTerm, Nat.ne_of_gt hn]

/-- The excluded zero placeholder agrees with Lean's totalized division, so the
function matches the summand used by mathlib's zeta theorem. -/
theorem baselTerm_eq_zeta_summand (n : ℕ) :
    baselTerm n = 1 / (n : ℝ) ^ 2 := by
  by_cases hn : n = 0
  · subst n
    simp [baselTerm]
  · simp [baselTerm, hn]

/-- Endliche klassische Partialsumme von `1` bis `N`. -/
noncomputable def baselPartialSum (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 N, baselTerm n

/-- Der Summand für das symmetrische Paar `{-n,n}`. -/
noncomputable def signedPairTerm (n : ℕ) : ℝ :=
  baselTerm n + baselTerm n

@[simp] theorem signedPairTerm_eq_two_mul (n : ℕ) :
    signedPairTerm n = 2 * baselTerm n := by
  simp [signedPairTerm, two_mul]

/-- Symmetrische Partialsumme über die Paare `±1,…,±N`. -/
noncomputable def bilateralPartialSum (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 N, signedPairTerm n

theorem bilateralPartialSum_eq_two_mul (N : ℕ) :
    bilateralPartialSum N = 2 * baselPartialSum N := by
  simp [bilateralPartialSum, baselPartialSum, Finset.mul_sum]

/-- Der formalisierte Basel-Satz. -/
theorem basel_hasSum :
    HasSum baselTerm (Real.pi ^ 2 / 6) := by
  exact hasSum_zeta_two.congr_fun (fun n => baselTerm_eq_zeta_summand n)

theorem basel_tsum :
    ∑' n : ℕ, baselTerm n = Real.pi ^ 2 / 6 :=
  basel_hasSum.tsum_eq

/-- Durch die Paarung positiver und negativer Indizes verdoppelt sich der
Grenzwert der Reihe über `ℤ \ {0}`. -/
theorem bilateral_hasSum :
    HasSum signedPairTerm (Real.pi ^ 2 / 3) := by
  have h := basel_hasSum.mul_left 2
  have h' : HasSum signedPairTerm (2 * (Real.pi ^ 2 / 6)) := by
    exact h.congr_fun (fun n => signedPairTerm_eq_two_mul n)
  have hvalue : 2 * (Real.pi ^ 2 / 6) = Real.pi ^ 2 / 3 := by ring
  rw [← hvalue]
  exact h'

example : baselPartialSum 1 = 1 := by
  norm_num [baselPartialSum, baselTerm]

example : baselPartialSum 2 = 5 / 4 := by
  norm_num [baselPartialSum, baselTerm, Finset.sum_Icc_succ_top]

end MathVizLab
