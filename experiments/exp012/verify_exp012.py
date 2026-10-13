import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

EXPECTED_PLAN_SHA = "05d6847671e8abb09e204ba65b71089b5a08be66e7171b6ab97465fc320df24d"
EXPECTED_RESULT_SHA = "fcba9e867f360f6af2b9fdafa0c8ab41a0b1ea5da0ee92faf5e1871eac4104a1"
EXPECTED_012C_PLAN_SHA = "0db4f655219ce8f1336ac1d6ba4a3d4269b87a02eba1461b3b1f0d02a78a52e5"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step(states, rule):
    left = np.roll(states, 1, axis=1)
    center = states
    right = np.roll(states, -1, axis=1)
    idx = (left << 2) | (center << 1) | right
    return ((rule >> idx) & 1).astype(np.uint8)


def generate_states(width, count, seed):
    rng = np.random.default_rng(seed)
    ps = rng.uniform(0.12, 0.88, size=count)
    return np.vstack([(rng.random(width) < p).astype(np.uint8) for p in ps])


def program(states, rule, horizon, mask):
    s = states.copy()
    for _ in range(horizon):
        s = step(s, rule)
    code = (np.roll(s, 1, axis=1) << 2) | (s << 1) | np.roll(s, -1, axis=1)
    return np.isin(code, [k for k in range(8) if (mask >> k) & 1]).sum(axis=1)


plan_path = HERE / "exp012_frozen_plan.json"
primary_path = HERE / "exp012_primary_results.json"
complete_path = HERE / "exp012_complete_results.json"
plan012c_path = HERE / "exp012c_frozen_plan.json"

assert sha256(plan_path) == EXPECTED_PLAN_SHA
assert sha256(primary_path) == EXPECTED_RESULT_SHA
assert sha256(plan012c_path) == EXPECTED_012C_PLAN_SHA

plan = json.loads(plan_path.read_text())
primary = json.loads(primary_path.read_text())
complete = json.loads(complete_path.read_text())

assert len(plan["grammar"]["allowed_horizons"]) * 254 == 2032
assert complete["primary_unique_recovery"] == "4/5"
assert complete["exp012c"]["hidden_mismatches"] == 0
assert complete["exp012c"]["competitor_mismatches"] == 217

hidden = {"T01": 56, "T03": 202, "T04": 158, "T05": 3, "T06": 78}
trial_order = ["T01", "T03", "T04", "T05", "T06"]

for j, tid in enumerate(trial_order):
    t = plan["trials"][tid]
    width = plan["prospective"]["sizes"][tid]
    states = generate_states(width, plan["prospective"]["states_per_trial"], plan["prospective"]["state_seed_base"] + j)
    p = t["synthesized_program"]
    y = program(states, hidden[tid], p["horizon"], p["mask"])
    exact = []
    mismatches = {}
    for rule in t["survivor_rules"]:
        pred = program(states, rule, p["horizon"], p["mask"])
        mismatches[str(rule)] = int(np.count_nonzero(pred != y))
        if np.array_equal(pred, y):
            exact.append(rule)
    expected = primary["primary_trials"][tid]
    assert exact == expected["exact_survivors"], (tid, exact, expected["exact_survivors"])
    assert mismatches == expected["mismatches"], tid

c = json.loads(plan012c_path.read_text())
states = generate_states(c["prospective"]["N"], c["prospective"]["states"], c["prospective"]["state_seed"])

def even_active(states, rule):
    return step(states, rule)[:, ::2].sum(axis=1)

hidden_y = even_active(states, 3)
m3 = int(np.count_nonzero(even_active(states, 3) != hidden_y))
m17 = int(np.count_nonzero(even_active(states, 17) != hidden_y))
assert (m3, m17) == (0, 217)

# Directly stress-check the stated shift identity across several horizons.
rng = np.random.default_rng(20261013)
states = rng.integers(0, 2, size=(128, 193), dtype=np.uint8)
a = states.copy()
b = states.copy()
for h in range(1, 9):
    a = step(a, 3)
    b = step(b, 17)
    assert np.array_equal(b, np.roll(a, -h, axis=1)), h

print("PASS: Experiment 012 and 012C reproduce the frozen result artifacts.")
