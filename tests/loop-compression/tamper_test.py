"""Forged-result test: copy the test folder, forge results in three ways, and show check_ledger.py rejects each.
Stdlib only. Run: python3 tamper_test.py"""
import json, shutil, subprocess, sys, tempfile, pathlib
HERE = pathlib.Path(__file__).parent
def check(d): return subprocess.run([sys.executable, str(HERE / "check_ledger.py"), str(d)], capture_output=True, text=True)
def forge(name, edit):
    d = pathlib.Path(tempfile.mkdtemp()) / "t"; shutil.copytree(HERE, d); edit(d); r = check(d)
    print(f"{name}: {'REJECTED' if r.returncode else 'ACCEPTED (BAD)'}"); print("   " + r.stdout.strip().splitlines()[-1] if r.returncode==0 else "   " + r.stdout.split('FAIL:')[1].strip().splitlines()[0])
    return r.returncode != 0
def flip_row(d):  # a WRONG answer from the fake control edited to say correct
    p = d / "rows.json"; rows = json.loads(p.read_text())
    next(x for x in rows if x["verdict"] == "WRONG")["verdict"] = "correct"; p.write_text(json.dumps(rows))
def flip_summary(d):  # results.json edited to claim the fake control had 0 wrong
    p = d / "results.json"; r = json.loads(p.read_text()); r["summary"]["B4_fake"]["wrong"] = 0; p.write_text(json.dumps(r, indent=1))
def move_goalposts(d):  # prereg edited after the fact
    p = d / "PREREG.md"; p.write_text(p.read_text() + "\nAmended: 2 wrong answers are acceptable.\n")
base = check(HERE); print("untouched copy:", "ACCEPTED" if base.returncode == 0 else "REJECTED (unexpected)")
ok = base.returncode == 0 and all([forge("forged row (WRONG -> correct)", flip_row), forge("forged summary (wrong 67 -> 0)", flip_summary), forge("edited prereg", move_goalposts)])
print("TAMPER TEST PASSED" if ok else "TAMPER TEST FAILED"); sys.exit(0 if ok else 1)
