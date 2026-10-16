# Loop-compression test (demo video, scene 5: "160 problems it had never seen")

Preregistered benchmark: a loop-summary method (summarise or abstain) vs. the textbook method (4×4 matrix power), direct simulation, SymPy, and a deliberately fake control. Stdlib + SymPy only; nothing here imports or calls HodgeForm.

- `PREREG.md`: the plan, written before the run. sha256 `3957a59428934b0c6e9c6ee2b7ba1587f612f9c62c600644c33261e0ff094666`.
- `ledger.jsonl`: hash-linked ledger. Entry 0 locks the prereg fingerprint; entry 1 records hashes of code and results after the run.
- `bench.py` (methods + task generator, seed 20261016), `verify.py` (independent ground truth, shares no code with the methods), `run.py` (the run).
- `results.json`, `rows.json` (one row per task × method), `RESULTS.md`, `VERDICT.md`.
- `check_ledger.py`: verifies the ledger chain, the prereg fingerprint, file hashes, and recounts results from `rows.json`.
- `tamper_test.py`: forged-result test. Edits a copy (WRONG→correct in a row, wrong 67→0 in the summary, an amended prereg) and shows each is rejected.

```bash
python3 check_ledger.py     # seconds; exit 0 = verified
python3 tamper_test.py      # seconds; prints REJECTED three times
cp -r . /tmp/lc && cd /tmp/lc && python3 run.py   # ~6 min; re-runs everything in a copy (run.py overwrites results.json/rows.json; timings differ per machine, so the ledger hashes will not match the copy, but the correctness counts should). Needs sympy.
```
Headline: 160 tasks (115 in scope, 45 out of scope). Loop method 115/115 correct, 45/45 out-of-scope refused, 0 wrong. Matrix method: identical accuracy (a tie; same math), about 16× slower median (1.6 ms vs 0.10 ms). Timings vary by machine; correctness counts should not.
