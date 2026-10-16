# From Search Failure to Language Limit

A reproducible study of **representational holes**: cases where a frozen measurement language cannot express a distinction required by the task.

## Check it yourself in 2 minutes

```bash
git clone https://github.com/ImDerekEarnhart/representational-holes-research.git
cd representational-holes-research
python3 -m pip install numpy
python3 experiments/exp012/verify_exp012.py
```

Expected output:

```
PASS: Experiment 012 and 012C reproduce the frozen result artifacts.
```

The Lean project under `artifacts/` proves general theorems about an arbitrary representation map, plus a two-bit parity toy. It is not a formalization of the Rule 3 / Rule 17 argument or of the 2,032-program grammar. See [REPRODUCE.md](REPRODUCE.md) for the longer replay, including how to rebuild that Lean project.

## Flagship result

Experiment 012 defines a frozen elementary-cellular-automata measurement language with exactly **2,032 translation-invariant aggregate programs** (8 horizons × 254 nonconstant neighborhood masks).

On the prospective evaluation:

- four of five ambiguity classes were uniquely resolved;
- the residual class was Rules **3 and 17**;
- under the supplied rule convention, `F17(x)_i = F3(x)_{i+1}`;
- because every observable in the frozen DSL is translation-invariant, no program in that language can distinguish the pair;
- a separately frozen parity-sensitive extension produced **0/256 mismatches for Rule 3 and 217/256 for Rule 17**, yielding unique recovery on that prospective sample.

The key contribution is the **language-relative failure certificate plus prospective repair**, not search difficulty.

An early note used both "16 programs" and "2,032 programs" for a baseline. Those are not two sizes of this frozen grammar. The resolution is in [research/CLAIM_AUDIT.md](research/CLAIM_AUDIT.md): the checked-in Experiment 012 language is the 2,032-program language above. The integer 16 in the frozen plan is a horizon length, and Rule 16 is one T05 survivor world.

## Reproduce

See [REPRODUCE.md](REPRODUCE.md). Clone `main` and run the verifier above.

The repository includes:

- frozen Experiment 012 / 012C plans and results;
- an independent verifier;
- SHA-256 provenance records for the files in this tree;
- a Lean formalization artifact (general theorems and a toy example);
- a GitHub Actions machine-check receipt for that Lean project.

The Lean project compiled successfully under **Lean 4.32.1 / Mathlib v4.32.1**.

## Companion: ORB Genesis

[`orb-genesis/`](orb-genesis/) is a separate bounded discovery loop on synthetic finite tables. Its lookup-table baselines are weak, and its Lean certificates prove facts about the exact rows in each file. Re-run commands are in [orb-genesis/README.md](orb-genesis/README.md).

## Scope

This result does **not** establish AGI, universal representation repair, autonomous ontology invention, difficult/novel program synthesis, or generalization beyond the specified bounded setting.

## Independent replication

Independent reproduction reports, discrepancies, and refutations are welcome:

[Independent reproduction issue #2](https://github.com/ImDerekEarnhart/representational-holes-research/issues/2)

## License

Source code is under the MIT License, copyright 2026 Derek Earnhart. See [LICENSE](LICENSE).

Documentation and other prose are under CC-BY-4.0, copyright 2026 Derek Earnhart. See [LICENSE-docs](LICENSE-docs).

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff). A Zenodo DOI is being prepared.
