# Evidence inventory — verification in progress

## Flagship Rule 3 / Rule 17 evidence

- [x] Experiment 012 frozen plan recovered and hash-checked.
- [x] Experiment 012C frozen plan recovered and hash-checked.
- [x] Experiment 012 primary and complete result files recovered; standalone copies are byte-identical to the audit ZIP copies.
- [x] Supplied Experiment 012 replay script rerun successfully.
- [x] Separate reimplementation reproduced all five prospective survivor sets and every mismatch count.
- [x] Rule 3 / Rule 17 parity repair reproduced: Rule 3 = 0/256 mismatches; Rule 17 = 217/256 mismatches.
- [x] Frozen DSL reconciled: 8 horizons × 254 nonconstant masks = **2,032 programs** for Experiment 012.
- [x] Translation-invariance certificate checked against the supplied ECA convention and numerically stress-checked across multiple horizons.
- [x] Independent audit enumeration found 0 resolving programs among all 2,032 frozen-DSL programs on a separate audit sample.
- [x] `LanguageLimitBench_v0.1.1_PUBLIC` recovered; manifest verifier reports 20 files verified and all 5 unit tests pass.
- [x] Lean source package recovered; all 8 manifest-listed project files match declared byte counts and SHA-256 hashes.
- [ ] Lean project compiled under pinned Lean 4 / Mathlib v4.32.1 with machine-check receipt.
- [ ] Third-party / separately hosted reproduction from the final public release.
- [ ] Original `From_Search_Failure_to_Language_Limit.tex` located, or publication source regenerated from the verified preprint.
- [ ] `Executable_Questions_Open_Source_Kit_v0.3.0.zip` located as a standalone release artifact, or reconstructed from the verified component artifacts.

See `research/EXP012_REPLICATION_AUDIT_2026-10-12.md`.

## Secondary representation-repair evidence received

- [x] `Representation_Repair_Computing_v0.1.0(3).zip`
  - SHA-256 manifest verified: 13/13 packaged files matched.
  - Reproduction rerun completed in a separate Python runtime.
  - Mathematical/result fields matched archived results; only the Python runtime string differed.
- [x] `Representation_Repair_Ablation_v1_FULL(1).zip`
  - Frozen four-arm ARC-AGI-3 protocol and local validation records inspected.
  - No live ARC-AGI-3 scout/confirmation result is claimed by the package.
- [x] `Representation Limits, Consciousness, and Experimental Roadmap`
  - Background framework/roadmap; not flagship evidence.
- [x] `From Representational Holes to Governed Cognitive Repair`
  - Background manuscript and Opaque Fiber benchmark record; not flagship Rule 3/17 evidence.

## Excluded as unrelated to this release

- `deep-research-report.md` — Kolyvagin/Stark-regulator mathematics research; keep out of this repository's public launch narrative.

## Current wording boundary

It is now accurate to say the Experiment 012/012C computational endpoints were **reproduced in a separate audit implementation**.

It is not yet accurate to say the result has received **external third-party replication** or that the supplied Lean project has been independently compiled.
