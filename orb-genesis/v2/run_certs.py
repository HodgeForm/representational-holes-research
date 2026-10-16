"""Regenerate and kernel-check per-study Lean certificates.

Run from the orb-genesis directory, with Lean 4.19.0 available through elan:

    python3 v2/run_certs.py

Paths are resolved from this file's location.
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import leancert as lc


def lean_exe():
    elan = pathlib.Path.home() / ".elan" / "bin" / "elan"
    if not elan.is_file():
        sys.exit("elan not found. Install Lean 4.19.0 via elan, then rerun from orb-genesis/.")
    proc = subprocess.run([str(elan), "which", "lean"], capture_output=True, text=True, cwd=ROOT)
    lean = proc.stdout.strip()
    if proc.returncode != 0 or not lean:
        sys.exit(
            "elan which lean failed. From orb-genesis/, install the pin in lean-toolchain:\n"
            "  elan toolchain install leanprover/lean4:v4.19.0"
        )
    return lean


def main():
    lean = lean_exe()
    hard = ROOT / "hard"
    cases = {}
    phase = ROOT / "result.json"
    if phase.is_file():
        cases["phase_demo"] = phase
    cases.update({
        "H1": hard / "h1-result.json",
        "H2": hard / "h2-result.json",
        "H3": hard / "h3-result.json",
    })
    certs = HERE / "certs"
    res = {}
    for name, path in cases.items():
        bundle = json.loads(path.read_text())
        src, study_hash, _ = lc.generate(bundle)
        (certs / f"{name}.lean").write_text(src)
        res[name] = {"study_hash": study_hash, **lc.check(src, lean)}

    forged_status = json.loads((hard / "h2-result.json").read_text())
    src, study_hash, _ = lc.generate(forged_status, status_override="HELDOUT_SUPPORTED")
    (certs / "H2_forged_status.lean").write_text(src)
    res["H2_forged_status"] = {"study_hash": study_hash, **lc.check(src, lean)}

    forged_rule = json.loads((hard / "h1-result.json").read_text())
    src, study_hash, _ = lc.generate(forged_rule, rule_override=[{"op": "field", "a": "site"}, {"op": "field", "a": "a"}])
    (certs / "H1_forged_rule.lean").write_text(src)
    res["H1_forged_rule"] = {"study_hash": study_hash, **lc.check(src, lean)}

    (certs / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    for name, row in res.items():
        extra = "" if row["lean_status"].startswith("STUDY") else row["output"][:300].replace("\n", " ")
        print(name, row["lean_status"], row["source_sha256"][:12], row["axioms_output"], extra)


if __name__ == "__main__":
    main()
