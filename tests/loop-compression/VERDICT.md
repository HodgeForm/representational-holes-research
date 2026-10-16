On 160 never-before-seen loop programs (plan locked by hash before running), the "exact summary or abstain" method answered every
in-scope problem exactly, up to 10^18 iterations, refused every problem outside its scope, and gave zero wrong answers. Direct
simulation solved only 18 of 115 in time; a symbolic-math solver gave 14 wrong answers. The textbook matrix-power method tied it
exactly on accuracy and safety — they are the same math — and the summary method was ~16x faster per problem (0.1 ms vs 1.6 ms).
Honest bottom line: this proves the method is correct and safe, not that it beats the best established method.
Re-run: cd /workspace/loop-compression-test && pip install sympy && python3 run.py
