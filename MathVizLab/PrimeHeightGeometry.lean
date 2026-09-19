import Mathlib.Analysis.Real.Sqrt
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Tactic

/-!
# Primhöhen als diagonale Fasern

Dieses Experiment adaptiert die Primhöhen-Geometrie aus dem Schwesterprojekt
`math-lab`. Auf dem positiven Gitter wird die Höhenprojektion
`(a,b) ↦ a+b` untersucht. Ihre Fasern sind Diagonalen; Primzahlen wählen daraus
bestimmte Bänder aus, und Differenzen ihrer Höhenindizes sind Primzahllücken.
-/

namespace MathVizLab

/-- Additive Höhe eines Gitterpunkts. -/
def height (a b : ℕ) : ℕ := a + b

/-- Ein Gitterpunkt hat Primhöhe, wenn sein Höhenindex prim ist. -/
def PrimeHeight (a b : ℕ) : Prop := Nat.Prime (height a b)

@[simp] theorem height_swap (a b : ℕ) : height a b = height b a := by
  simp [height, Nat.add_comm]

theorem primeHeight_swap {a b : ℕ} : PrimeHeight a b ↔ PrimeHeight b a := by
  simp [PrimeHeight]

theorem primeHeight_of_sum_eq {a b p : ℕ} (hp : Nat.Prime p)
    (h : a + b = p) : PrimeHeight a b := by
  simpa [PrimeHeight, height, h] using hp

/-- Sichtbare `a`-Koordinaten der Höhenfaser `a+b=n` im Fenster `1 ≤ a,b ≤ N`. -/
def visibleHeightCoordinates (N n : ℕ) : Finset ℕ :=
  Finset.Icc (max 1 (n - N)) (min N (n - 1))

/-- Anzahl sichtbarer Gitterpunkte einer Höhenfaser. -/
def visibleHeightCardinality (N n : ℕ) : ℕ :=
  (visibleHeightCoordinates N n).card

/-- Eine Faser ist vollständig sichtbar, solange `2 ≤ n ≤ N+1`. -/
def CompleteHeightFiber (N n : ℕ) : Prop := 2 ≤ n ∧ n ≤ N + 1

theorem visibleHeightCardinality_eq_interval (N n : ℕ) :
    visibleHeightCardinality N n =
      min N (n - 1) + 1 - max 1 (n - N) := by
  simp [visibleHeightCardinality, visibleHeightCoordinates, Nat.card_Icc]

/-- Eine vollständige positive Höhenfaser enthält genau `n-1` Punkte. -/
theorem visibleHeightCardinality_of_complete {N n : ℕ}
    (h : CompleteHeightFiber N n) :
    visibleHeightCardinality N n = n - 1 := by
  rcases h with ⟨h2, hupper⟩
  have hmin : min N (n - 1) = n - 1 := by
    apply min_eq_right
    omega
  have hmax : max 1 (n - N) = 1 := by
    apply max_eq_left
    omega
  rw [visibleHeightCardinality_eq_interval, hmin, hmax]
  omega

/-- Nach der Vollständigkeitsschwelle schrumpft die sichtbare Faser linear. -/
theorem visibleHeightCardinality_of_truncated {N n : ℕ}
    (hlo : N + 1 < n) (hhi : n ≤ 2 * N) :
    visibleHeightCardinality N n = 2 * N - n + 1 := by
  have hmin : min N (n - 1) = N := by
    apply min_eq_left
    omega
  have hmax : max 1 (n - N) = n - N := by
    apply max_eq_right
    omega
  rw [visibleHeightCardinality_eq_interval, hmin, hmax]
  omega

/-- Abstand zweier Bänder in ganzzahligen Höhenindizes. -/
def bandGap (p q : ℕ) : ℕ := q - p

/-- Anzahl der Höhenbänder, die strikt zwischen zwei Indizes liegen. -/
def separatorCount (p q : ℕ) : ℕ := bandGap p q - 1

/-- Abgesehen von `2` sind Abstände zwischen Primhöhen gerade. -/
theorem primeBand_gap_even {p q : ℕ}
    (hp : Nat.Prime p) (hq : Nat.Prime q)
    (hp2 : p ≠ 2) (hq2 : q ≠ 2) (hpq : p < q) :
    Even (bandGap p q) := by
  rcases hp.odd_of_ne_two hp2 with ⟨a, ha⟩
  rcases hq.odd_of_ne_two hq2 with ⟨b, hb⟩
  refine ⟨b - a, ?_⟩
  simp only [bandGap]
  omega

/-- Die im Bild gewählten Primhöhen `11` und `13` haben Lücke zwei und
genau ein dazwischenliegendes Höhenband. -/
theorem eleven_thirteen_prime_gap :
    Nat.Prime 11 ∧ Nat.Prime 13 ∧
      bandGap 11 13 = 2 ∧ separatorCount 11 13 = 1 := by
  norm_num [bandGap, separatorCount]

/-- Orthogonale Lage des Bandes `a+b=n` auf seiner Einheitsnormalen. -/
noncomputable def bandNormalCoordinate (n : ℕ) : ℝ := n / Real.sqrt 2

/-- Die euklidische Distanz der parallelen Geraden `a+b=11` und `a+b=13`
ist `√2`; sie ist nicht mit der ganzzahligen Primzahllücke `2` identisch. -/
theorem bandNormalDistance_eleven_thirteen :
    bandNormalCoordinate 13 - bandNormalCoordinate 11 = Real.sqrt 2 := by
  have hsqrt : (Real.sqrt 2) ^ 2 = (2 : ℝ) := by
    exact Real.sq_sqrt (by norm_num)
  have hne : Real.sqrt 2 ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (by norm_num))
  unfold bandNormalCoordinate
  calc
    (13 : ℝ) / Real.sqrt 2 - (11 : ℝ) / Real.sqrt 2 =
        (2 : ℝ) / Real.sqrt 2 := by ring
    _ = Real.sqrt 2 := by
      apply (div_eq_iff hne).2
      rw [← pow_two]
      exact hsqrt.symm

example : visibleHeightCardinality 16 11 = 10 := by
  norm_num [visibleHeightCardinality, visibleHeightCoordinates]

example : visibleHeightCardinality 16 19 = 14 := by
  norm_num [visibleHeightCardinality, visibleHeightCoordinates]

end MathVizLab
