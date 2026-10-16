# Lean CI machine-check receipt

GitHub Actions workflow: `Verify release candidate`

Workflow run ID: `38398326853`

Lean job ID: `115299148630`

PR merge-test commit checked by GitHub Actions:

`418b7d3d04e06bc50624c4313ff2b0676d002fc9`

Exact reconstructed Lean archive SHA-256:

`3ff0a2bf1034a34111f5060bdafe947daf46c3245f6a894d55a168b700b2409c`

Toolchain:

`leanprover/lean4:v4.32.1`

CI-reported versions:

- Lean 4.32.1, commit `f054605aea4b840552cca2e725580bffd1e1b704`
- Lake 5.0.0-src+f054605

Build result:

`Build completed successfully (8659 jobs).`

The workflow also scanned the Lean source tree for unfinished `sorry`, `admit`, or explicit `axiom` placeholders before compilation. That check passed.

GitHub Actions artifact:

- name: `lean-proof-receipt`
- artifact ID: `11814216649`
- artifact ZIP digest: `sha256:b39dad26be8002c48572667224505c4fc5084741139a19b6c977c2cdc569af63`

This receipt establishes successful compilation of the supplied abstract Lean formalization under its pinned toolchain. The sources prove general theorems about an arbitrary representation map, plus a two-bit parity toy. They are not a formalization of Rules 3 and 17 or of the Experiment 012 grammar. The receipt does not by itself establish novelty or validate any external application of the abstract theorems.
