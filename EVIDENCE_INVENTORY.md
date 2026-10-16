# Evidence inventory

What a reader can check from this repository. Staging checklists that named uploads not included here are in `research/archive/EVIDENCE_INVENTORY_staging.md`.

## Flagship Rule 3 / Rule 17 evidence in this tree

- [x] Experiment 012 frozen plan, primary results, complete results, and Experiment 012C plan are in `experiments/exp012/`. SHA-256 values are in `MANIFEST_SHA256.md`.
- [x] `experiments/exp012/verify_exp012.py` recomputes the five prospective survivor sets, every recorded mismatch count, the 012C endpoint (0/256 and 217/256), and the Rule 3 / Rule 17 shift identity.
- [x] Frozen DSL size is 8 horizons × 254 nonconstant masks = **2,032 programs**. The 16-versus-2,032 wording is resolved in `research/CLAIM_AUDIT.md`.
- [x] The language-limit statement is the shift identity plus translation invariance of the frozen aggregate DSL, recorded in the result JSON and checked numerically by the verifier.
- [x] The Lean archive in `artifacts/` matches the SHA-256 in `MANIFEST_SHA256.md`. `formal/LEAN_CI_RECEIPT.md` records a successful compile under Lean 4.32.1 / Mathlib v4.32.1. That project is general theorems plus a two-bit parity toy. It is not a formalization of Rules 3 and 17.

## Still open, and not claimed

- [ ] A third party reproducing the public tree and reporting the result independently.

## Companion, separate from the flagship

`orb-genesis/` is a synthetic finite-data discovery loop with weak lookup-table baselines and per-study Lean certificates about those exact rows. It is not evidence for the Rule 3 / Rule 17 claim. See `orb-genesis/README.md`.
