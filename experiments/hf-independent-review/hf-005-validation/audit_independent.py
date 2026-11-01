"""Independent-source, no imports from run.py. Recompute frozen HF005 predictions and scores.
This is a LOCAL independent implementation, NOT a third-party auditor or seal.
"""
from pathlib import Path
import hashlib, json, math, statistics
from collections import defaultdict
import numpy as np
from sklearn.datasets import load_digits,load_wine,load_breast_cancer
from sklearn.model_selection import train_test_split
BASE=Path(__file__).resolve().parent
frozen=json.loads((BASE/'precommit.json').read_text())
reported=json.loads((BASE/'holdout_scoring.json').read_text())
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
hashv=lambda x:hashlib.sha256(canonical(x).encode()).hexdigest()
assert hashv({k:v for k,v in frozen.items() if k!='frozen_sha256'})==frozen['frozen_sha256']
assert frozen['frozen_sha256']==reported['precommit_hash']
results={}

def source(name):
 if name.startswith('digits'):
  raw=load_digits(); aa,bb=map(int,name.replace('digits_','').split('_vs_'))
  include=(raw.target==aa)|(raw.target==bb)
  X=raw.data[include].astype(float);Y=(raw.target[include]==bb).astype(int)
 elif name.startswith('wine'):
  raw=load_wine();include=(raw.target==0)|(raw.target==1)
  X=raw.data[include].astype(float);Y=raw.target[include].astype(int)
 else:
  raw=load_breast_cancer();X=raw.data.astype(float);Y=raw.target.astype(int)
 return X,Y

def predict(train,test,coarse,binarized,labels,fields):
 freq=defaultdict(lambda:[0,0]);prior=sum(int(labels[i]) for i in train)/len(train)
 for i in train:
  z=freq[int(coarse[i])];z[0]+=1;z[1]+=int(labels[i])
 def bp(i):
  n,pos=freq[int(coarse[i])]
  return (pos+6.0*prior)/(n+6.0)
 if not fields:return [bp(i) for i in test]
 secondary=defaultdict(lambda:[0,0])
 def key(i):return int(coarse[i]),tuple(int(binarized[i,j]) for j in fields)
 for i in train:
  z=secondary[key(i)];z[0]+=1;z[1]+=int(labels[i])
 return [(secondary[key(i)][1]+12.0*bp(i))/(secondary[key(i)][0]+12.0) for i in test]

for number,(name,rec) in enumerate(frozen['tasks'].items()):
 X,Y=source(name)
 tri,tei=train_test_split(np.arange(len(Y)),stratify=Y,test_size=0.4,random_state=20261101+['digits_0_vs_6','digits_2_vs_5','digits_4_vs_9','wine_0_vs_1','breast_cancer'].index(name)*11)
 assert rec['data_hash']==hashv({'X':X.tolist(),'y':Y.tolist()})
 assert rec['holdout_indices']==tei.tolist()
 assert rec['holdout_label_hash']==hashv(Y[tei].tolist())
 if name.startswith('digits'):
  B=(X>=8).astype(int)
  pixels=B.reshape((-1,8,8))
  base=(pixels.sum((1,2))//4)*10+(pixels[:,2:6,2:6].sum((1,2))//3)
 else:
  B=(X>np.median(X[tri],axis=0)).astype(int)
  base=B[:,0]*2+B[:,1]
 check={}
 for model,fields in rec['selected_fields'].items():
  p=predict(tri.tolist(),tei.tolist(),base,B,Y,fields)
  frozen_p=rec['predictions'][model]
  assert all(abs(a-b)<1e-10 for a,b in zip(p,frozen_p)),f'Independent prediction mismatch for {name}: {model}'
  brier=statistics.fmean((pp-int(Y[i]))**2 for pp,i in zip(p,tei))
  acc=statistics.fmean(int((pp>=0.5)==Y[i]) for pp,i in zip(p,tei))
  assert abs(brier-reported['tasks'][name]['scores'][model]['brier'])<1e-10
  assert abs(acc-reported['tasks'][name]['scores'][model]['accuracy'])<1e-10
  check[model]={'brier':brier,'accuracy':acc}
 results[name]={'predictions_recalculated':True,'scores':check,'n_holdout':len(tei)}
mean_gain=statistics.fmean(results[k]['scores']['baseline']['brier']-results[k]['scores']['deployed']['brier'] for k in results)
assert abs(mean_gain-reported['equal_task_mean_brier_gain'])<1e-12
assert reported['pass_gates']['cross_dataset'] and reported['pass_gates']['compound_specific']
out={'status':'LOCAL_INDEPENDENT_CODE_REPLAY_PASS','frozen_sha256':frozen['frozen_sha256'],'holdout_predictions_exactly_recomputed':sum(d['n_holdout'] for d in results.values()),'tasks':results,'mean_brier_gain':mean_gain,'caveats':['same environment and public dataset sources, not an external evaluator','original script designed benchmark, not externally blinded','does not validate superiority over unrestricted full-feature standard predictors']}
(BASE/'independent_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':out['status'],'frozen_sha256':out['frozen_sha256'],'predictions_recomputed':out['holdout_predictions_exactly_recomputed'],'mean_brier_gain':mean_gain},indent=2))
