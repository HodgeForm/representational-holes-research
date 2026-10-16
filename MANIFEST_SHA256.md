# Source artifact SHA-256 manifest

These hashes identify files shipped in this repository. Hashes of staging uploads that are not in the tree are kept only as history in `research/archive/MANIFEST_SHA256_staging.md`.

| File | SHA-256 |
|---|---|
| `experiments/exp012/exp012_frozen_plan.json` | `05d6847671e8abb09e204ba65b71089b5a08be66e7171b6ab97465fc320df24d` |
| `experiments/exp012/exp012_primary_results.json` | `fcba9e867f360f6af2b9fdafa0c8ab41a0b1ea5da0ee92faf5e1871eac4104a1` |
| `experiments/exp012/exp012c_frozen_plan.json` | `0db4f655219ce8f1336ac1d6ba4a3d4269b87a02eba1461b3b1f0d02a78a52e5` |
| `experiments/exp012/exp012_complete_results.json` | `8696747031786ac2cad5783f300a93a22f46c64ab8c25533efffd7b0b372e874` |
| Lean artifact ZIP reconstructed from `artifacts/orbita_language_limit_lean_v0_1.zip.b64` | `3ff0a2bf1034a34111f5060bdafe947daf46c3245f6a894d55a168b700b2409c` |

`experiments/exp012/verify_exp012.py` checks the plan, primary-result, and 012C-plan hashes on every run.
