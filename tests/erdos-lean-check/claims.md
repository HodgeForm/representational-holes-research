# Claims extracted from ChatGPT conversation
Source: https://chatgpt.com/c/6ad22b63-9ddc-83ea-823b-0d1c55c1f3e3 (title "Training status report")
Extracted: 2026-10-16 ~10:15 (UTC-4), read-only except for one accidental message (see Note 0).

## Note 0 — Accidental message sent (IMPORTANT)
While trying to paste code into a terminal, a stray Computer keystroke sequence typed the text
`cat > block_01.lean` into the ChatGPT composer and it was SENT as a new user message in this conversation.
ChatGPT then generated a new reply (not part of the original answer). I clicked Stop and did not delete anything.
The stray user message and the new reply remain in the conversation; the user should decide whether to delete them.
The new reply contains a Bash block (`cat > block_01.lean <<'EOF' ... EOF`) with a Lean snippet and
the text "UNCHECKED: awaiting Lean verification." It is NOT one of the original Lean blocks and was not extracted as a block_NN file.

## Structure of the original assistant response (all visible text)
- Section 1: "Hodge Native — Task 2 status" — "Training comparison not yet verified"
- Section 2: "Erdős–Straus problem #242 — Lean 4 candidates" — "All proofs unverified"
- Section 3: "What remains genuinely difficult?"
- Section 4: "Theorem extraction summary" — "All five are UNCHECKED: awaiting Lean verification."
- Final checkpoint paragraph.
- A "View analysis" panel contains a Python block (not Lean; not saved) that checks the 5 families over ranges with Fraction.
  Its STDOUT/STDERR shows: even True / 3mod4 True / 2mod3 True / 0mod4 True / 0mod3 True.

## Claims about what was proved (quoted verbatim from the original response)

1. "I recovered the prior Hodge Native v0.2 benchmark result and checked the connected HodgeForm workspace, but could not recover the actual trained checkpoint, frozen fresh-evaluation dataset, or complete matched training artifacts."
2. "The previous conversation contains a report that both architectures had been trained across three seeds. However, that report does not provide the individual scores, executable checkpoints, or evaluation receipts needed to substantiate the comparison."
3. "Verdict: No demonstrated improvement over the simple baseline. The existing reported neural result is one question worse, and there is no verified three-seed evidence establishing superiority outside the noise."
4. "The statistical comparison remains incomplete: mean ± standard deviation across three seeds, paired error analysis, and uncertainty in the difference from 53/60 cannot yet be reported responsibly."
5. "All proofs unverified" (section heading) / "The following are standalone Lean candidates using Mathlib. They use no sorry, admit, axiom, or native_decide. I did not have an installed Lean 4/Mathlib v4.19.0 checker, so none has a compiler verification receipt."
6. "The official Formal Conjectures statement is currently classified as open."
7. "UNCHECKED: awaiting Lean verification" — label on Theorems 1–5 (also "All five are UNCHECKED: awaiting Lean verification.")
8. "I checked the explicit witness formulas independently using Python's exact rational arithmetic for the first 100 values of each parameter k. All five families passed the strict ordering and fraction-equality checks."
9. "That is an additional finite arithmetic check, not a Lean verification."
10. "The constructions are standard elementary Egyptian-fraction identities, not novel mathematical discoveries."
11. Table (section 3): Even n — "All even n > 2 — Known identity"; n ≡ 3 (mod 4) — "Entire residue class — Known identity"; n ≡ 2 (mod 3) — "All such n > 2 — Known identity"; n ≡ 0 (mod 4) — "Subset of even n — Known identity"; n ≡ 0 (mod 3) — "All multiples of 3 above 2 — Known identity".
12. "The important remaining territory includes odd n ≡ 1 (mod 4) not divisible by 3 and not congruent to 2 modulo 3—in particular: n ≡ 1 (mod 12)"
13. "This does not mean every number in that class is unresolved individually. It means these five constructions do not establish the conjecture for the entire class."
14. "The original open conjecture remains unsolved." (Final checkpoint) — also "Five Erdős–Straus Lean candidates have been written and their witness formulas passed finite exact-arithmetic checks, but none has been Lean-verified."
15. "Final checkpoint: Hodge Native has no demonstrated advantage over 53/60; the three-seed training comparison remains unverified because the frozen artifacts are unavailable."

Note on the (sloppy) claims in the response: Theorem 4 (mod4_eq0) is described as "a specialization of the even-integer construction". Theorem 5 is labelled "Harder coverage" but its family is n = 3(k+1), i.e. multiples of 3, which the response's own table lists as "Known identity".

## Hodge Native training results (verbatim from the table, original response)
| Condition | Reported score | Status |
|---|---|---|
| Simple baseline | 53/60 (88.3%) | Historical reference |
| Hodge Native v0.2 | 52/60 (86.7%) | Historical reference |
| Matched model A, 3 seeds | — | No verified results |
| Matched model B, 3 seeds | — | No verified results |
- The response says the 3-seed training comparison is NOT verified; no mean ± spread across seeds is reported; no per-seed scores, checkpoints or eval receipts were available.
- Verdict quoted: "No demonstrated improvement over the simple baseline."

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
  clipboard paste was not completed (no text editor was available and the attempt caused the stray message in Note 0).
- Block 1 as rendered reads `field_simp  ring  positivity` (the `<;>` operators are absent from the rendered DOM text),
  whereas blocks 2–5 contain `field_simp <;> ring <;> positivity`. Block 1 as saved is therefore likely NOT the same as the
  source intended; it probably does not compile as written. Verify against the original text (or the copy button) before use.
- Theorem statements in the blocks use `(4 / (2 * (k + 2)) : ℚ)` etc. — i.e. the ℚ-division form, not the `4/n` in the target text.
