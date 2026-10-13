# What Happens When AI Cannot Ask the Right Question?

*Launch draft — computational core reproduced in a separate audit implementation; public release still pending formal-build, packaging, external-replay, and metadata/IP gates.*

Most AI research asks how to improve a system's answers. But sometimes a system fails for a more basic reason: its measurement language cannot express the distinction needed for the task.

I call this kind of failure a **representational hole**.

A representational hole is not simply a hard problem or an unsuccessful search. It occurs when two target-relevant situations remain indistinguishable under a declared representation or measurement language even though the task requires different answers.

The cleanest demonstration in my current research uses elementary cellular automata.

## A frozen language with 2,032 questions

Experiment 012 fixed a low-level measurement language before the final evaluation. Each program:

1. rolls a candidate cellular-automaton rule forward for one of 8 allowed horizons;
2. encodes each periodic three-cell neighborhood;
3. applies one of 254 nonconstant Boolean masks;
4. sums that predicate over every lattice position.

That gives exactly **8 × 254 = 2,032 executable measurement programs**.

Across five ambiguity classes inherited from an earlier blind replication, the selected programs uniquely resolved four classes on fresh states.

The fifth class did something more interesting.

It left **Rule 3 and Rule 17 exactly tied**.

## Why searching harder could not fix it

Under the rule convention used in the experiment,

`f3(a,b,c) = (1-a)(1-b)`

while

`f17(a,b,c) = (1-b)(1-c)`.

This means that one update of Rule 17 is a spatial shift of one update of Rule 3:

`F17(x)_i = F3(x)_{i+1}`.

The same relationship persists under repeated evolution.

Every program in the frozen language applies the same local predicate everywhere and then globally sums over a periodic lattice. Such measurements are translation-invariant: shifting the pattern does not change the answer.

So the failure is stronger than "we tried 2,032 programs and none happened to work."

Within that declared language, **no program can distinguish the pair**.

That is the language-limit certificate.

## Repairing the hole

The next experiment, 012C, froze a small symmetry-breaking extension before its prospective test:

`INDEX_PARITY(i) = i mod 2`.

The new executable question counted active cells at even-indexed positions after one update.

On 256 fresh states:

- Rule 3: **0 mismatches**
- Rule 17: **217 mismatches**
- unique recovery: **yes**

The important idea is not that index parity is profound. It is that the missing capability was diagnosed from the symmetry of the failure, added explicitly, frozen, and then tested prospectively.

## I reran it

For the release audit, I reran the supplied reproduction code and separately reimplemented the cellular-automaton transition and evaluation logic. The second implementation reproduced all five prospective survivor sets, every recorded mismatch count, and the 0-versus-217 result.

I also enumerated all 2,032 frozen-language programs on a separate audit sample for Rules 3 and 17 and found zero separators, consistent with the analytic symmetry proof.

This is still a bounded synthetic result. It is not evidence of AGI, universal ontology invention, or a general new theorem of mathematics. And the other four solvable Experiment-012 classes were not algorithmically difficult: the accompanying paper reports that resolving programs were dense in those finite spaces.

The scientifically interesting result is narrower:

> A system can distinguish ordinary search failure from a certified limitation of a declared measurement language, identify the kind of missing distinction, and test a separately frozen repair.

That suggests a different direction for automated discovery.

When search fails, don't always search harder.

Sometimes the right question is:

**What distinction did my current language erase?**

**Technical evidence:** [GitHub release URL]

**Archived version:** [Zenodo DOI]

**Author:** Derek Earnhart
