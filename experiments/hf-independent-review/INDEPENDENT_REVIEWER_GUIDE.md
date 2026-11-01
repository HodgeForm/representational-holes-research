# Independent reviewer: make and score your own challenge

## Start here (plain English)

Make a small hidden-rule puzzle: give HodgeForm a summary that loses information needed for the answer, and let it request an additional measurement from a fixed menu. Keep the hidden rule and final test answers to yourself.

The question to test is: **Can the submitted system show why the original summary is insufficient, choose a useful extra measurement, and predict fresh cases correctly?**

Start with a finite, deterministic puzzle you can exhaustively check on your own laptop. A successful first puzzle is a case study, not proof of general discovery.

## Suggested first test

Use short binary strings or a small finite-state simulator.

- Pick your own hidden rule for producing a binary answer from the full state.
- Reveal a deliberately coarse summary (for example, a count or aggregate) and training answers.
- Define a small menu of extra measurements. Some should help, some should be redundant, and some should be irrelevant. Give every competing method the same menu and costs.
- Independently verify that two different states have the same initial summary but different correct answers. This pair is an exact witness that no predictor using only that summary can always be correct.
- Ensure at least one allowed measurement repairs the ambiguity in the repairable condition.
- Include a second condition where no allowed measurement, even their permitted combinations, can repair it. Also include a condition where the original summary is already sufficient.

These examples are public suggestions, so do not use a copied parity/XOR puzzle as evidence of unfamiliar discovery. Choose the actual rules, measurements, and final cases privately. Do not ask Derek or the tested assistant to construct or approve the secret answers.

For a first pilot, 8-bit states (256 possibilities) and a menu of roughly 6–12 measurements make exhaustive checking practical. This is a suggested scale, not a statistical power calculation.

## Important: what is executable today?

The HF-004/HF-005 files here replay fixed experiments. They are **not** a general interface for running arbitrary reviewer-authored challenges. The existing replay instructions are in [README.md](README.md).

Before a new challenge starts, Derek must supply a runnable adapter or an agreed hosted interface for the tested HodgeForm version. The reviewer must verify that it accepts the public task and permitted observations, and returns the submission described below. Pin the exact code commit/build, operator list, model and settings, dependencies, and any human assistance.

If that interface is unavailable, record **BLOCKED: test interface unavailable**. An ordinary ChatGPT answer or a manual repair must not be silently reported as autonomous HodgeForm performance. A hosted run tests that hosted system; independent execution of its implementation requires access to that implementation.

## A fair procedure

1. **Reviewer prepares the challenge privately.** Keep generator source, secrets/seeds, complete answer table, scoring code, and final test cases outside the tested system and its workspace. Use a separate process or machine. Split by underlying rule/system when claiming transfer across rules; fresh rows from the same rule only test within-rule prediction.
2. **Agree and freeze the public protocol.** Specify observable inputs, target, allowed measurements and combinations, training access, query/candidate/time budgets, allowed libraries, number of tasks, scoring metrics, tie handling, and the exact failure criteria below. All methods get equivalent information and budgets.
3. **Commit before testing.** Publish a SHA-256 digest of the private challenge bundle before any submissions, using an independently timestamped record. Include a private high-entropy nonce in that bundle so a tiny secret space cannot be guessed from the digest. Retain the exact bytes; a hash alone does not establish time or experimental independence.
4. **Run the frozen system and baselines.** Give only public inputs, training labels, and responses to permitted queries. Log every query, response, proposal, error, elapsed time, and manual intervention. No hidden test feedback, secret filesystem access, or extra hints. Discovery queries must never access final holdout answers.
5. **Lock submissions before revealing answers.** Each method submits its selected measurements, executable predictor, diagnosis, witnesses or certificates, and predictions for the fixed hidden-label cases. Timestamp and hash these exact submissions. Set one common submission deadline.
6. **Reviewer scores independently.** Run each frozen predictor against the private answer table using the reviewer's own scorer. Exhaustively check certificates on the finite domain where feasible. Record every task, including failures and abstentions.
7. **Publish the audit.** After scoring, reveal the exact committed bundle and nonce, verify its hash, publish submissions, logs, versions, per-task scores, and the independently authored report. If the secrets cannot be released, state that public reproducibility is limited. Any repair after reveal belongs to a new experiment with new hidden cases.

Do not put private answers in a public GitHub issue, draft branch, or PR before the submission deadline.

## What each method must return

A machine-readable submission should contain:

- task ID and exact system/build ID;
- decision: `repair`, `already_sufficient`, `insufficient_within_budget`, or `error`;
- initial collision witness: two state IDs, their shared representation, and differing target values (where such evidence is accessible from allowed queries);
- selected measurement IDs and cost;
- executable predictor plus predictions, keyed by case ID;
- scope of each claim: observed sample, held-out cases, or complete finite domain;
- proof/certificate, or explicit statement that no certificate was obtained;
- full query log and runtime/budget accounting.

Failure to find a repair is not a proof that none exists. A justified impossibility claim needs a valid witness under the strongest permitted representation, or another independently checked exhaustive argument. The reviewer may verify hidden witnesses privately; do not supply forbidden labels to help the system produce them.

## Baselines and scoring

At minimum compare:
1. A predictor using only the original summary.
2. Exhaustive or adaptive search over the same allowed measurements and combinations, with the same budget.
3. A conventional predictor using all permitted measurements, when allowed by the budget. If it exceeds that budget, report it separately as an informational upper reference.

For deterministic finite puzzles, freeze these criteria before the run:

| Claim | Reviewer checks |
| --- | --- |
| Initial representation is insufficient | Exact same-summary/different-answer pair; recompute both from the private generator |
| Repair succeeds | Frozen predictor gets every final test answer correct; report exact numerator/denominator |
| Repair is globally sufficient | Every fiber of the repaired representation has a constant target across the entire finite domain |
| No permitted repair exists | A collision remains even under all jointly permitted measurements, or exhaustive checking covers every permitted combination |
| No repair was needed | Original representation is sufficient on the full finite domain |
| Method beats search | Better preregistered accuracy/cost tradeoff than the equal-budget strong search baseline across fresh tasks, not merely one successful example |

A holdout pass is not a global proof. Lower-cost repair is not established unless costs and the comparison were frozen. Keep abstentions, false repairs, errors, and budget overruns separate. Include noisy or continuous problems only after defining suitable error tolerances and uncertainty estimates; exact finite criteria do not automatically transfer to those domains.

## Report template

- Reviewer and relationship to project:
- Protocol timestamp/digest:
- Challenge commitment and reveal digest match:
- Tested code/build/model and human involvement:
- Scorer implementation and environment:
- Secret leakage or protocol deviations:
- For each task: condition, decision, correct/total, collision verified, repair verified, queries, runtime, baseline results:
- All failed cases and false repair claims:
- Verdict: BLOCKED / PROTOCOL INVALID / FAILED / PASSED THIS FINITE TEST:
- What the result does and does not establish:

**Interpretation:** Independent replay checks the old evidence. An independently authored sealed challenge checks a new capability. Success on either does not by itself establish a new physical law, autonomous general discovery, or superiority over strong conventional methods.
