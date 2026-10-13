# Representational Holes — v0.1.0-rc1

**Status: private release candidate. Do not publish yet.**

This branch is a reproducible release candidate for the bounded Experiment 012 / 012C representational-hole result.

## Flagship claim

Experiment 012 freezes an ECA measurement DSL containing exactly **2,032 translation-invariant aggregate programs** (8 horizons × 254 nonconstant neighborhood masks). Four of five ambiguity classes were uniquely resolved on fresh states. The residual Rule 3 / Rule 17 class is shift-equivalent under the frozen language and therefore cannot be separated by any program in that DSL.

Experiment 012C separately froze an index-parity extension and prospectively obtained:

- Rule 3: **0/256 mismatches**
- Rule 17: **217/256 mismatches**
- unique recovery: **yes**

## Computational reproduction

Run:

```bash
python -m pip install numpy
python experiments/exp012/verify_exp012.py
```

Expected final line:

`PASS: Experiment 012 and 012C reproduce the frozen result artifacts.`

GitHub Actions independently ran this verifier on the release-candidate branch and passed.

## Formal proof check — PASSED

The exact supplied Lean ZIP is preserved as Base64 at:

`artifacts/orbita_language_limit_lean_v0_1.zip.b64`

Reconstructed ZIP SHA-256:

`3ff0a2bf1034a34111f5060bdafe947daf46c3245f6a894d55a168b700b2409c`

GitHub Actions built it successfully under:

- Lean 4.32.1
- Mathlib v4.32.1
- Lake 5.0.0-src+f054605

CI reported:

`Build completed successfully (8659 jobs).`

See `formal/LEAN_CI_RECEIPT.md`.

## Evidence boundaries

Supported:
- frozen DSL definition and 2,032-program denominator;
- computational replay of Exp012/012C;
- independent audit reimplementation;
- analytic Rule 3/17 shift argument;
- separately frozen prospective parity repair;
- successful compilation of the supplied abstract Lean formalization.

Not established:
- AGI;
- universal representational repair;
- difficult or novel synthesis;
- minimality of parity among all conceivable extensions;
- external third-party replication;
- peer review.

## Remaining public-release gates

- External reproduction from the release candidate is obtained.
- Paper author/contact placeholders are replaced.
- Licensing and IP/public-disclosure review is completed.
- Repository visibility change is explicitly approved.
- Zenodo DOI is minted only after the approved GitHub release is public.
