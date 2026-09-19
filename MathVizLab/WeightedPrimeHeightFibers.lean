import MathVizLab.PrimeHeightGeometry
import MathVizLab.BaselProblem
import Mathlib.NumberTheory.SumPrimeReciprocals
import Mathlib.Tactic

/-!
# Basel-Gewichte auf Primhöhenfasern

Dieses zusammengesetzte Experiment versieht jeden Punkt der positiven
Höhenfaser `a+b=n` mit dem Basel-Gewicht `1/n²`. Die Fasermultiplizität
`n-1` ändert damit den Beitrag eines Höhenindex zu `(n-1)/n²`.
-/

namespace MathVizLab

/-- Gesamtgewicht einer vollständigen positiven Höhenfaser mit Index `n`. -/
noncomputable def fullFiberMass (n : ℕ) : ℝ :=
  ((n - 1 : ℕ) : ℝ) * baselTerm n

/-- Im endlichen Fenster sichtbares Gewicht der Höhenfaser `n`. -/
noncomputable def visibleFiberMass (N n : ℕ) : ℝ :=
  (visibleHeightCardinality N n : ℝ) * baselTerm n

/-- Endliche Summe der vollständigen Fasergewichte. -/
noncomputable def fiberMassPartialSum (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 N, fullFiberMass n

/-- Endliche harmonische Vergleichssumme auf demselben Indexintervall. -/
noncomputable def reciprocalPartialSum (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.Icc 1 N, (1 : ℝ) / n

/-- Solange die Faser vollständig sichtbar ist, stimmt ihr sichtbares Gewicht
mit dem Gewicht der vollen Faser überein. -/
theorem visibleFiberMass_of_complete {N n : ℕ}
    (h : CompleteHeightFiber N n) :
    visibleFiberMass N n = fullFiberMass n := by
  rw [visibleFiberMass, fullFiberMass, visibleHeightCardinality_of_complete h]

/-- Die Fasermasse zerlegt sich in einen harmonischen und einen quadratisch
abfallenden Anteil. -/
theorem fullFiberMass_eq_one_div_sub_one_div_sq {n : ℕ} (hn : 1 ≤ n) :
    fullFiberMass n = 1 / (n : ℝ) - 1 / (n : ℝ) ^ 2 := by
  rw [fullFiberMass, baselTerm_of_pos (by omega), Nat.cast_sub hn]
  have hn0 : (n : ℝ) ≠ 0 := by positivity
  field_simp
  ring

/-- Auf jedem endlichen Intervall ist die gewichtete Fasermassensumme exakt
die harmonische Partialsumme minus der Basel-Partialsumme. -/
theorem fiberMassPartialSum_eq_reciprocal_sub_basel (N : ℕ) :
    fiberMassPartialSum N = reciprocalPartialSum N - baselPartialSum N := by
  unfold fiberMassPartialSum reciprocalPartialSum baselPartialSum
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro n hn
  simpa [baselTerm_eq_zeta_summand] using
    fullFiberMass_eq_one_div_sub_one_div_sq (Finset.mem_Icc.mp hn).1

/-- Bereits die Reihe über alle vollständigen Höhenfasern ist nicht
summierbar. -/
theorem fullFiberMass_not_summable : ¬ Summable fullFiberMass := by
  intro hmass
  have hreciprocal : Summable (fun n : ℕ ↦ (1 : ℝ) / n) := by
    have hadd := hmass.add hasSum_zeta_two.summable
    refine hadd.congr ?_
    intro n
    cases n with
    | zero => simp [fullFiberMass, baselTerm]
    | succ n =>
        rw [fullFiberMass_eq_one_div_sub_one_div_sq (Nat.succ_pos n)]
        ring
  exact Real.not_summable_one_div_natCast hreciprocal

/-- Die gewichteten vollen Primhöhenfasern bilden keine summierbare Reihe.
Die Fasermultiplizität verwandelt den Basel-Abfall in einen harmonischen
Hauptterm. -/
theorem prime_fullFiberMass_not_summable :
    ¬ Summable (fun p : Nat.Primes ↦ fullFiberMass p) := by
  intro hmass
  have hsquare : Summable (fun p : Nat.Primes ↦ (1 : ℝ) / (p : ℝ) ^ 2) := by
    exact hasSum_zeta_two.summable.subtype Nat.Prime
  have hreciprocal : Summable (fun p : Nat.Primes ↦ (1 : ℝ) / (p : ℝ)) := by
    have hadd := hmass.add hsquare
    refine hadd.congr ?_
    intro p
    rw [fullFiberMass_eq_one_div_sub_one_div_sq (Nat.Prime.one_le p.property)]
    ring
  exact Nat.Primes.not_summable_one_div hreciprocal

example : fullFiberMass 5 = 4 / 25 := by
  norm_num [fullFiberMass, baselTerm]

example : visibleFiberMass 16 11 = 10 / 121 := by
  norm_num [visibleFiberMass, visibleHeightCardinality,
    visibleHeightCoordinates, baselTerm]

end MathVizLab
