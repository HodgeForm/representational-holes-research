"""Independent holdout metric check, separate from run.py scoring routines."""
import hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
P=Path(__file__).parent
frozen=json.loads((P/'frozen_protocol.json').read_text());pred=json.loads((P/'frozen_predictions.json').read_text());result=json.loads((P/'holdout_results.json').read_text())
canon=lambda o:json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=True)
h=lambda o:hashlib.sha256(canon(o).encode()).hexdigest()
assert h({k:v for k,v in pred.items() if k!='precommit_sha256'})==pred['precommit_sha256']
data=load_digits();mask=np.isin(data.target,[3,8]);X=data.data[mask];y=(data.target[mask]==8).astype(int)
all_idx=np.arange(len(y));train,test=train_test_split(all_idx,test_size=.4,stratify=y,random_state=20261101)
assert test.tolist()==pred['index'];assert h(y[test].tolist())==frozen['holdout_label_sha256']
B=(X>=8).astype(int);ink=B.sum(1)//4;center=B.reshape(-1,8,8)[:,2:6,2:6].sum((1,2))//3
check={};
for name,fields in frozen['frozen_features'].items():
  p=np.array(pred['probabilities'][name]);label=y[test]
  assert len(p)==len(label)
  brier=float(((p-label)**2).mean());acc=float(((p>=0.5)==label).mean())
  groups=defaultdict(lambda:[0,0])
  for i in test:
    key=(int(ink[i]),int(center[i]))+tuple(int(B[i,j]) for j in fields)
    groups[key][int(y[i])]+=1
  collisions=sum(a*b for a,b in groups.values())
  assert round(brier,6)==result['results'][name]['brier'];assert round(acc,4)==result['results'][name]['accuracy'];assert collisions==result['results'][name]['collisions']['conflicting_pairs']
  check[name]={'brier':round(brier,6),'accuracy':round(acc,4),'conflicting_pairs':collisions}
verified={'status':'PASS','independent_reimplementation':True,'separate_source':True,'records':len(test),'precommit_sha256':pred['precommit_sha256'],'recomputed':check}
(P/'independent_verification.json').write_text(json.dumps(verified,indent=2)+'\n')
print(json.dumps(verified,indent=2))
