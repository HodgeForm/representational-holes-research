# Harder test results (prereg sha256 945d9113...a1df771)
H1 XOR: PASS. Selected eq(a,b) (equivalent partition to xor; tie-break by id). 8/8, HELDOUT_SUPPORTED, advantage +1.0; all baselines 0/8 (abstain).
H2 flipped labels: PASS. REFUTED, exactly 2 counterexamples retained (val-16, val-21).
H3 spurious trap: as predicted, engine picked cheap shortcut field c, REFUTED 4/8 wrong. Failure is caught at validation, not avoided.
Lean: KERNEL_CHECKED in all 3, identical source hash e38e9181194c -> Lean checks a fixed template lemma, not anything study-specific.
Forged status (REFUTED->HELDOUT_SUPPORTED) rejected by verify: see run log.
Caveat: baselines are exact-lookup tables that abstain on unseen vectors; a decision tree/logistic model with interaction would also get 8/8 on H1.
