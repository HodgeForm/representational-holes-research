# Representational Holes — v0.1.0-rc1

**Status: private release candidate. Do not publish yet.**

This branch is intended to become a reproducible public research release after the remaining gates pass.

## Flagship claim

In Experiment 012, the frozen ECA measurement DSL contains exactly 2,032 translation-invariant aggregate programs (8 horizons × 254 nonconstant neighborhood masks). Four of five ambiguity classes were uniquely resolved on fresh states. The residual Rule 3 / Rule 17 class is shift-equivalent under the frozen language and therefore cannot be separated by any program in that DSL. Experiment 012C separately froze an index-parity extension and prospectively obtained 0/256 mismatches for Rule 3 and 217/256 for Rule 17.

## Reproduce the computational result

```bash
python -m pip install numpy
python experiments/exp012/verify_exp012.py
```

Expected final line:

`PASS: Experiment 012 and 012C reproduce the frozen result artifacts.`

## Formal proof check

The exact supplied Lean artifact is stored at:

`artifacts/orbita_language_limit_lean_v0_1.zip`

CI unpacks it and builds it with:

- Lean 4 v4.32.1
- Mathlib v4.32.1
- `lake update`
- `lake exe cache get`
- `lake build`

The CI result is the machine-check receipt; do not call the Lean artifact compiled until that job passes.

## Evidence boundaries

Supported:
- frozen DSL definition and 2,032-program denominator;
- computational replay of Exp012/012C;
- independent audit reimplementation;
- analytic Rule 3/17 shift argument;
- separately frozen prospective parity repair.

Not established:
- AGI;
- universal representational repair;
- difficult or novel synthesis;
- minimality of parity among all conceivable extensions;
- third-party external replication;
- peer review.

## Remaining public-release gates

- CI Lean build passes.
- Raw/release artifact manifest is finalized.
- External reproduction is obtained.
- Paper author/contact placeholders are replaced.
- Licensing and IP/public-disclosure review is completed.
- Repository visibility change is explicitly approved.
- Zenodo DOI is minted only after the approved GitHub release is public.
