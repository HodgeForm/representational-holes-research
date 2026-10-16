# ORB Genesis 0.3 acceptance record — 2026-10-16

## Implemented and exercised

- Persistent hosted discovery runs with conditional writes, per-user isolation, idempotency and event/state hashes.
- Training-only candidate selection over a fixed field/equality/XOR/sum/difference grammar; predictions frozen before validation labels.
- One-shot validation with explicit abstention, retained counterexamples and current-language/single-field/all-field lookup baselines.
- Candidate-disagreement experiment suggestions. These are proposals, not physical experiment execution.
- Related refuters retained across runs from the same source. No automatic grammar or policy changes.
- Python implementation with SQLite storage, command line operation and a local stdio MCP server.
- Python recomputation of hosted-format bundles and a restricted Lean proof adapter accepting only the generated finite-collision template.
- Web interface integration tests exercised startup, synthetic demo, freeze, scoring, rendering, refresh and invalid JSON.

## Observed results

The synthetic phase fixture has 8 conflicting training pairs. The selected phase field predicts 8/8 validation rows correctly. The single-field baseline also predicts 8/8: there is no demonstrated advantage over that baseline. Reversing the validation labels refutes the selected candidate and retains all 8 counterexamples. A separate XOR fixture exercises composition of supplied fields. These are development acceptance fixtures, not blind scientific benchmarks.

Seven Python tests passed with the real Lean 4.19.0 executable, including cross-implementation recomputation, rejection of forged predictions, rejection of modified proof source/encoding, SQLite lifecycle, local MCP startup/call, and negative Lean controls. Lean rejected an invalid equality proof; the incomplete-proof control exposed `sorryAx`; a fabricated axiom was visible in the axiom report.

The actual generated obstruction proof compiled successfully. Lean printed:

```
'obstruction' does not depend on any axioms
```

Proof source SHA-256: `e38e9181194c13fc340ea8ab5f562fdaf8b408e87015304a8aab1d2e306c6747`
Compiler executable SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`
Lean version: `4.19.0`, release commit prefix `6caaee842e94`.

This hosted development environment required a small compatibility library redirecting its own `/proc/PID/exe` lookup to `/proc/self/exe`. It did not change Lean proof code or the kernel. Shim SHA-256: `663f5f91cf423a1e13378956e23427e4e0619292c02188ff30ee11323e22e133`.

## Remaining boundaries

The hosted Site does not execute Lean; the local companion does. Neither an exported source file nor a caller-supplied verification report is automatically admitted as proof. The Python/JavaScript implementations are same-author implementations, not independent research teams. Browser visual/sign-in testing, Windows execution, Archive OS ingestion, automatic HodgeForm admission, arbitrary theorem proving, production scheduling, physical experiment control, autonomous policy promotion and scientific novelty have not been established by this release.

The complete general discovery machine remains a research and engineering goal. This release is a functioning bounded discovery loop and proof-checking companion.
