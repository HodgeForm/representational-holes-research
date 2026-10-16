# ORB Genesis bridge (store != admit)

Rerun from the `orb-genesis` directory. The script scans `*.db` files under that directory (or the database paths you pass) and queues newly verified `HELDOUT_SUPPORTED` studies into `bridge/outbox/`:

```bash
python3 bridge/bridge.py
```

Gate: skips studies already bridged (`ledger.json`, keyed by study bundle sha256), studies that are not `HELDOUT_SUPPORTED` (for example `REFUTED`), and studies whose `verify` step fails.

An operator may then attach each `outbox/*.json` to HodgeForm case `case_c5a82d74f4a94cda` ("ORB Genesis studies") using only `orbita_add_inline_file` (optionally `orbita_check_evidence_eligibility`), record the file id in `ledger.json`, and move the file to `outbox/sent/`.

Do not call promote, approve, activate, or admit tools. Lean status in the payloads covers the fixed built-in lemma and the per-study certificate for the exact rows in the file. The limits are in `v2/LIMITS.md`.
