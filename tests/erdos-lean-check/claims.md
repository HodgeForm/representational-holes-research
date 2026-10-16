# Claims extracted from the ChatGPT session
Source: Derek's ChatGPT session (private conversation; not linked).
Extracted: 2026-10-16 ~10:15 (UTC-4).

## Structure of the original assistant response (Erdős-relevant parts)
- An earlier section on an unrelated topic (omitted here).
- Section 2: "Erdős–Straus problem #242 — Lean 4 candidates" — "All proofs unverified"
- Section 3: "What remains genuinely difficult?"
- Section 4: "Theorem extraction summary" — "All five are UNCHECKED: awaiting Lean verification."
- Final checkpoint paragraph.
- A "View analysis" panel contains a Python block (not Lean; not saved) that checks the 5 families over ranges with Fraction.
  Its STDOUT/STDERR shows: even True / 3mod4 True / 2mod3 True / 0mod4 True / 0mod3 True.

## Claims about what was proved (quoted verbatim from the original response)

1. "All proofs unverified" (section heading) / "The following are standalone Lean candidates using Mathlib. They use no sorry, admit, axiom, or native_decide. I did not have an installed Lean 4/Mathlib v4.19.0 checker, so none has a compiler verification receipt."
2. "The official Formal Conjectures statement is currently classified as open."
3. "UNCHECKED: awaiting Lean verification" — label on Theorems 1–5 (also "All five are UNCHECKED: awaiting Lean verification.")
4. "I checked the explicit witness formulas independently using Python's exact rational arithmetic for the first 100 values of each parameter k. All five families passed the strict ordering and fraction-equality checks."
5. "That is an additional finite arithmetic check, not a Lean verification."
6. "The constructions are standard elementary Egyptian-fraction identities, not novel mathematical discoveries."
7. Table (section 3): Even n — "All even n > 2 — Known identity"; n ≡ 3 (mod 4) — "Entire residue class — Known identity"; n ≡ 2 (mod 3) — "All such n > 2 — Known identity"; n ≡ 0 (mod 4) — "Subset of even n — Known identity"; n ≡ 0 (mod 3) — "All multiples of 3 above 2 — Known identity".
8. "The important remaining territory includes odd n ≡ 1 (mod 4) not divisible by 3 and not congruent to 2 modulo 3—in particular: n ≡ 1 (mod 12)"
9. "This does not mean every number in that class is unresolved individually. It means these five constructions do not establish the conjecture for the entire class."
10. "The original open conjecture remains unsolved." (Final checkpoint) — also "Five Erdős–Straus Lean candidates have been written and their witness formulas passed finite exact-arithmetic checks, but none has been Lean-verified."

Note on the (sloppy) claims in the response: Theorem 4 (mod4_eq0) is described as "a specialization of the even-integer construction". Theorem 5 is labelled "Harder coverage" but its family is n = 3(k+1), i.e. multiples of 3, which the response's own table lists as "Known identity".

## Erdős–Straus Lean blocks and their statements (theorem statement = `P(n)` from 242.lean, per response)
Target (quoted in response): for every n > 2, 4/n = 1/x + 1/y + 1/z with 1 ≤ x < y < z naturals.

| Block | Theorem name | Family | Witness (per response) | Lean status |
|---|---|---|---|---|
| block_01.lean | erdos_242_even | n = 2(k+2) | x=k+2, y=k+3, z=(k+2)(k+3) | UNCHECKED |
| block_02.lean | erdos_242_mod4_eq3 | n = 4k+3 | a=k+1, m=n·a, witnesses a, m+1, m(m+1) | UNCHECKED |
| block_03.lean | erdos_242_mod3_eq2 | n = 3k+5 | x=k+2, y=3k+5, z=(3k+5)(k+2) | UNCHECKED |
| block_04.lean | erdos_242_mod4_eq0 | n = 4(k+1) | x=2(k+1), y=2(k+1)+1, z=xy | UNCHECKED |
| block_05.lean | erdos_242_mod3_eq0 | n = 3(k+1) | x=k+1, y=3(k+1)+1, z=3(k+1)(3(k+1)+1) | UNCHECKED |

Common statement shape in every block:
`∃ x y z : ℕ, 1 ≤ x ∧ x < y ∧ y < z ∧ (4 / n : ℚ) = 1 / x + 1 / y + 1 / z`

Each block's text is the DOM text of the rendered code element (see "Extraction method" below).
None of these has been compiled. The response itself says no Lean/Mathlib checker was available.

## Extraction method and caveats
- Blocks were taken from the rendered code elements' text (exact DOM text), NOT from the "Copy code" buttons:
  clipboard paste was not used.
- Block 1 as rendered reads `field_simp  ring  positivity` (the `<;>` operators are absent from the rendered DOM text),
  whereas blocks 2–5 contain `field_simp <;> ring <;> positivity`. Block 1 as saved is therefore likely NOT the same as the
  source intended; it probably does not compile as written. Verify against the original text (or the copy button) before use.
- Theorem statements in the blocks use `(4 / (2 * (k + 2)) : ℚ)` etc. — i.e. the ℚ-division form, not the `4/n` in the target text.
