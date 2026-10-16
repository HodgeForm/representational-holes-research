# DRAFT (not deployed): ORB Genesis service + Genesis->HodgeForm proposal bridge
## A. Companion as service next to Derek OS (Railway)
- Separate Railway service "orb-genesis" in the same project, private networking only (no public domain).
- Dockerfile: python:3.12-slim + elan with pinned leanprover/lean4:v4.19.0 (~600MB image) + orb_genesis.py 0.3.0 (sha-pinned).
- Thin HTTP wrapper (~60 lines, stdlib http.server): POST /discover, POST /validate/{id}, POST /verify, GET /history,
  each shells to the existing CLI functions; requires header X-Archive-Key == ARCHIVE_OS_GATEWAY_KEY (read from env, never logged).
- SQLite at /data/research.db on a Railway volume. Lean 30s timeout already in code; add 1 concurrent job limit, 256KB body cap.
- "Continuous remote execution" = Derek OS calls this service on demand; optional cron that re-verifies stored bundles nightly. No daemon that self-modifies.
## B. Bridge (store != admit)
- Trigger: Derek OS stores a Genesis bundle whose evaluation.status == HELDOUT_SUPPORTED AND service verify returns python_recomputation PASSED.
- Action: write bundle + verification JSON into a dedicated HodgeForm case via orbita_add_inline_file (attachment only) and record
  in Derek OS Decisions as "proposed - awaiting Derek". Labels: admission=PROPOSED, never ADMITTED.
- Optional read-only check: orbita_check_evidence_eligibility(receipt_id, decision_kind) ("never grants admission or activation").
- Never call orbita_promote_improvement, approve_*, governed-improvement or activation tools. Admission stays a manual Derek decision.
- Include caveats in every filed item: synthetic/lookup baselines only; Lean certifies a fixed template lemma, not the study.
## Approvals needed before building: new Railway service (cost), writing to a HodgeForm case (which case_id).
