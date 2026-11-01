"""Check preserved files and documented frozen/held-out results without overwriting frozen evidence."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent

def canon(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False)
def sha_obj(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def load(p): return json.loads((ROOT/p).read_text())

def check():
    manifest=load('MANIFEST_SHA256.json')
    for rel,meta in manifest['files'].items():
        data=(ROOT/rel).read_bytes()
        assert len(data)==meta['bytes'],rel
        assert hashlib.sha256(data).hexdigest()==meta['sha256'],rel
    a=load('hf-004-compound/frozen_predictions.json')
    assert a['precommit_sha256']==sha_obj({k:v for k,v in a.items() if k!='precommit_sha256'})
    assert a['precommit_sha256']=='69fc9b7f7d0ba3af868bd40b7936e837ab165d27196b3ec2173d073082db4244'
    v=load('hf-005-validation/precommit.json')
    assert v['frozen_sha256']==sha_obj({k:x for k,x in v.items() if k!='frozen_sha256'})
    assert v['frozen_sha256']=='4e5d6e02eec66a3ace20ddb4b5ad5928298af44e22727ea419ac3585899a8e0c'
    b=load('hf-004-compound/holdout_results.json')
    assert b['holdout_count']==143
    assert b['results']['pair']['brier']>b['results']['baseline']['brier']
    c=load('hf-005-validation/holdout_scoring.json')
    assert c['final_status']=='PASS' and all(c['pass_gates'].values())
    assert sum(x['n_holdout'] for x in c['tasks'].values())==713
    d=load('hf-005-validation/strong_baseline_exploratory.json')
    # Challenger verdict is documented in the report and should not be suppressed.
    assert len(c['tasks'])==5
    assert set(d)==set(c['tasks'])
    assert all(entry['all_feature_logit_brier'] < entry['selected_pair_or_single_brier'] for entry in d.values())
    null=load('hf-005-validation/negative_control_exploratory.json')
    assert null['tasks_improved']==1 and null['null_passes_four_of_five'] is False
    print('PASS: preserved raw artifact SHA-256 checks, both prediction commitments, and documented trial outcomes')
    print('NOTE: scientific/external verification status remains UNVERIFIED; HF-004 failed predictive holdout improvement.')

if __name__=='__main__': check()
