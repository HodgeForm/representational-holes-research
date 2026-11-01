# HodgeForm HF-004 / HF-005 — independent verification materials

**Review status: DRAFT / UNVERIFIED scientifically.** These artifacts reproduce two locally designed feature-representation experiments. They are not independent proof of novel science or autonomous research. The connected HodgeForm Studio Experimental v0.1.0 plugin was not upgraded by either experiment and its evidence audit returned `UNVERIFIED`.

This folder contains **unaltered original experiment scripts**, **frozen prediction data**, exact prediction/protocol commitments, **test outcomes including failures**, independently coded **local** audit scripts, post-hoc stronger baselines, and a GitHub Actions workflow. Third-party researchers should verify the claims independently and report contradictions, not simply rerun a tool and accept its verdict.

## Experiments and all results

| Experiment | Holdout | Result | Negative evidence |
| --- | --- | --- | --- |
| [HF-004](hf-004-compound/REPORT.md): digits 3 vs 8; single-/two-pixel feature search | 143 records | Pair Brier **0.120237** and accuracy **86.01%** | The original coarse representation had better Brier **0.106691**, accuracy **87.41%**; pair **failed** predictive improvement |
| [HF-005](hf-005-validation/REPORT.md): five binary tasks (digits, wine, Wisconsin diagnostic data) | 713 predictions | All 5 beat intentionally coarse baselines; mean task Brier gain **0.07728**; local benchmark criteria passed | An exploratory conventional all-feature logistic regression **outperformed the chosen representation on all 5 tasks** |

There is no peer-independent sealed task or trusted timestamp for the original commitments; all outcome labels are public. The GitHub commit will timestamp **publication**, not retroactively certify when the predictions were originally frozen. Neither experiment proves a general representation theorem, nor does locally rerunning it constitute an independent research discovery.

## Reproduce on a clean checkout

Use **Python 3.13, NumPy 2.3.5 and scikit-learn 1.8.0** (the versions used to produce and recheck these artifacts):

```sh
python -m pip install -r experiments/hf-independent-review/requirements.txt
python experiments/hf-independent-review/check_evidence.py
```

For explicit checks:

```sh
cd experiments/hf-independent-review/hf-004-compound
python run.py evaluate                  # does not reselect models
python independent_verify.py            # separate local code for holdout metric checks
python test_joint.py                    # synthetic XOR unit control

cd ../hf-005-validation
python run.py evaluate                  # scores the frozen choices and predictions
python audit_independent.py             # separate local implementation: 713 predictions
python strong_baseline.py               # exploratory challenger: full-feature logit
python negative_controls.py             # exploratory shuffled-outcome controls
```

**Caution:** `python run.py prepare` overwrites the frozen artifacts in its folder, so copy the experiment folder before regenerating. Verify checksums before and after replay. The provided [check_evidence.py](check_evidence.py) checks internal file identities and documented outcomes without overwriting commitments.

## Source, provenance, and integrity

- `hf-004-compound/frozen_predictions.json` includes 143 frozen predictions and commitment `69fc9b7f7d0ba3af868bd40b7936e837ab165d27196b3ec2173d073082db4244`.
- `hf-005-validation/precommit.json` includes the held-out probabilities and frozen choices for five tasks; commitment `4e5d6e02eec66a3ace20ddb4b5ad5928298af44e22727ea419ac3585899a8e0c`.
- `MANIFEST_SHA256.json` records the **raw bytes** of every original included experiment artifact. Hashes protect against accidental changes to this reviewed snapshot; they do not prove the experimental claims.
- Source data are from scikit-learn's bundled public datasets. No individual-level patient data, API credentials, or private HodgeForm tenant records are distributed.

## What independent reviewers should do

1. Clone this repository; verify file checksums; run the pinned dependency environment and CI commands, reporting software versions.
2. Re-implement the metrics and selection logic independently, challenge the absence of leakage, and check all failures and null controls.
3. Examine competitive baselines; do **not** infer HodgeForm superiority from beating deliberately restricted coarse baselines.
4. For a true new claim, require a fresh third-party administered sealed challenge, an externally timestamped frozen protocol and predictions, and independent execution/scoring. No post-hoc changes to those requirements.
5. Record results including refutations in an independently authored issue, pull request, or external report.

**Release interpretation:** The correct scientific status today is `UNVERIFIED`. The only supported positive claims concern numerical reproducibility and the internal acceptance gates of a locally designed benchmark.
