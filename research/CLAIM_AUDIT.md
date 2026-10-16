# Claim audit

This is the public claim record for the files in this repository. Earlier staging memos that name uploads not included here are in [archive/](archive/), with a note on how to read them.

## Resolved: 16 versus 2,032 programs

The frozen Experiment 012 measurement language contains **2,032 programs**.

`experiments/exp012/exp012_frozen_plan.json` fixes that language as:

- 8 horizons: `1, 2, 4, 8, 12, 16, 24, 30`;
- 254 nonconstant neighborhood masks: the integers `1` through `254` (masks `0` and `255` are excluded as constants);
- one program for each horizon–mask pair.

`8 × 254 = 2,032`. `experiments/exp012/verify_exp012.py` asserts that product before it replays the prospective sample.

The integer 16 appears in the same frozen plan, and it is not a program count:

- `16` is one of the eight horizon lengths above;
- elementary Rule 16 is one of the 77 T05 survivor worlds. On the prospective sample the selected program records 235 mismatches for Rule 16, and 0 mismatches for both Rule 3 and Rule 17.

No plan, result file, or verifier in this repository defines an Experiment 012 grammar of 16 programs. Early notes recorded that some prior write-ups called a baseline "16 programs." Those write-ups are not in this tree, and they do not supply a second frozen grammar a reader can replay. The public denominator is the checked-in 2,032-program language. The two figures were never two sizes of that grammar.

## What the frozen artifacts support

- Four of five prospective ambiguity classes were uniquely resolved. The residual class is Rules 3 and 17.
- Under the supplied convention, `F17(x)_i = F3(x)_{i+1}`. Every program in the frozen DSL sums a translation-invariant local predicate on a periodic lattice, so none of the 2,032 programs can distinguish the pair. The verifier stress-checks the iterated shift for horizons 1 through 8.
- Experiment 012C was frozen separately. It counts even-index activity after one step. The verifier recomputes 0/256 mismatches for Rule 3 and 217/256 mismatches for Rule 17 on that prospective sample.

The Lean sources in `artifacts/` prove general facts about an arbitrary representation map, plus the two-bit parity toy in `OrbitaLanguageLimit/Example.lean`. They do not encode Rules 3 and 17, the horizon list, or the 2,032 masks. `formal/LEAN_CI_RECEIPT.md` records a successful compile of that abstract project under Lean 4.32.1 / Mathlib v4.32.1.

## What is not established

- Universal representation repair, AGI, or autonomous ontology invention.
- That the search was difficult. Four classes were resolved by short programs.
- Minimality of index parity among every conceivable extension.
- Independent third-party replication, historical priority, or peer review.
- A machine-checked Lean proof of the cellular-automaton claim.

## Claim history

The first staging claim audit left "16 programs" and "2,032 programs" as an open discrepancy and pointed at draft packages that are not published in this repository. The 2026-10-12 replication note already treated 2,032 as the Experiment 012 size and warned against quoting a 16-program language as this experiment's denominator. This file closes that discrepancy against the frozen plan. The staging memos remain in [archive/](archive/) so the earlier wording is still readable.
