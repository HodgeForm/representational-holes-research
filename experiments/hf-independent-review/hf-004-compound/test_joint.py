"""Deterministic diagnostic unit test: XOR requires a two-field representation."""
import json
from collections import defaultdict
import numpy as np
from sklearn.model_selection import StratifiedKFold
import run

seed=2077
rng=np.random.default_rng(seed)
X=[]; y=[]
for a in (0,1):
    for b in (0,1):
        for j in range(20):
            X.append((a,b,int(rng.integers(0,2)),int(rng.integers(0,2))))
            y.append(a^b)
X=np.asarray(X,dtype=np.int8);y=np.asarray(y,dtype=np.int8)
base=np.zeros((80,2),dtype=np.int8)
idx=np.arange(len(y)); folds=list(StratifiedKFold(4,shuffle=True,random_state=777).split(idx,y))
cv={
 'base':run.cv_score(idx,base,X,y,(),folds),
 'field0':run.cv_score(idx,base,X,y,(0,),folds),
 'field1':run.cv_score(idx,base,X,y,(1,),folds),
 'joint01':run.cv_score(idx,base,X,y,(0,1),folds)
}
col={k:run.collision_stats(base,X,y,idx,t) for k,t in [('base',()),('field0',(0,)),('field1',(1,)),('joint01',(0,1))]}
assert col['base']['conflicting_pairs']>0
assert col['field0']['conflicting_pairs']>0 and col['field1']['conflicting_pairs']>0
assert col['joint01']['conflicting_pairs']==0
assert cv['joint01']<min(cv['field0'],cv['field1'])
result={'test':'synthetic_XOR_two_feature_repair','status':'PASS','cv_brier':cv,'collisions':col,'interpretation':'Unit test only, not evidence of new scientific discovery'}
run.pack_json('unit_test_results.json',result)
print(json.dumps({'status':'PASS','cv_brier':cv,'conflicting_pairs':{k:v['conflicting_pairs'] for k,v in col.items()}},indent=2))
