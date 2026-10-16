# RESULTS — loop summary-or-abstain benchmark (prereg sha256 3957a594…4666)
Seed 20261016, 160 tasks (115 in-representation, 45 out), n = 10^3..10^18, 2.0 s/task budget, plain Python big ints.
Ground truth: independent interpreter (verify.py), exact simulation for n<=10^5, else parity-class exact polynomial interpolation
with 2 held-out check points (all checks passed). Out-of-rep tasks with n>10^5 have no truth: correct = abstain.

| Method | In-rep exact | Out-of-rep handled OK | WRONG | Median time | Peak mem |
|---|---|---|---|---|---|
| M summary-or-abstain | 115/115 | 45/45 | **0** | 0.10 ms | 216 KB |
| B2 4x4 matrix power (established) | 115/115 | 45/45 | **0** | 1.60 ms | 326 KB |
| B1 direct simulation | 18/115 | 43/45 | 2 (unverifiable answers, n=10^6) | 2000 ms (timeouts) | 12.5 MB |
| B3 sympy rsolve+summation | 83/115 | 45/45 | 14 | 31 ms | 4.5 MB |
| B4 fake control | 78/115 | 15/45 | 67 | 5.7 ms | 14 MB |

Prereg verdicts:
- M PASSES: 0 wrong, 100% in-rep, 100% abstention correctness.
- M vs matrix power: **TIE on accuracy and safety** (expected; same math). Speed: M median 16x faster (0.10 vs 1.60 ms) -> meets the
  prereg "speed edge" bar (<0.5x). Honest caveat: both are milliseconds; the edge is a 5-number tuple vs a 16-entry matrix, a constant factor, not new capability.
- M beats simulation (can't reach large n) and sympy (as wrapped here) on accuracy with 0 wrong.
- B3's 14 wrong answers all involve x -> 0*x + b steps (sympy's closed form mishandles the 0^k case at k=0). A more careful sympy
  wrapper could fix this; it's a fair-baseline weakness of my wrapper as much as of sympy.
- B1's 2 "wrong" are out-of-rep runs it finished at n=10^6 that the verifier couldn't confirm (scored WRONG per prereg); probably correct.
- Fake control produced 67 wrong -> scorer works; run valid.
Abstention is by syntactic op type, identical in M and B2 — no edge there either.
