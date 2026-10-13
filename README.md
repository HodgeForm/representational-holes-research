# From Search Failure to Language Limit

**Private research release candidate — verified computational core, not yet published**

Author: Derek Earnhart

## Research question

Can a frozen measurement language make distinct dynamics observationally indistinguishable, and can a targeted measurement extension repair the collision?

## Flagship bounded result

Experiment 012 defines a frozen elementary-cellular-automata measurement language containing exactly **2,032 translation-invariant aggregate programs**: 8 evolution horizons × 254 nonconstant local-neighborhood masks.

The supplied historical result and a separate audit reimplementation agree:

- four of five ambiguity classes were uniquely resolved on the prospective evaluation;
- the residual class was Rules **3 and 17**;
- under the supplied rule convention, `F17(x)_i = F3(x)_{i+1}`;
- because every observable in the frozen DSL is translation-invariant, no program in that language can distinguish the pair;
- a separately frozen parity-sensitive extension then produced **0/256 mismatches for Rule 3 and 217/256 for Rule 17**, yielding unique recovery in that prospective sample.

The strongest scientific claim is therefore the **language-relative failure certificate plus prospective repair**, not the difficulty of the search. The accompanying preprint explicitly notes that resolving programs were dense in the other four solvable search spaces.

## Audit status

Completed in this private release candidate:

- plan/result hashes checked;
- supplied replay rerun;
- separate ECA implementation reproduced the reported endpoints and mismatch counts;
- all 2,032 frozen-DSL programs independently enumerated on an audit sample with zero Rule-3/17 separators;
- LanguageLimitBench v0.1.1 release manifest and tests verified;
- Lean source package manifest verified.

Still pending:

- Lean compilation under the pinned toolchain;
- complete public packaging of raw results/audit archive;
- external third-party reproduction;
- metadata, licensing/IP review, DOI creation, and publication approval.

## Non-claims

This result does **not** establish AGI, universal representation repair, autonomous ontology invention, difficult/novel program synthesis, or a new general theorem of quotient mathematics.

See `research/EXP012_REPLICATION_AUDIT_2026-10-12.md`, `RELEASE_GATES.md`, and `EVIDENCE_INVENTORY.md`.
