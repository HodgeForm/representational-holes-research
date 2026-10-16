# Erdős #242 Lean check (Lean 4.19.0 + Mathlib, 2026-10-16 ET)
Official statement (official_242.lean, formal-conjectures main): `∀ n > 2, ∃ x y z : ℕ, 1 ≤ x ∧ x < y ∧ y < z ∧ (4/n : ℚ) = 1/x+1/y+1/z`. It is still open and marked `sorry` upstream.

| File | Compiles | sorry/admit/axiom/native_decide | Axioms | Verdict |
|---|---|---|---|---|
| block_01.lean (as saved) | NO: unsolved goal `4*((k+2)*(k+3)) = (k+3+(k+2)+1)*(2*(k+2))`, then `unexpected identifier; expected command` at 12:16 | none in the source (the failure adds sorryAx) | propext, sorryAx, Classical.choice, Quot.sound | FAIL |
| block_01_fixed.lean (`<;>` restored) | yes (linter warnings only) | none | propext, Classical.choice, Quot.sound | PASS |
| block_02.lean | yes | none | standard 3 | PASS |
| block_03.lean | yes | none | standard 3 | PASS |
| block_04.lean | yes | none | standard 3 | PASS |
| block_05.lean | yes | none | standard 3 | PASS |

## How each one differs from the official statement
The conclusion has the same shape in every block. Each one replaces `n` (with `2 < n`) by a fixed parametrisation in k : ℕ:
- 01: n = 2(k+2), so even n ≥ 4. Witnesses (k+2, k+3, (k+2)(k+3)).
- 02: n = 4k+3, so n ≡ 3 (mod 4), n ≥ 3. Witnesses (k+1, m+1, m(m+1)) with m = (4k+3)(k+1).
- 03: n = 3k+5, so n ≡ 2 (mod 3), n ≥ 5. Witnesses (k+2, 3k+5, (3k+5)(k+2)).
- 04: n = 4(k+1), so n ≡ 0 (mod 4), n ≥ 4. This is already covered by 01.
- 05: n = 3(k+1), so n ≡ 0 (mod 3), n ≥ 3.

## Coverage
Together, the blocks cover every n > 2 except n ≡ 1 (mod 12). That case needs n odd and not ≡ 3 (mod 4), so n ≡ 1 (mod 4), and also n not ≡ 0 or 2 (mod 3), so n ≡ 1 (mod 3). A brute-force check over 3..199 finds exactly the uncovered n = 13, 25, 37, 49, 61, 73, ... (all ≡ 1 mod 12). This is the hard core of the problem, which includes the primes ≡ 1 (mod 12) and is related to Erdős–Straus-type difficulty. **Erdős #242 is NOT proved.**
Receipts: ledger.jsonl. Raw Lean outputs: ax/*.out.
