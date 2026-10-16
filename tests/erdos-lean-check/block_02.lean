import Mathlib

theorem erdos_242_mod4_eq3 (k : ℕ) :
    ∃ x y z : ℕ,
      1 ≤ x ∧ x < y ∧ y < z ∧
      (4 / (4 * k + 3) : ℚ) =
        1 / x + 1 / y + 1 / z := by
  let a : ℕ := k + 1
  let m : ℕ := (4 * k + 3) * a
  have ha : 0 < a := by
    dsimp [a]
    omega
  have hm : 1 < m := by
    dsimp [m, a]
    nlinarith [Nat.zero_le (k * k)]
  refine ⟨a, m + 1, m * (m + 1),
    by omega, ?_, ?_, ?_⟩
  · dsimp [a, m]
    nlinarith [Nat.zero_le (k * k)]
  · nlinarith [Nat.zero_le (m * m)]
  · dsimp [a, m]
    push_cast
    field_simp <;> ring <;> positivity
