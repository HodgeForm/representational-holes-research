"""Post-hoc contextual benchmark: regularized logistic regression with all raw features.
Exploratory; NOT part of the preregistered HF005 acceptance gate.
"""
import json
from pathlib import Path
from sklearn.datasets import load_digits,load_wine,load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
import numpy as np
P=Path(__file__).resolve().parent
frozen=json.loads((P/'precommit.json').read_text())
results=json.loads((P/'holdout_scoring.json').read_text())
out={}
allnames=['digits_0_vs_6','digits_2_vs_5','digits_4_vs_9','wine_0_vs_1','breast_cancer']
for name in allnames:
 if name.startswith('digits'):
  data=load_digits();a,b=map(int,name.removeprefix('digits_').split('_vs_')); ix=np.isin(data.target,[a,b]); X=data.data[ix]; y=(data.target[ix]==b).astype(int)
 elif name.startswith('wine'):
  data=load_wine();ix=np.isin(data.target,[0,1]); X=data.data[ix];y=data.target[ix].astype(int)
 else:
  data=load_breast_cancer();X=data.data;y=data.target.astype(int)
 n=allnames.index(name);tr,te=train_test_split(np.arange(len(y)),stratify=y,test_size=.4,random_state=20261101+n*11)
 m=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=1000,random_state=20261101))
 m.fit(X[tr],y[tr]);p=m.predict_proba(X[te])[:,1]
 brier=float(np.mean((p-y[te])**2));acc=float(np.mean((p>=.5)==y[te]))
 out[name]={'all_feature_logit_brier':brier,'all_feature_logit_accuracy':acc,'selected_pair_or_single_brier':results['tasks'][name]['scores']['deployed']['brier'],'full_model_beats_selected':bool(brier<results['tasks'][name]['scores']['deployed']['brier'])}
(P/'strong_baseline_exploratory.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
