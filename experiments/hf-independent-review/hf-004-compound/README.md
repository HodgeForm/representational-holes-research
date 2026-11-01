# HodgeForm compound discovery pilot 004

- Start with [REPORT.md](REPORT.md).
- `run.py` prepares a training-only feature search and freezes all holdout predictions, then evaluates them in a separate phase. Dataset: scikit-learn `load_digits()` (UCI Optical Recognition of Handwritten Digits).
- `test_joint.py` tests exact two-feature XOR repair.
- `independent_verify.py` recomputes key test metrics with different code.
- `frozen_protocol.json` and `frozen_predictions.json` contain pre-evaluation hashes and locked choices.
- `holdout_results.json`, `training_diagnostics.json`, `unit_test_results.json`, and `independent_verification.json` show all outcomes.
- `remote_training_probe_24.json`, `remote_holdout_probe_24.json` contain small representative case samples; see REPORT.md for actual live HodgeForm plugin runs using the *first 42* training records and the XOR test.

The wrapper is **not** a deployed upgrade to the HodgeForm Studio Experimental plugin.
