# From Search Failure to Language Limit

**Private research release candidate — computational and formal CI checks pass; not yet public**

Author: Derek Earnhart

## Research question

Can a frozen measurement language make distinct dynamics observationally indistinguishable, and can a targeted measurement extension repair the collision?

## Flagship bounded result

Experiment 012 defines a frozen elementary-cellular-automata measurement language containing exactly **2,032 translation-invariant aggregate programs**: 8 evolution horizons × 254 nonconstant local-neighborhood masks.

The supplied result and a separate audit reimplementation agree:

- four of five ambiguity classes were uniquely resolved prospectively;
- the residual class was Rules **3 and 17**;
- under the supplied rule convention, `F17(x)_i = F3(x)_{i+1}`;
- because every observable in the frozen DSL is translation-invariant, no program in that language can distinguish the pair;
- a separately frozen parity-sensitive extension produced **0/256 mismatches for Rule 3 and 217/256 for Rule 17**, yielding unique recovery on that prospective sample.

The strongest scientific claim is therefore the **language-relative failure certificate plus prospective repair**, not the difficulty of the search. The preprint explicitly notes that resolving programs were dense in the other four solvable search spaces.

## Verification status

Completed:

- frozen plan/result SHA-256 values checked;
- supplied replay rerun;
- separate ECA implementation reproduced the prospective endpoints and mismatch counts;
- all 2,032 frozen-DSL programs independently enumerated on an audit sample with zero Rule-3/17 separators;
- LanguageLimitBench v0.1.1 release manifest and tests verified;
- exact Lean artifact reconstructed from its recorded SHA-256;
- Lean source scanned for unfinished proof placeholders;
- **Lean 4.32.1 / Mathlib v4.32.1 build passed in GitHub Actions (8659 jobs).**

See `formal/LEAN_CI_RECEIPT.md` and `REPRODUCE.md`.

Still pending before public launch:

- external third-party reproduction;
- final manuscript author/contact/DOI fields;
- metadata and licensing/IP review;
- explicit approval to make the repository public and mint a Zenodo DOI.

## Non-claims

This result does **not** establish AGI, universal representation repair, autonomous ontology invention, difficult/novel program synthesis, or a new general theorem of quotient mathematics.

See `research/EXP012_REPLICATION_AUDIT_2026-10-12.md`, `RELEASE_GATES.md`, and `EVIDENCE_INVENTORY.md`.
