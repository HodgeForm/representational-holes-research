# What the per-study Lean check does NOT prove (written before reporting results; 2026-10-16)
1. Finite data only: it proves facts about the exact rows in this file (a conflict between two rows; the rule's predictions on these validation rows). It says nothing about any row not in the file.
2. Not a general theorem: "the rule fits 8/8 held-out rows" is not "the rule is true". New data can still refute it.
3. Encoding is trusted: Python writes the Lean file from the stored study. Lean proves the claims about the data as written; it cannot tell if the measurements, labels, or the JSON were wrong, fabricated, or leaked.
4. Lean semantics of the rule (field/eq/xor/sum/diff, lookup-table prediction) are a re-implementation of the Python engine; agreement with Python is checked, not proven equivalent.
5. It does not prove the rule is causal, novel, best, or better than strong baselines; only that it beats the built-in lookup baselines on these rows.
6. It does not certify the search was honest (e.g. that labels were unseen at selection time); that rests on the freeze hash and the store's history.
7. A "REFUTED" certificate proves one specific counterexample row; it does not prove no better rule exists.
