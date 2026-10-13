# From Search Failure to Language Limit

A reproducible study of **representational holes**: cases where a frozen measurement language cannot express a distinction required by the task.

## Flagship result

Experiment 012 defines a frozen elementary-cellular-automata measurement language with exactly **2,032 translation-invariant aggregate programs** (8 horizons × 254 nonconstant neighborhood masks).

On the prospective evaluation:

- four of five ambiguity classes were uniquely resolved;
- the residual class was Rules **3 and 17**;
- under the supplied rule convention, `F17(x)_i = F3(x)_{i+1}`;
- because every observable in the frozen DSL is translation-invariant, no program in that language can distinguish the pair;
- a separately frozen parity-sensitive extension produced **0/256 mismatches for Rule 3 and 217/256 for Rule 17**, yielding unique recovery on that prospective sample.

The key contribution is the **language-relative failure certificate plus prospective repair**, not search difficulty.

## Reproduce

See [REPRODUCE.md](REPRODUCE.md).

The repository includes:

- frozen Experiment 012 / 012C plans and results;
- an independent verifier;
- SHA-256 provenance records;
- a Lean formalization artifact;
- a GitHub Actions machine-check receipt.

The Lean project compiled successfully under **Lean 4.32.1 / Mathlib v4.32.1**.

## Scope

This result does **not** establish AGI, universal representation repair, autonomous ontology invention, difficult/novel program synthesis, or generalization beyond the specified bounded setting.

## Independent replication

Independent reproduction reports, discrepancies, and refutations are welcome:

[Independent reproduction issue #2](https://github.com/ImDerekEarnhart/representational-holes-research/issues/2)

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff). A Zenodo DOI is being prepared.
