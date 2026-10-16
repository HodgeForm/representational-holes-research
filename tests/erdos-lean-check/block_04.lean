import Mathlib

theorem erdos_242_mod4_eq0 (k : ℕ) :
    ∃ x y z : ℕ,
      1 ≤ x ∧ x < y ∧ y < z ∧
      (4 / (4 * (k + 1)) : ℚ) =
        1 / x + 1 / y + 1 / z := by
  refine ⟨2 * (k + 1), 2 * (k + 1) + 1,
    (2 * (k + 1)) * (2 * (k + 1) + 1),
    by omega, by omega, ?_, ?_⟩
  · nlinarith [Nat.zero_le (k * k)]
  · push_cast
    field_simp <;> ring <;> positivity
