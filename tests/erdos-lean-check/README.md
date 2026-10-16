# Erdős #242 Lean check (demo video, scene 3)

A ChatGPT session produced five Lean 4 proof candidates for parts of Erdős problem #242, labelled "UNCHECKED: awaiting Lean verification". This folder holds those files exactly as extracted, the Lean results, and the coverage argument.

- `claims.md`: what the session claimed, quoted verbatim.
- `block_01.lean` … `block_05.lean`: the five blocks as saved. `block_01_fixed.lean` is block 1 with one line repaired (`field_simp  ring  positivity` → `field_simp <;> ring <;> positivity`).
- `official_242.lean`: the official (still open) statement from formal-conjectures.
- `REPORT.md`: per-block verdicts, how each block differs from the official statement, and coverage.
- `ax/*.out`: raw Lean output. `ledger.jsonl`: sha256 of each file and output at check time.

## Result
Block 1 as saved fails; after the one-line fix it passes. Blocks 2–5 pass. Every passing block depends only on `propext`, `Classical.choice`, `Quot.sound` (no `sorryAx`). Block 4 (n ≡ 0 mod 4) is already covered by block 1 (even n). Together the blocks cover every n > 2 except n ≡ 1 (mod 12). **Verdict: known results, confirmed. Erdős #242 is not solved.**

## Re-run
Needs Lean 4.19.0 (`leanprover/lean4:v4.19.0`) and a Mathlib checkout pinned to that toolchain, with the cache downloaded.
```bash
git clone https://github.com/leanprover-community/mathlib4 && cd mathlib4
git checkout v4.19.0            # a Mathlib tag whose lean-toolchain is v4.19.0
lake exe cache get
for f in block_01 block_01_fixed block_02 block_03 block_04 block_05; do
  thm=$(grep -oP '^theorem \K\S+' ../tests/erdos-lean-check/$f.lean | head -1)
  (cat ../tests/erdos-lean-check/$f.lean; echo; echo "#print axioms $thm") > /tmp/$f.lean
  echo "== $f"; lake env lean /tmp/$f.lean 2>&1 | grep -E "error|axioms"
done
# Coverage check (no Lean needed):
python3 -c "c=lambda n:n%2==0 or n%4==3 or n%3==2 or n%3==0; print(all((not c(n))==(n%12==1) for n in range(3,100000)))"
```
Re-run on 2026-10-16 (ET): output matched `REPORT.md` exactly.
