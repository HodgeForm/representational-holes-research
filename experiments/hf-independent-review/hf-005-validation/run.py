"""HF-VALIDATION-005: deterministic, preregistered multi-dataset stress test.
Command order: python run.py prepare; python run.py evaluate.
Operationally sealed holdouts; NOT externally independently administered.
"""
import hashlib,itertools,json,sys
from pathlib import Path
from collections import Counter
import numpy as np
import sklearn
from sklearn.datasets import load_digits,load_wine,load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold
ROOT=Path(__file__).resolve().parent
SEED=20261101
N_FOLDS=4
ALPHA_GLOBAL=6.0
ALPHA_LOCAL=12.0
DELTA_CV=0.004
REQUIRED_FOLD_WINS=3
TASK_NAMES=['digits_0_vs_6','digits_2_vs_5','digits_4_vs_9','wine_0_vs_1','breast_cancer']

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def save(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
def load(name):return json.loads((ROOT/name).read_text())

def dataset(task):
 if task.startswith('digits'):
  A=load_digits();pair={'digits_0_vs_6':(0,6),'digits_2_vs_5':(2,5),'digits_4_vs_9':(4,9)}[task]
  keep=np.isin(A.target,pair);x=A.data[keep].astype(float);y=(A.target[keep]==pair[1]).astype(np.int8)
  ink=np.sum(x>=8,axis=1)//4;center=np.sum((x>=8).reshape(-1,8,8)[:,2:6,2:6],axis=(1,2))//3
  # Encode fixed coarse baseline categories with unique integer keys.
  base=(ink*10+center).astype(int)
  binary=(x>=8).astype(np.int8)
 else:
  A=load_wine() if task.startswith('wine') else load_breast_cancer()
  keep=np.isin(A.target,(0,1)) if task.startswith('wine') else np.ones(len(A.target),bool)
  x=A.data[keep].astype(float);y=A.target[keep].astype(np.int8)
  # Use feature summaries in training-only median bins. Median thresholds fitted only to training indices below.
  base=None;binary=None
 return x,y,base,binary

def construct(task):
 x,y,base,binary=dataset(task)
 ix=np.arange(len(y));tr,te=train_test_split(ix,stratify=y,test_size=.4,random_state=SEED+TASK_NAMES.index(task)*11)
 if base is None:
  med=np.median(x[tr],axis=0)
  binary=(x>med).astype(np.int8)
  base=(binary[:,0]*2+binary[:,1]).astype(int)
 usable=[j for j in range(binary.shape[1]) if len(set(binary[tr,j].tolist()))>1]
 # Holdout feature data is available at prediction time, holdout LABELS are only accessed in evaluate().
 return dict(task=task,x=x,y=y,base=base,binary=binary,tr=tr,te=te,usable=usable)

def pred_single_split(base,b,y,train,test,added):
 prior=float(np.mean(y[train]));codes=base.astype(int)
 # Counts by coarse representation.
 bc=np.bincount(codes[train],minlength=int(codes.max()+1)).astype(float)
 bp=np.bincount(codes[train],weights=y[train],minlength=len(bc))
 p_base=(bp+ALPHA_GLOBAL*prior)/(bc+ALPHA_GLOBAL)
 if not added:return p_base[codes[test]]
 nstates=1<<len(added)
 combined=codes*nstates
 for bit,j in enumerate(added):combined=combined+(b[:,j].astype(int)<<bit)
 gcount=np.bincount(combined[train],minlength=int(combined.max()+1)).astype(float)
 gsum=np.bincount(combined[train],weights=y[train],minlength=len(gcount))
 p=(gsum[combined[test]]+ALPHA_LOCAL*p_base[codes[test]])/(gcount[combined[test]]+ALPHA_LOCAL)
 return p

def select(t):
 y=t['y'];tr=t['tr'];base=t['base'];b=t['binary']
 folds=list(StratifiedKFold(n_splits=N_FOLDS,shuffle=True,random_state=SEED+123).split(tr,y[tr]))
 def cv(added):
  v=[];pred=np.zeros(len(tr))
  for ti,vi in folds:
   z=pred_single_split(base,b,y,tr[ti],tr[vi],added)
   v.append(float(np.mean((z-y[tr[vi]])**2)))
   pred[vi]=z
  return float(np.mean((pred-y[tr])**2)),v
 baseline=cv(())
 scores={():baseline}
 for j in t['usable']:scores[(j,)]=cv((j,))
 for a,c in itertools.combinations(t['usable'],2):scores[(a,c)]=cv((a,c))
 winner_single=min((k for k in scores if len(k)==1),key=lambda k:(scores[k][0],k))
 winner_pair=min((k for k in scores if len(k)==2),key=lambda k:(scores[k][0],k))
 def qualifies(candidate,reference):
  val,fold=scores[candidate];ref,r_fold=scores[reference]
  return ref-val >= DELTA_CV and sum(v+1e-12<r for v,r in zip(fold,r_fold))>=REQUIRED_FOLD_WINS
 select=()
 if qualifies(winner_single,()):select=winner_single
 if qualifies(winner_pair,select):select=winner_pair
 return {'baseline':[],'best_single':list(winner_single),'best_pair':list(winner_pair),'deployed':list(select)},\
        {'baseline_cv':baseline[0],'single_cv':scores[winner_single][0],'pair_cv':scores[winner_pair][0],
         'deployed_cv':scores[select][0],'deploy_vs_baseline_cv_gain':baseline[0]-scores[select][0],
         'fold_differences_deployed_vs_baseline':[round(a-b,8) for a,b in zip(baseline[1],scores[select][1])],
         'single_candidate_count':sum(len(k)==1 for k in scores),'pair_candidate_count':sum(len(k)==2 for k in scores)}

def prepare():
 spec={'name':'HF-VALIDATION-005','dataset_tasks':TASK_NAMES,'goal':'cross-dataset predictive value of CV-gated joint binary signatures',
       'criteria':{'predictive_improvement':'deployed method improves held-out Brier vs original baseline in >=4 of 5 tasks; mean Brier gain positive with 95% bootstrap interval lower bound >0; no regression >0.015',
       'compound_specific':'selected pair beats selected single on heldout in >=2 tasks; >=2 pairs must actually have been deployed',
       'integrity':'hashes of all frozen choices/predictions and data labels unchanged and independently recomputed'},
       'design':'Train-only feature selection; 4-fold stratified CV Brier; all individual binary fields and unordered pairs; hierarchical smoothed frequencies; choose added pair only if CV reduction >=0.004 and improved in >=3/4 folds over current best; 40% holdout.',
       'seed':SEED,'alpha_global':ALPHA_GLOBAL,'alpha_local':ALPHA_LOCAL,'folds':N_FOLDS,'sklearn':sklearn.__version__,
       'sealing_limit':'All datasets and labels are publicly available and not externally sequestered; local SHA commitment is not external timestamping',
       'no_post_reveal_tuning':True}
 artifact={'protocol':spec,'tasks':{},'data_hashes':{}}
 for name in TASK_NAMES:
  t=construct(name)
  choices,cv=select(t)
  tr=t['tr'];te=t['te'];y=t['y']
  predictions={label:[round(float(p),12) for p in pred_single_split(t['base'],t['binary'],y,tr,te,vars)] for label,vars in choices.items()}
  artifact['tasks'][name]={'n_train':len(tr),'n_holdout':len(te),'training_indices_hash':sha(tr.tolist()),
    'holdout_indices':te.tolist(),'holdout_label_hash':sha(y[te].tolist()),
    'data_hash':sha({'X':t['x'].tolist(),'y':y.tolist()}),'selected_fields':choices,'cv_scores':cv,'predictions':predictions}
 print('TRAINING-ONLY SELECTED AND FROZEN: '+str([(k, v['selected_fields']['deployed'],v['cv_scores']['deployed_cv']) for k,v in artifact['tasks'].items()]),flush=True)
 artifact['frozen_sha256']=sha({k:v for k,v in artifact.items() if k!='frozen_sha256'})
 save('precommit.json',artifact)
 print('FROZEN SHA-256',artifact['frozen_sha256'],flush=True)

def evaluate():
 z=load('precommit.json');assert z['frozen_sha256']==sha({k:v for k,v in z.items() if k!='frozen_sha256'})
 res={'protocol':'HF-VALIDATION-005','precommit_hash':z['frozen_sha256'],'tasks':{}}
 deltas=[];by_task=[];delta_by_task={}
 for name,entry in z['tasks'].items():
  t=construct(name);assert entry['data_hash']==sha({'X':t['x'].tolist(),'y':t['y'].tolist()})
  assert entry['holdout_indices']==t['te'].tolist()
  assert entry['holdout_label_hash']==sha(t['y'][t['te']].tolist())
  y=t['y'][t['te']]
  m={}
  for label,p in entry['predictions'].items():
   p=np.array(p);m[label]={'brier':float(np.mean((p-y)**2)),'accuracy':float(np.mean((p>=.5)==y))}
  dl=(np.array(entry['predictions']['baseline'])-y)**2-(np.array(entry['predictions']['deployed'])-y)**2
  deltas.extend(dl.tolist());by_task.append(float(np.mean(dl)));delta_by_task[name]=dl
  res['tasks'][name]={'selected_fields':entry['selected_fields'],'cv_scores':entry['cv_scores'],'scores':m,
     'delta_brier_positive_improves':float(np.mean(dl)), 'n_holdout':len(y)}
 # Equal task-weighted uncertainty, bootstrap WITHIN each task.
 rg=np.random.default_rng(SEED+119);boot=[]
 for _ in range(3000):
  vals=[]
  for name,delta in delta_by_task.items():
   vals.append(float(np.mean(rg.choice(delta,size=len(delta),replace=True))))
  boot.append(float(np.mean(vals)))
 interval=np.percentile(boot,[2.5,97.5])
 gains=np.array(by_task)
 pair_deployed=sum(len(t['selected_fields']['deployed'])==2 for t in res['tasks'].values())
 pair_beat_single=sum(t['scores']['best_pair']['brier']<t['scores']['best_single']['brier'] and len(t['selected_fields']['deployed'])==2 for t in res['tasks'].values())
 improvements=sum(g>0 for g in by_task)
 gates={'cross_dataset':bool(improvements>=4 and np.mean(gains)>0 and interval[0]>0 and all(g>=-.015 for g in gains)),
        'compound_specific':bool(pair_deployed>=2 and pair_beat_single>=2)}
 res.update({'equal_task_mean_brier_gain':float(gains.mean()),'equal_task_bootstrap_95pct_ci':interval.tolist(),
             'holdout_tasks_improved':int(improvements),'pair_models_deployed':pair_deployed,'deployed_pairs_beating_singles':pair_beat_single,
             'pass_gates':gates,'final_status':'PASS' if all(gates.values()) else 'NOT_VALIDATED'})
 save('holdout_scoring.json',res);print(json.dumps(res,indent=2))
if __name__=='__main__':
 arg=sys.argv[1] if len(sys.argv)>1 else 'prepare'
 if arg=='prepare':prepare()
 elif arg=='evaluate':evaluate()
 else:raise ValueError(arg)
