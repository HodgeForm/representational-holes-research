# Reproduce v0.1.0-rc1 from zero

This release candidate is designed so an independent reviewer can reproduce the flagship computational endpoint without HodgeForm or Orbita.

## 1. Clone the release-candidate branch

```bash
git clone https://github.com/ImDerekEarnhart/representational-holes-research.git
cd representational-holes-research
git checkout release/representational-holes-v0.1.0-rc1
```

The repository is currently private, so this command works only for authorized reviewers until public release.

## 2. Reproduce Experiment 012 / 012C

Python 3.12 is the CI reference runtime.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install numpy
python experiments/exp012/verify_exp012.py
```

Expected output:

```
PASS: Experiment 012 and 012C reproduce the frozen result artifacts.
```

The verifier:
- checks the frozen plan/result SHA-256 values;
- reconstructs all five prospective evaluations;
- compares every per-rule mismatch count to the frozen primary result;
- checks the 012C 0-versus-217 endpoint;
- stress-checks the Rule 3 / Rule 17 shift identity over multiple horizons.

## 3. Reconstruct and build the exact Lean artifact

```bash
base64 -d artifacts/orbita_language_limit_lean_v0_1.zip.b64 > /tmp/orbita_language_limit_lean_v0_1.zip
echo "3ff0a2bf1034a34111f5060bdafe947daf46c3245f6a894d55a168b700b2409c  /tmp/orbita_language_limit_lean_v0_1.zip" | sha256sum -c -
unzip /tmp/orbita_language_limit_lean_v0_1.zip -d /tmp/orbita-lean
cd /tmp/orbita-lean/orbita_language_limit_lean
```

Install elan if needed, then:

```bash
lake update
lake exe cache get
lake build
```

The archive pins:

`leanprover/lean4:v4.32.1`

and Mathlib:

`v4.32.1`

## 4. Interpretation boundary

A successful replay establishes that the supplied frozen artifacts are internally reproducible under the declared implementation and that the Lean source compiles if the formal CI passes.

It does not by itself establish scientific novelty, historical priority, external third-party replication, or generalization beyond the bounded ECA setting.
