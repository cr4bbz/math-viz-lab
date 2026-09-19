import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic

/-!
# Die kubische Familie `x³ - a·x`

Diese Datei formalisiert die Aussagen, die in der ersten interaktiven
Visualisierung des math-viz-lab gezeigt werden. Wir untersuchen die Nullstellenmenge

`V = {(a, x) | x³ - a·x = 0}`

und ihre beiden Koordinatenprojektionen. Die Projektion auf `a` liefert für jedes
`a` die Nullstellen des Polynoms. Die Projektion auf `x` zeigt bei `x = 0` eine
außergewöhnlich große Faser.
-/

namespace MathVizLab

/-- Die parametrisierte kubische Funktion, deren Fasern wir untersuchen. -/
def cubicFamily (a x : ℝ) : ℝ := x ^ 3 - a * x

/-- Algebraische Normalform der Nullstellenbedingung: `x = 0` oder `x² = a`. -/
theorem cubicFamily_eq_zero_iff (a x : ℝ) :
    cubicFamily a x = 0 ↔ x = 0 ∨ x ^ 2 = a := by
  unfold cubicFamily
  have hfactor : x ^ 3 - a * x = x * (x ^ 2 - a) := by ring
  rw [hfactor, mul_eq_zero]
  constructor
  · rintro (hx | hrest)
    · exact Or.inl hx
    · exact Or.inr (sub_eq_zero.mp hrest)
  · rintro (hx | hsq)
    · exact Or.inl hx
    · exact Or.inr (sub_eq_zero.mpr hsq)

/-- Für negative Parameter besteht die `a`-Faser nur aus der Nullstelle `0`. -/
theorem parameterFiber_of_neg {a : ℝ} (ha : a < 0) :
    {x : ℝ | cubicFamily a x = 0} = ({0} : Set ℝ) := by
  ext x
  rw [Set.mem_ofPred_eq, Set.mem_singleton_iff, cubicFamily_eq_zero_iff]
  constructor
  · rintro (hx | hsq)
    · exact hx
    · nlinarith [sq_nonneg x]
  · intro hx
    exact Or.inl hx

/-- Am kritischen Parameter `a = 0` fallen alle drei algebraischen Äste zusammen. -/
theorem parameterFiber_at_zero :
    {x : ℝ | cubicFamily 0 x = 0} = ({0} : Set ℝ) := by
  ext x
  simp only [Set.mem_ofPred_eq, Set.mem_singleton_iff, cubicFamily_eq_zero_iff]
  constructor
  · rintro (hx | hsq)
    · exact hx
    · nlinarith [sq_nonneg x]
  · intro hx
    exact Or.inl hx

/-- Für `a > 0` hat die `a`-Faser genau die drei sichtbaren Punkte
`0`, `√a` und `-√a`. -/
theorem parameterFiber_of_pos {a : ℝ} (ha : 0 < a) :
    {x : ℝ | cubicFamily a x = 0} =
      ({0, Real.sqrt a, -Real.sqrt a} : Set ℝ) := by
  have ha0 : 0 ≤ a := le_of_lt ha
  have hsqrt0 : 0 ≤ Real.sqrt a := Real.sqrt_nonneg a
  have hsqrt_sq : (Real.sqrt a) ^ 2 = a := Real.sq_sqrt ha0
  ext x
  simp only [Set.mem_ofPred_eq, Set.mem_insert_iff, Set.mem_singleton_iff,
    cubicFamily_eq_zero_iff]
  constructor
  · rintro (hx | hsq)
    · exact Or.inl hx
    · right
      by_cases hxnonneg : 0 ≤ x
      · left
        nlinarith
      · right
        nlinarith
  · rintro (hx | hx | hx)
    · exact Or.inl hx
    · right
      nlinarith
    · right
      nlinarith

/-- Über dem Zustand `x = 0` liegt die gesamte Parameterachse: eine
außergewöhnliche Faser der Projektion auf `x`. -/
theorem stateFiber_at_zero :
    {a : ℝ | cubicFamily a 0 = 0} = Set.univ := by
  ext a
  simp [cubicFamily]

/-- Für jeden Zustand `x ≠ 0` besteht die `x`-Faser aus genau einem Parameter,
nämlich `a = x²`. -/
theorem stateFiber_of_ne_zero {x : ℝ} (hx : x ≠ 0) :
    {a : ℝ | cubicFamily a x = 0} = ({x ^ 2} : Set ℝ) := by
  ext a
  simp [cubicFamily_eq_zero_iff, hx, eq_comm]

/-- Der positive Fall enthält tatsächlich drei paarweise verschiedene Punkte. -/
theorem positive_roots_are_distinct {a : ℝ} (ha : 0 < a) :
    (0 : ℝ) ≠ Real.sqrt a ∧
      (0 : ℝ) ≠ -Real.sqrt a ∧
      Real.sqrt a ≠ -Real.sqrt a := by
  have hsqrt : 0 < Real.sqrt a := Real.sqrt_pos.2 ha
  constructor
  · nlinarith
  · constructor <;> nlinarith

end MathVizLab
