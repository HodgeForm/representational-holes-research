import Mathlib

theorem erdos_242_even (k : ℕ) :
    ∃ x y z : ℕ,
      1 ≤ x ∧ x < y ∧ y < z ∧
      (4 / (2 * (k + 2)) : ℚ) =
        1 / x + 1 / y + 1 / z := by
  refine ⟨k + 2, k + 3, (k + 2) * (k + 3),
    by omega, by omega, ?_, ?_⟩
  · nlinarith [Nat.zero_le (k * k)]
  · push_cast
    field_simp <;> ring <;> positivity
