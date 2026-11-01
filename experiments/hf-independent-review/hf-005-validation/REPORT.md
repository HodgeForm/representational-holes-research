# HodgeForm research validation — HF-VALIDATION-005

**Date:** 2026-11-01

**Overall scientific status: UNVERIFIED.**  The predeclared HF-005 **local engineering acceptance gates passed**, and a separate Python implementation reproduced the predictions and metrics. This does **not** establish third-party certification, discovery of a new scientific result, or superiority over established statistical methods.

## Question

Does a cross-validated feature-search wrapper (one variable or two variables) improve prediction on new examples when an original mathematical representation is intentionally coarse? The wrapper is **local code**. `HodgeForm Studio Experimental v0.1.0` was **not modified** and remains a finite-sample collision-audit tool.

## Frozen before revealing holdout results

- Five binary classification tasks, drawn from **three public dataset sources**: digits (0 vs 6, 2 vs 5, 4 vs 9), wine (0 vs 1), and Wisconsin breast cancer diagnostic classes.
- Each task: train 60%, holdout 40%, with a deterministic stratified split. All selection and four-fold cross-validation used training labels only.
- Original representation: for digits, count of high-intensity pixels and center pixels in coarse bins; for other data, first two numerical features thresholded using **training medians**.
- Candidate representation: baseline plus one or two binary raw features. Model uses hierarchical frequency smoothing (global alpha 6, within-representation alpha 12).
- Search uses all nonconstant single fields and every unordered pair, by four-fold training cross-validation Brier loss. A candidate is deployed only after improving CV Brier by at least 0.004 relative to the current choice and improving at least 3/4 folds.
- **Predeclared pass gates**: holdout Brier improvement in at least four of five tasks, positive equal-task mean gain with lower bound of within-task bootstrap interval above zero, no task regression greater than 0.015; and at least two pair choices deployed and two deployed pairs beating their single-field alternative in holdout Brier.
- Locked prediction/protocol SHA256: `4e5d6e02eec66a3ace20ddb4b5ad5928298af44e22727ea419ac3585899a8e0c`. Exact file: `precommit.json`. The local program modified a performance-only loop *after* freezing predictions to cache bootstrap deltas; it did not change predictions or test gates. This file hash is not an external trusted timestamp.

## Heldout results (lower Brier is better)

| Task | Holdout n | Deployed added fields | Baseline Brier | Deployed Brier | Heldout gain |
|---|---:|---|---:|---:|---:|
| Digits 0 vs 6 | 144 | `[21]` | 0.17819 | 0.06125 | +0.11694 |
| Digits 2 vs 5 | 144 | `[5,26]` | 0.21816 | 0.09561 | +0.12255 |
| Digits 4 vs 9 | 145 | `[21,43]` | 0.13477 | 0.05390 | +0.08088 |
| Wine 0 vs 1 | 52 | `[12]` | 0.07662 | 0.04722 | +0.02940 |
| Breast cancer | 228 | `[13,26]` | 0.11246 | 0.07582 | +0.03664 |

**Total holdout predictions: 713**. All five tasks improved relative to the predeclared coarse baseline; two of three selected pairs beat their best selected single field in the same holdout. Equal-task Brier gain **+0.07728**. Within-task record bootstrap interval for equal-task mean **[+0.07049, +0.08443]**. This interval ignores uncertainty over dataset selection, benchmark design and scientific domain shift; it is not a universal generalization confidence interval.

**Local test gate:** `PASS`. See `holdout_scoring.json` and `precommit.json`.

## Independent-code reproducibility check

`audit_independent.py` uses an independently written dictionary-based probability predictor rather than importing the research algorithm. It reconstructs the selected features and labels, recovers all 713 predictions within rounding tolerance, checks each holdout score and the SHA-256 commitment, and reports `LOCAL_INDEPENDENT_CODE_REPLAY_PASS` in `independent_audit.json`. This is **independent implementation locally**, not an independently administered/scored external challenge.

## Stronger baseline (exploratory, post-reveal)

Standard-scaled all-feature regularized logistic regression, trained only on the original training set, achieved **lower Brier scores on all five tasks** than the wrapper; see `strong_baseline_exploratory.json`. This comparison was not part of the original acceptance criteria and cannot be hidden or retroactively used to redefine the gate.

## Negative control (exploratory, post-reveal)

With per-task scrambled outcomes, the method improved only one of the five held-out null tasks; the four-of-five gate did not pass. Some null tasks nonetheless selected spurious variables, so stronger negative-control calibration is still needed. See `negative_control_exploratory.json`.

## Claim authority / deployment boundary

`HodgeForm Studio Experimental` returned `UNVERIFIED` in its evidence inventory: it cannot execute or authenticate a separate verifier, run Lean, or issue a proof certificate. The native HodgeForm/Orbita connection attempts failed during this session, including both linked OrbitaX read-only capability checks. The plugin itself has not been upgraded. No genuine independent third-party sealed test was run. Do not describe this as a scientific discovery or an autonomous research system.

**Three distinct conclusions:**

1. **VERIFIED by local independent code:** the numerical HF-005 results and frozen-file internal consistency.
2. **PASSED on preregistered local benchmark:** two-variable search can improve very coarse summaries on these publicly available tasks.
3. **UNVERIFIED:** general scientific discovery, superiority to standard full-feature predictors, independent external certification, Lean formal proof, or a native HodgeForm governor receipt.

## Falsification-preserving next gate

Use a third-party maintained benchmark with genuinely sealed labels, independently timestamped predictions, a baseline at least as competitive as a standard all-feature regularized classifier, and two independent scorer implementations. Freeze this new protocol *before* a new dataset is revealed. Do not retune HF-005 after observing results and count it as a fresh confirmatory trial.

## Rerun

Python 3.11+, NumPy, scikit-learn:

```
python run.py prepare              # regenerates training-only selections and frozen probabilities
python run.py evaluate             # checks frozen SHA-256 and computes heldout scores
python audit_independent.py        # independently recomputes 713 predictions and checks scores
python strong_baseline.py         # post-hoc contextual challenger
python negative_controls.py       # post-hoc shuffled-label controls
```

The packaged `precommit.json` should be backed up before re-running `prepare`, which overwrites it. All source labels are publicly available, and the local freeze can be reproduced but is not a trusted third-party timestamp.
