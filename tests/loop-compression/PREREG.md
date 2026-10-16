# PREREG — "exact loop summary or abstain" vs established baselines
Written 2026-10-16 before any code was run. Hash recorded in ledger.jsonl.

## Task family (held-out seed = 20261016, N_TASKS = 160)
Program = (x0, n, body). Body ops: aff(a,b): x=a*x+b; cost(r,s,t): C+=r*x^2+s*x+t;
loop(m, body) (nested, m in 2..5); out-of-representation ops: sq: x=x*x+1; mod(m): x=x%m;
pw(T,k): x = x-k if x>T else 2x; data(D): x=x+D[i%len(D)] (depends on outer counter i).
70% of tasks in-representation (only aff/cost/loop), 30% contain >=1 out-of-rep op.
n = 10^e, e uniform integer in 3..18. For e>=5 every multiplier a in {-1,0,1} (otherwise the exact
answer has ~n bits and cannot be written down by ANY method); for e<5, a in [-2,2]. b in [-9,9], r,s,t in [-5,5], x0 in [-9,9].
Answer = exact (x_final, C) as Python big integers.

## Methods (identical per-task budget: 2.0 s wall via SIGALRM, single process; peak memory via tracemalloc)
M  method: compose 5-tuples (a,b,r,s,t) with the chat's rule, repeated squaring; ABSTAIN if any out-of-rep op.
B1 direct simulation (answers whatever it finishes in budget; timeout = no answer).
B2 established: 4x4 integer matrix power on state [x^2, x, 1, C] (companion-style linearization); abstains on out-of-rep ops.
B3 sympy: rsolve for the affine recurrence + summation for the cost, evaluated at n; abstain on non-polynomial/degree>1 maps or errors.
B4 fake control: simulate min(n,1000) steps and extrapolate linearly; always answers.

## Ground truth / verification (code shares nothing with M or B2)
Independent interpreter. If simulable in 5 s: exact simulation. Else, for in-rep tasks with all a in {-1,0,1}: x_n and C(n)
are polynomials in n on each parity class; fit by exact Fraction Lagrange on 8 simulated points (n>=2, same parity as N),
confirm on 2 extra points, evaluate at N. Out-of-rep tasks with no simulable truth: correct behaviour = abstain; any answer = WRONG (unverifiable).

## Metrics
exact-answer accuracy (in-rep), abstention correctness (abstain on out-of-rep with no truth; on out-of-rep with truth, abstain OR correct answer both OK),
WRONG-ANSWER RATE (critical; must be 0), median/max wall time, peak memory.

## Win/loss criteria (fixed now)
M PASSES iff wrong = 0 AND in-rep accuracy = 100% AND abstention correctness = 100%.
M vs B2: accuracy is expected to TIE (mathematically equivalent). M has a speed edge only if median time < 0.5x B2's; otherwise declared a tie.
M beats B1/B3 iff M accuracy > theirs with wrong = 0. Any wrong answer by M = method FAILS, reported as such.
B4 must show wrong > 0 (else the scorer is broken and the run is void).
