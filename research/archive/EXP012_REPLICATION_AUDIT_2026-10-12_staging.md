> **Archived staging note.** This memo is historical. It names uploads that are not in this repository. The public claim is `research/CLAIM_AUDIT.md` and the frozen files under `experiments/exp012/`. Instructions below to keep the repository private, or to treat the flagship result as unverified, are obsolete where they conflict with those public artifacts. See `research/archive/README.md`.

# Experiment 012 / 012C replication audit — 2026-10-12

## Verdict

The newly supplied Experiment 012 artifacts materially clear the main technical evidence gap for the Rule 3 / Rule 17 flagship example.

This audit independently reran the supplied reproduction script and also reimplemented the ECA transition, aggregate observable, prospective evaluation, and parity repair separately. Both paths reproduced the reported endpoints.

This is a computational replication of the supplied frozen artifacts, **not** a blind clean-room replication of the historical experiment.

## Artifact fingerprints

- `Experiment_012_Autonomous_Question_Program_Synthesis_Audit(2).zip`
  - SHA-256: `2c02c4510a61f422062a32e8e2695a6cb75bd35c932080e93f8bf0ab6426f1f2`
- `exp012_frozen_plan.json`
  - SHA-256: `05d6847671e8abb09e204ba65b71089b5a08be66e7171b6ab97465fc320df24d`
- `exp012_primary_results.json`
  - SHA-256: `fcba9e867f360f6af2b9fdafa0c8ab41a0b1ea5da0ee92faf5e1871eac4104a1`
- `exp012c_frozen_plan.json`
  - SHA-256: `0db4f655219ce8f1336ac1d6ba4a3d4269b87a02eba1461b3b1f0d02a78a52e5`
- `exp012_complete_results.json`
  - SHA-256: `8696747031786ac2cad5783f300a93a22f46c64ab8c25533efffd7b0b372e874`

The four separately uploaded JSON files were byte-identical to the copies inside the Experiment 012 audit ZIP. The hash references embedded in the complete-results file matched the actual plan/result files.

## Frozen DSL

The plan defines exactly:

- horizons: `{1,2,4,8,12,16,24,30}`;
- masks: `1..254`, excluding constant masks 0 and 255;
- periodic three-cell encoding: `CODE3(i)=4*x[i-1]+2*x[i]+x[i+1]`;
- Boolean mask membership;
- global sum across lattice sites.

Therefore the primary search language contains exactly **8 × 254 = 2,032 programs**.

Earlier project notes that mention a 16-program language should not be presented as the Experiment 012 denominator unless a distinct earlier experiment is explicitly identified. For the supplied Exp012 package, 2,032 is the correct frozen DSL size.

## Supplied reproduction script

Running:

```sh
python exp012_reproduce.py
```

reproduced:

- T01 -> exact survivor `[56]`
- T03 -> exact survivor `[202]`
- T04 -> exact survivor `[158]`
- T05 -> residual exact class `[3,17]`
- T06 -> exact survivor `[78]`
- 012C Rule 3 mismatches -> `0`
- 012C Rule 17 mismatches -> `217`

## Separate reimplementation

A second implementation was written for this audit without importing the supplied reproduction module. It used explicit periodic left/right arrays, a separately constructed ECA lookup table, and independently reconstructed aggregate outputs.

Results:

- all five prospective survivor sets matched the supplied result file;
- every per-rule mismatch count matched the supplied result file;
- 012C reproduced **0** Rule-3 mismatches and **217** Rule-17 mismatches;
- the identity `F17^h(x) = shift_left^h(F3^h(x))` was checked numerically for multiple horizons;
- all **2,032** frozen-DSL programs were enumerated on an independent audit sample for Rules 3 and 17, with **0 resolving programs**.

## Analytic certificate

Under the rule convention used by the supplied code,

- Rule 3: `f3(a,b,c)=(1-a)(1-b)`
- Rule 17: `f17(a,b,c)=(1-b)(1-c)`

so

`F17(x)_i = F3(x)_{i+1}`.

Iterating gives a spatial shift after each horizon. Because every primary-DSL observable applies the same local predicate everywhere and then globally sums over a periodic lattice, the observable is translation-invariant. Thus Rules 3 and 17 are indistinguishable throughout this declared DSL.

This is the strongest part of the result: the failure is language-relative but grammar-wide, rather than "we searched many programs and none worked."

## 012C repair

The separately frozen extension adds

`INDEX_PARITY(i) = i mod 2`

and evaluates even-index activity after one step. On the frozen prospective sample:

- hidden Rule 3: 0 / 256 mismatches;
- competitor Rule 17: 217 / 256 mismatches;
- unique recovery: true.

## Scope

What this audit now supports:

> In this bounded ECA setting, a declared translation-invariant 2,032-program measurement language cannot distinguish Rules 3 and 17 because the two dynamics are related by a spatial shift; a separately frozen parity-sensitive extension prospectively breaks that collision on the specified fresh sample.

What it does **not** establish:

- universal representational repair;
- AGI or autonomous ontology invention;
- difficult/novel search (resolving programs are dense for four other classes);
- minimality of index parity among all conceivable extensions;
- independent historical priority or peer review.

## Remaining gates

1. Put the complete raw result JSONs and original audit archive into the repository/release, not only the plans and replay script.
2. Compile/check the supplied Lean artifact under its pinned Lean/Mathlib toolchain.
3. Run a third-party or separately hosted reproduction from the public release.
4. Finalize author identity, citation metadata, licensing, and IP/public-disclosure review.
