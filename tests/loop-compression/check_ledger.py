"""Standalone audit of the loop-compression test. Stdlib only; imports nothing else.
Checks: (1) ledger hash chain, (2) PREREG.md matches the preregistered fingerprint,
(3) every result file matches the hash recorded in the ledger, (4) the headline numbers
recomputed from rows.json match results.json. Exit code 0 = all good, 1 = tampering/mismatch."""
import json, hashlib, sys, pathlib
D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent)
PREREG = "3957a59428934b0c6e9c6ee2b7ba1587f612f9c62c600644c33261e0ff094666"
sha = lambda p: hashlib.sha256((D / p).read_bytes()).hexdigest()
bad = []
prev = "0" * 64; ents = []
for line in (D / "ledger.jsonl").read_text().splitlines():
    e = json.loads(line); h = e.pop("hash")
    if e["prev"] != prev: bad.append(f"ledger seq {e['seq']}: prev link broken")
    if hashlib.sha256(json.dumps(e, sort_keys=True).encode()).hexdigest() != h:
        bad.append(f"ledger seq {e['seq']}: entry hash mismatch (entry edited)")
    prev = h; ents.append(e)
if ents[0].get("prereg_sha256") != PREREG: bad.append("ledger prereg fingerprint changed")
if sha("PREREG.md") != PREREG: bad.append("PREREG.md does not match fingerprint 3957a594... (goalposts moved)")
for f, h in ents[1]["files"].items():
    if sha(f) != h: bad.append(f"{f}: hash differs from ledger (file edited after the run)")
rows = json.loads((D / "rows.json").read_text()); res = json.loads((D / "results.json").read_text())
for m, s in res["summary"].items():
    r = [x for x in rows if x["method"] == m]
    wrong = sum(x["verdict"] == "WRONG" for x in r)
    inc = sum(x["verdict"] == "correct" and not x["oor"] for x in r)
    if wrong != s["wrong"] or f"{inc}/{res['in_rep']}" != s["in_rep_correct"]:
        bad.append(f"{m}: rows.json disagrees with results.json")
m = res["summary"]["M_summary"]; b = res["summary"]["B2_matrix"]
print(f"tasks={res['tasks']} in_scope={res['in_rep']} out_of_scope={res['out_rep']}")
print(f"loop method: {m['in_rep_correct']} in scope, {m['oor_handled_ok']} out of scope refused/handled, wrong={m['wrong']}")
print(f"matrix (textbook): {b['in_rep_correct']} in scope, {b['oor_handled_ok']} out of scope, wrong={b['wrong']}")
print("FAIL:\n  " + "\n  ".join(bad) if bad else "OK: ledger chain, prereg fingerprint, file hashes and counts all verify")
sys.exit(1 if bad else 0)
