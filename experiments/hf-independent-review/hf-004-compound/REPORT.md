# HodgeForm HF-COMPOUND-004 — Compound-Feature Discovery / Public Benchmark

**Date:** 2026-11-01  
**Result:** Local two-feature discovery wrapper developed and executed; finite unit test passes; third-party dataset holdout **does not show predictive improvement**. Independent external proof or novel science **not established**.

## Scope and provenance

- **Plugin:** HodgeForm Studio Experimental v0.1.0 (`hodgeform_diagnose_blind_spot`). The plugin's backend was **not** changed. A local Python layer enumerates two-variable candidate representations; the plugin can audit collision outcomes on those representations.
- **Public data:** `sklearn.datasets.load_digits()` in scikit-learn 1.8.0, a copy of UCI Optical Recognition of Handwritten Digits. Source: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html ; UCI creators E. Alpaydin and C. Kaynak, 1998; doi:10.24432/C50P49. The source is **third-party**, but its outcome labels are publicly known. The held-out labels were hidden **operationally during our feature selection**, not escrowed by an independent benchmark authority.
- **Task:** Distinguish handwritten digit 3 from 8 using deliberately coarse image measurements and the candidate repair fields.
- **Split:** fixed stratified train/test, seed 20261101, 214 labeled training images and 143 held-out images.
- **Coarse language L0:** `floor(count(pixels >= 8)/4)` and `floor(count(central 4x4 pixels >= 8)/3)`.
- **Candidate fields:** all nonconstant individual pixel-intensity-at-least-8 indicators; all combinations of two. Categorical-group mean predictor, shrunk toward training prevalence by alpha=4. Ranked with fourfold training-only cross-validation Brier loss.
- **Freeze:** selected features and all 143 holdout predictions serialized to `frozen_protocol.json` and `frozen_predictions.json` **before** `run.py evaluate` read/scored holdout labels. Files contain immutable content hashes verified by the local evaluator.

## Frozen selection

- Single best field: zero-indexed pixel 46.
- Pair: zero-indexed pixels (41, 46), *selected by training CV alone*.
- Training CV Brier: L0 **0.072119**; best single **0.063790**; pair **0.060900**. These are model-selection scores, **not** an unbiased test.
- Prediction commitment SHA-256: `69fc9b7f7d0ba3af868bd40b7936e837ab165d27196b3ec2173d073082db4244`.
- Held-out label commitment SHA-256: `432ca238a82e7b9da08afe019318459d29b63d3c883c870580ec20ac5aed0730`.

## Actual withheld outcomes

| Locked representation | Accuracy | Brier loss (lower better) | Conflicting finite pairs | Comparable pairs | Same-signature holdout support |
|---|---:|---:|---:|---:|---:|
| L0 coarse summary | **87.41%** | **0.106691** | 446 | 1845 | 99.3% |
| L0 + best single | 88.11% | 0.112427 | 378 | 1487 | 99.3% |
| L0 + two-field pair | 86.01% | 0.120237 | 364 | 1398 | 95.8% |

The two-field repair reduces the number of **raw conflicting pairs**, but also makes representations more granular, reducing the total comparable-pair denominator and harming generalization. The fraction of comparable pairs that disagree **increased** from 24.17% (L0) to 26.04% (two-field pair), so raw collision-count reduction alone is misleading. The two-field Brier is **0.013546 worse** than L0. A paired 2,500-draw nonparametric bootstrap gave a 95% interval of **[-0.025306, -0.002203]** for Brier improvement (positive means pair better). The pair also performs worse than the selected single field. No retuning was performed after these outcomes were inspected.

**Cross-check:** `independent_verify.py` independently recomputes holdout classification accuracy, Brier, and conflicting-pair counts from the original scikit-learn data and the sealed predictions. All checked results match. This is independent *code*, not an independent third-party scientific verification.

## Native HodgeForm plugin demonstrations

1. **42 first training cases from the third-party dataset:** Original representation 18 collision pairs; L0 plus selected pair 2 collision pairs. Both reports status `COLLISION_FOUND`; this is not a complete repair.
2. **24-case synthetic XOR engineering unit test:** L0 144 contradictory pairs; adding ordered pair `(f0,f1)` 0 contradictory pairs. The plugin reported `COLLISION_FOUND` then `NO_COLLISION_IN_SUPPLIED_CASES`. This proves the wrapper can supply a composition that resolves this *constructed* finite example; it is **not** a blind independent discovery.
3. **Claim-audit tool:** `UNVERIFIED` because this runtime cannot authenticate an external replay/Lean proof.

## Scientific and engineering verdict

**What passed:** Construction, enumeration, deterministic train-only selection of two-feature representations; freeze-before-score integrity; successful unit test for XOR joint information; plugin collision audit; independent local metric recomputation.

**What failed:** Predictive benefit on this public-data holdout. The fact that fewer conflicting pairs exist after adding fields is not sufficient evidence of improved generalization or causal explanation.

**What's still missing:** independent third-party sealed challenge, cross-dataset validation, robust penalty/selection rules for rare representation signatures, external replay service, and a governed HodgeForm/Orbita backend capable of running and persisting research plans and approvals. No Lean proof was executed; no operator registry was upgraded.

## Reproduce

From the extracted folder, with Python 3 and scikit-learn 1.8.0 and NumPy:

```sh
python run.py prepare  # deterministically produces frozen_protocol.json and frozen_predictions.json from training labels
python run.py evaluate # checks commitments and scores the actual withheld labels
python test_joint.py   # synthetic XOR two-field unit test
python independent_verify.py  # independent held-out result checks
```

**Integrity caveat:** SHA-256 checks demonstrate file identity in this workflow, not independent timestamping or protection against an adversarial experiment designer who controls the public dataset. A future study should obtain withheld labels from a third-party scorer *after* independently timestamping predictions.
