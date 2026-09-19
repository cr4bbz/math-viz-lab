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

/-! ## Freier Exponent

Für den reellen Exponenten `s` indexieren wir durch `k=n-1`. Dadurch ist die
Höhe immer positiv (`n=k+1`) und die Fasermultiplizität genau `k`.
-/

/-- Punktgewicht `1/(k+1)^s` in der für reelle Exponenten geeigneten
`rpow`-Schreibweise. -/
noncomputable def powerPointTerm (s : ℝ) (k : ℕ) : ℝ :=
  ((k + 1 : ℕ) : ℝ) ^ (-s)

/-- Gesamtgewicht einer Faser der Höhe `k+1` mit `k` Punkten. -/
noncomputable def powerFiberTerm (s : ℝ) (k : ℕ) : ℝ :=
  (k : ℝ) * powerPointTerm s k

/-- Die ungewichtete Potenzreihe über positive Höhen ist genau für `s>1`
summierbar. -/
theorem powerPointTerm_summable_iff (s : ℝ) :
    Summable (powerPointTerm s) ↔ 1 < s := by
  unfold powerPointTerm
  have hshift :
      (Summable (fun k : ℕ ↦ (((k + 1 : ℕ) : ℝ) ^ (-s)))) ↔
        Summable (fun n : ℕ ↦ (n : ℝ) ^ (-s)) := by
    simpa using
      (summable_nat_add_iff (f := fun n : ℕ ↦ (n : ℝ) ^ (-s)) 1)
  rw [hshift, Real.summable_nat_rpow]
  constructor <;> intro h <;> linarith

/-- Die Fasermultiplizität senkt den effektiven Exponenten von `s` auf
`s-1`. -/
theorem powerFiberTerm_decomposition (s : ℝ) (k : ℕ) :
    powerFiberTerm s k =
      (((k + 1 : ℕ) : ℝ) ^ (1 - s) - ((k + 1 : ℕ) : ℝ) ^ (-s)) := by
  have hpos : 0 < (((k + 1 : ℕ) : ℝ)) := by positivity
  rw [powerFiberTerm, powerPointTerm]
  have hk : (k : ℝ) = ((k + 1 : ℕ) : ℝ) - 1 := by norm_num
  rw [hk, sub_mul, one_mul]
  rw [show 1 - s = 1 + (-s) by ring, Real.rpow_add hpos, Real.rpow_one]

/-- Für `s>2` ist die gewichtete Faserreihe summierbar. -/
theorem powerFiberTerm_summable_of_two_lt {s : ℝ} (hs : 2 < s) :
    Summable (powerFiberTerm s) := by
  have hlead0 : Summable (fun n : ℕ ↦ (n : ℝ) ^ (1 - s)) :=
    Real.summable_nat_rpow.mpr (by linarith)
  have htail0 : Summable (fun n : ℕ ↦ (n : ℝ) ^ (-s)) :=
    Real.summable_nat_rpow.mpr (by linarith)
  have hlead : Summable (fun k : ℕ ↦ (((k + 1 : ℕ) : ℝ) ^ (1 - s))) :=
    (summable_nat_add_iff 1).2 hlead0
  have htail : Summable (fun k : ℕ ↦ (((k + 1 : ℕ) : ℝ) ^ (-s))) :=
    (summable_nat_add_iff 1).2 htail0
  exact (hlead.sub htail).congr fun k ↦ (powerFiberTerm_decomposition s k).symm

/-- Im Übergangsbereich `1<s≤2` konvergiert die ursprüngliche Potenzreihe,
die gewichtete Faserreihe dagegen nicht. -/
theorem powerFiberTerm_not_summable_of_one_lt_le_two {s : ℝ}
    (h1 : 1 < s) (h2 : s ≤ 2) :
    ¬ Summable (powerFiberTerm s) := by
  intro hfiber
  have htail0 : Summable (fun n : ℕ ↦ (n : ℝ) ^ (-s)) :=
    Real.summable_nat_rpow.mpr (by linarith)
  have htail : Summable (fun k : ℕ ↦ (((k + 1 : ℕ) : ℝ) ^ (-s))) :=
    (summable_nat_add_iff 1).2 htail0
  have hlead : Summable (fun k : ℕ ↦ (((k + 1 : ℕ) : ℝ) ^ (1 - s))) := by
    refine (hfiber.add htail).congr ?_
    intro k
    rw [powerFiberTerm_decomposition]
    ring
  have hlead0 : Summable (fun n : ℕ ↦ (n : ℝ) ^ (1 - s)) :=
    (summable_nat_add_iff 1).1 hlead
  have hexponent : 1 - s < -1 := Real.summable_nat_rpow.mp hlead0
  linarith

/-- Innerhalb des Bereichs, in dem die Punktreihe bereits konvergiert, liegt
die exakte Konvergenzschwelle der Faserreihe bei `s=2`. -/
theorem powerFiberTerm_summable_iff_of_one_lt {s : ℝ} (h1 : 1 < s) :
    Summable (powerFiberTerm s) ↔ 2 < s := by
  constructor
  · intro hsummable
    by_contra hnot
    exact powerFiberTerm_not_summable_of_one_lt_le_two h1 (le_of_not_gt hnot)
      hsummable
  · exact powerFiberTerm_summable_of_two_lt

example : fullFiberMass 5 = 4 / 25 := by
  norm_num [fullFiberMass, baselTerm]

example : visibleFiberMass 16 11 = 10 / 121 := by
  norm_num [visibleFiberMass, visibleHeightCardinality,
    visibleHeightCoordinates, baselTerm]

end MathVizLab
