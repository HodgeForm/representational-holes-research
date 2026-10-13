# Claim audit — provisional

## Reported
- A translation-invariant measurement DSL failed to distinguish ECA Rules 3 and 17.
- A parity-sensitive extension reportedly separated the rules on 217/256 evaluated states.
- Prior documents variously describe the baseline as 16 programs and 2,032 programs. **These are not interchangeable**; determine whether they describe distinct grammar versions/experiments before publicizing a single count.

## Proof obligations
- Specify boundary conditions, lattice length, observation horizon, rule convention, grammar, and equivalence notion.
- Check shift relationship for the exact rule convention and all stated time steps.
- Confirm whether the claimed equivalence is pointwise per state, after shifting input, or distributional. Do not conflate these.
- Validate independent checker logs and complete test counts.
- Confirm the parity repair was frozen before evaluating untouched states.

## Not established
- Universal representation repair or AI self-improvement.
- Minimality of the added primitive.
- Independent reproduction of the original published numbers.

## Source pointers
Earlier Publication_Dossier.md cites Executable_Questions_Open_Source_Kit_v0.3.0.zip, LanguageLimitBench_v0.1.1_PUBLIC.zip, From_Search_Failure_to_Language_Limit(3).tex, and Focused_Paper_Preprint_2026-09-21_v1.6.tex. Original binaries have not yet been inspected for this repository.
