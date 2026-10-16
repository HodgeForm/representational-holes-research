#!/usr/bin/env python3
"""Re-run preregistered ORB Genesis studies H1–H3.

From orb-genesis/:

    python3 hard/run_hard.py
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import orb_genesis as og


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_expression(run):
    return next(c["expression"] for c in run["candidates"] if c["id"] == run["selected_id"])


def replay(db, request, labels):
    store = og.Store(db)
    frozen = store.add(json.loads(pathlib.Path(request).read_text()))
    return store.score(frozen["run"]["id"], json.loads(pathlib.Path(labels).read_text()))


def expect(name, cond, detail):
    if not cond:
        raise SystemExit(f"FAIL {name}: {detail}")
    print(f"{name} PASS {detail}")


def main():
    recorded = (HERE / "PREREG.sha256").read_text().split()[0]
    actual = sha256(HERE / "PREREG.md")
    expect("PREREG", actual == recorded, f"sha256 {actual}")

    subprocess.run([sys.executable, str(HERE / "gen.py")], cwd=HERE, check=True)

    with tempfile.TemporaryDirectory() as tmp:
        db = str(pathlib.Path(tmp) / "hard.db")
        h1 = replay(db, HERE / "h1-request.json", HERE / "h1-labels.json")
        h2 = replay(db, HERE / "h1-request.json", HERE / "h2-labels-flipped.json")
        h3 = replay(db, HERE / "h3-request.json", HERE / "h3-labels.json")

    e1 = h1["run"]["evaluation"]
    expect(
        "H1",
        e1["status"] == "HELDOUT_SUPPORTED"
        and selected_expression(h1["run"]) == {"op": "eq", "a": "a", "b": "b"}
        and e1["selected_result"]["metrics"]["correct"] == 8
        and e1["selected_result"]["metrics"]["wrong"] == 0
        and e1["baseline_advantage"] == 1.0
        and all(b["metrics"]["correct"] == 0 and b["metrics"]["abstained"] == 8 for b in e1["baselines"]),
        "HELDOUT_SUPPORTED eq(a,b) 8/8 advantage +1.0 baselines 0/8",
    )

    e2 = h2["run"]["evaluation"]
    cx2 = [c["id"] for c in e2["selected_result"]["counterexamples"]]
    expect(
        "H2",
        e2["status"] == "REFUTED" and cx2 == ["val-16", "val-21"],
        f"REFUTED counterexamples {cx2}",
    )

    e3 = h3["run"]["evaluation"]
    expect(
        "H3",
        e3["status"] == "REFUTED"
        and selected_expression(h3["run"]) == {"op": "field", "a": "c"}
        and e3["selected_result"]["metrics"]["correct"] == 4
        and e3["selected_result"]["metrics"]["wrong"] == 4,
        "REFUTED field(c) 4/8",
    )

    for name in ("h1-result.json", "h2-result.json", "h3-result.json"):
        bundle = json.loads((HERE / name).read_text())
        report = og.verify(bundle, None)
        expect(name, report["python_recomputation"] == "PASSED" and report["lean_status"] == "NOT_RUN", "python recomputation PASSED")

    forged = json.loads((HERE / "h2-forged.json").read_text())
    try:
        og.verify(forged, None)
    except ValueError as exc:
        expect("H2-forged", "Evaluation mismatch" in str(exc), f"rejected ({exc})")
    else:
        raise SystemExit("FAIL H2-forged: verify accepted a forged status")

    print("PASS: hard tests H1-H3 match the preregistered expectations.")


if __name__ == "__main__":
    main()
