# Evidence audit — 2026-10-12

## Executive verdict

New uploaded materials materially strengthen the **bounded representation-repair** evidence base, but they do **not yet verify the flagship Rule 3 / Rule 17 experiment**. The public launch should therefore remain on HOLD until the original ECA package or an independently reconstructed, frozen replacement is checked.

## 1. Representation-Repair Computing v0.1.0

Artifact reviewed: `Representation_Repair_Computing_v0.1.0(3).zip`.

### Integrity check
A clean extraction was verified **before rerunning any code**:

- `python code/verify_manifest.py`
- Result: `PASS: 13 packaged files match the SHA-256 manifest.`

### Independent replay in this audit environment
I then ran:

```sh
python code/reproduce.py
```

Observed replay:

- streaming change detector: **100,000 / 100,000** correct after the one-bit repair;
- memory observation menu: **50,000 / 50,000** validation cases;
- sensor observation menu: **50,000 / 50,000**;
- resolution observation menu: **50,000 / 50,000**;
- one-bit FSM enumeration: exactly **1 / 256** survivor under the frozen reset/scoring convention;
- longer-sequence holdout: **32,640 / 32,640** exact sequences;
- reachable product-state certificate: **equivalent for all finite sequence lengths** under the stated convention.

The regenerated `reproduced_results.json` differed from the archived file only in the recorded Python runtime string (archived Python 3.12.14 vs audit Python 3.13.5). The mathematical/result fields matched.

### What this supports
This is reproducible evidence for a **toy, explicitly bounded** representation-repair claim: current-input-only information is insufficient for an exact change-detection task, and one bit of state is sufficient and minimal under the specified interface. It also includes a restricted Boolean-grammar expressiveness example.

### What it does not support
It does not authenticate the earlier original run, does not verify the Rule 3/17 ECA result, does not establish autonomous repair across unrelated task families, and does not establish a new model of computation.

## 2. Representation-Repair Ablation v1

Artifact reviewed: `Representation_Repair_Ablation_v1_FULL(1).zip`.

The package contains a frozen four-arm ARC-AGI-3 causal experiment:

- B0 BASE
- B1 COLLISION ONLY
- B2 IMMEDIATE REPAIR
- B3 GOVERNED REPAIR

The package records local regression/smoke validation and a locked scout/confirmation procedure. Its own status file explicitly states that **no live ARC-AGI-3 scout or confirmation score was produced in that container**. Accordingly, this is valuable protocol and engineering evidence, but not yet an ARC capability result.

Public launch language must not imply an ARC-AGI-3 performance improvement until the locked experiment is actually executed and independently checked.

## 3. Uploaded manuscripts

Two manuscripts provide useful framing and evidence boundaries:

- `Representation Limits, Consciousness, and Experimental Roadmap`
- `From Representational Holes to Governed Cognitive Repair`

They consistently separate mathematical/finitary results from broader engineering or consciousness hypotheses. These are background manuscripts, not substitutes for executable flagship evidence.

The Arc 3 manuscript records Opaque Fiber Stress Benchmark v1.0.1 as 18/18 exact status classification with strong restraint/provenance metrics, while also preserving the critical caveat that the final run was **not perfectly information-isolated** because a ground-truth overview appeared before the final submission was generated. This should remain qualified if mentioned publicly.

## 4. Deep-research report

`deep-research-report.md` concerns a Kolyvagin/Stark-regulator mathematics program. It is scientifically separate from the representational-hole launch and should **not** be added to this repository or launch narrative.

## 5. Launch consequence

### Now verified enough to say
> We have a reproducible bounded demonstration that a fixed representation can make an exact task impossible, and that a minimal additional state variable can repair the task under explicit conventions.

### Still not verified enough to say
> We have independently reproduced the flagship Rule 3/17 language-limit and 217/256 symmetry-breaking result.

## 6. Remaining critical gate

Locate or reconstruct and freeze the exact Rule 3 / Rule 17 experiment package, including:

1. exact ECA convention and boundary conditions;
2. exact DSL grammar and program count;
3. proof of grammar-wide translation invariance;
4. frozen repair primitive;
5. untouched evaluation set;
6. raw outputs and hashes;
7. independent replay receipt.

Until those are present, keep this repository private and the Zenodo/Medium/X release unpublished.
