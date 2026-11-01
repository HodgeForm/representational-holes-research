"""HF-COMPOUND-004, reproducible third-party digits benchmark.
Two commands: `python run.py prepare`; `python run.py evaluate`.
The prepare command uses ONLY training labels to choose features and freeze predictions.
The evaluate command checks that the withheld-label SHA256 is unchanged before scoring.
"""
import csv, hashlib, itertools, json, math, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import StratifiedKFold, train_test_split
import sklearn

ROOT=Path(__file__).resolve().parent
SEED=20261101
CLASSES=(3,8)
SPLIT_TEST=0.40
ALPHA=4.0
THRESHOLD=8
N_FOLDS=4

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)
def sha(x): return hashlib.sha256(canon(x).encode('utf-8')).hexdigest()
def pack_json(file,obj): (ROOT/file).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def get_data():
    data=load_digits()
    sel=np.isin(data.target,CLASSES)
    X=data.data[sel].astype(np.int16)
    y=(data.target[sel]==CLASSES[1]).astype(np.int8)
    ix=np.arange(X.shape[0]); tr,te=train_test_split(ix,random_state=SEED,test_size=SPLIT_TEST,stratify=y)
    # Two coarse summary variables from the image, fixed before search.
    b=(X>=THRESHOLD).astype(np.int8)
    ink=np.sum(b,axis=1)//4
    center=np.sum(b.reshape(-1,8,8)[:,2:6,2:6],axis=(1,2))//3
    baseline=np.stack([ink,center],axis=1)
    return X,b,baseline,y,tr,te

def keys_for(base,b,indices,added):
    # Category key for each record. Categorical and deterministic.
    a=base[indices]
    return [tuple(int(z) for z in a[t])+tuple(int(b[indices[t],j]) for j in added) for t in range(len(indices))]

def predict_for(train_idx,test_idx,base,b,y,added):
    hist=defaultdict(lambda:[0,0]); prior=float(y[train_idx].mean())
    kt=keys_for(base,b,train_idx,added)
    for k,lab in zip(kt,y[train_idx]):
        hist[k][0]+=1;hist[k][1]+=int(lab)
    probs=[]; supported=[]
    for k in keys_for(base,b,test_idx,added):
        n,plus=hist.get(k,(0,0))
        probs.append((plus+ALPHA*prior)/(n+ALPHA))
        supported.append(n>0)
    return np.asarray(probs),np.asarray(supported)

def cv_score(idx,base,b,y,added,folds):
    all_p=np.empty(len(idx),dtype=float)
    # folds use positional indices mapped to original data indices
    for ti,vi in folds:
        preds,_=predict_for(idx[ti],idx[vi],base,b,y,added)
        all_p[vi]=preds
    return float(np.mean((all_p-y[idx])**2))

def collision_stats(base,b,y,idx,added):
    groups=defaultdict(lambda:[0,0]);
    for k,lab in zip(keys_for(base,b,idx,added),y[idx]):
        groups[k][int(lab)]+=1
    collisions=sum(x[0]*x[1] for x in groups.values())
    comparable=sum((sum(x)*(sum(x)-1)//2) for x in groups.values())
    return {'conflicting_pairs':collisions,'comparable_pairs':comparable,'collision_rate':round(collisions/comparable,6) if comparable else None,'distinct_representations':len(groups),'singleton_groups':sum(sum(x)==1 for x in groups.values())}

def prepare():
    X,b,base,y,tr,te=get_data()
    folds=list(StratifiedKFold(n_splits=N_FOLDS,shuffle=True,random_state=SEED+42).split(tr,y[tr]))
    # Exclude degenerate constant features, before label-dependent scoring.
    fields=[int(j) for j in range(b.shape[1]) if len(np.unique(b[tr,j]))>1]
    base_cv=cv_score(tr,base,b,y,(),folds)
    single={str(j):cv_score(tr,base,b,y,(j,),folds) for j in fields}
    best_one=min(fields,key=lambda j:(single[str(j)],j))
    # Search ALL pair combinations, including pairs without strong marginal effect.
    scores={}
    for j,k in itertools.combinations(fields,2):
        scores[f'{j},{k}']=cv_score(tr,base,b,y,(j,k),folds)
    best_pair=min(itertools.combinations(fields,2),key=lambda jk:(scores[f'{jk[0]},{jk[1]}'],jk))
    picks={'baseline':[],'single':[best_one],'pair':list(best_pair)}
    frozen={'protocol':'HF-COMPOUND-004','source':'sklearn.datasets.load_digits; UCI Optdigits, scikit-learn v'+sklearn.__version__,
      'dataset_source':'https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html',
      'samples_total':len(y),'training_n':len(tr),'holdout_n':len(te),
      'dataset_row_sha256':sha({'X':X.tolist(),'y':y.tolist()}),
      'training_index_sha256':sha(tr.tolist()),'holdout_index_sha256':sha(te.tolist()),
      'holdout_label_sha256':sha(y[te].tolist()),'split_seed':SEED,'split_fraction':SPLIT_TEST,
      'task':'distinguish digit 3 (0) vs digit 8 (1)',
      'baseline':'number of pixels >=8 /4 (floor); number of central 4x4 pixels >=8 /3 (floor)',
      'raw_features':'8x8 pixel intensity >=8; zero-indexed flattened pixel indices',
      'learner':'categorical-signature class frequency with Laplace-like shrinkage to training prior',
      'smoothing_alpha':ALPHA,'train_selection':'4-fold stratified CV Brier score, all variable pixels and all pairs',
      'usable_raw_fields':len(fields),'single_cv_brier':single[str(best_one)],'pair_cv_brier':scores[f'{best_pair[0]},{best_pair[1]}'],
      'baseline_cv_brier':base_cv,'frozen_features':picks,'frozen_procedure':'No feature changes, new thresholds, or selection after holdout reveal',
      'caveats':['Original labels are public (operationally withheld in selection, not externally sealed).','Data is preexisting and not truly novel scientific discovery.','Only 3 vs 8 subset; coarse representation deliberately chosen; no claim about all-digit generalization.','No remote HodgeForm backend modified.']}
    pred={'protocol':frozen['protocol'],'index':te.tolist(),'probabilities':{},'support':{},'precommit_sha256':None}
    for name,added in picks.items():
        p,s=predict_for(tr,te,base,b,y,added)
        pred['probabilities'][name]=[round(float(v),12) for v in p]
        pred['support'][name]=[bool(v) for v in s]
    # This commitment seals predictions and all choices before holdout labels are read by evaluate.
    pred['precommit_sha256']=sha({k:v for k,v in pred.items() if k!='precommit_sha256'})
    pack_json('frozen_protocol.json',frozen)
    pack_json('frozen_predictions.json',pred)
    pack_json('training_diagnostics.json',{'baseline':collision_stats(base,b,y,tr,()),'single':collision_stats(base,b,y,tr,picks['single']),'pair':collision_stats(base,b,y,tr,picks['pair']),'selection_top_pairs':sorted(scores.items(),key=lambda kv:(kv[1],kv[0]))[:10]})
    # Export a few training cases for optional remote diagnostic smoke test only.
    cases=[]
    for i in tr[:24]:
        cases.append({'id':f'digit-{int(i)}','language_view':{'ink_bucket':int(base[i,0]),'center_bucket':int(base[i,1])},
         'outcome':int(y[i]),'state':{'chosen0':int(b[i,best_pair[0]]),'chosen1':int(b[i,best_pair[1]])}})
    pack_json('remote_training_probe_24.json',cases)
    print(json.dumps({'state':'FROZEN_NO_HOLDOUT_SCORING','training':len(tr),'holdout':len(te),'best_single':picks['single'],'best_pair':picks['pair'],'CV_Brier':{'baseline':base_cv,'single':frozen['single_cv_brier'],'pair':frozen['pair_cv_brier']},'predictions_sha256':pred['precommit_sha256'],'label_commitment_sha256':frozen['holdout_label_sha256'],'training_diagnostics':json.loads((ROOT/'training_diagnostics.json').read_text())},indent=2))

def evaluate():
    protocol=json.loads((ROOT/'frozen_protocol.json').read_text());pred=json.loads((ROOT/'frozen_predictions.json').read_text())
    assert sha({k:v for k,v in pred.items() if k!='precommit_sha256'})==pred['precommit_sha256'],'frozen predictions altered'
    X,b,base,y,tr,te=get_data()
    assert sha(y[te].tolist())==protocol['holdout_label_sha256'],'holdout labels altered'
    assert pred['index']==te.tolist(),'holdout ordering changed'
    assert sha({'X':X.tolist(),'y':y.tolist()})==protocol['dataset_row_sha256'],'dataset altered'
    outcome={};
    for name,probs in pred['probabilities'].items():
        p=np.asarray(probs); true=y[te]
        cm=collision_stats(base,b,y,te,protocol['frozen_features'][name])
        outcome[name]={'accuracy':round(float(np.mean((p>=.5)==true)),4),'brier':round(float(np.mean((p-true)**2)),6),
                       'support_fraction':round(float(np.mean(pred['support'][name])),4),'collisions':cm}
    # Predeclared paired bootstrap, no model changes; descriptive uncertainty, not proof.
    rng=np.random.default_rng(SEED+777)
    pair=np.asarray(pred['probabilities']['pair']);single=np.asarray(pred['probabilities']['single']);basepred=np.asarray(pred['probabilities']['baseline'])
    t=y[te]; n=len(t)
    stats={}
    for label,other in [('pair_vs_baseline',basepred),('pair_vs_single',single)]:
        delta=(other-t)**2-(pair-t)**2
        picks=rng.integers(0,n,size=(2500,n))
        bs=delta[picks].mean(axis=1)
        stats[label]={'brier_gain_positive_is_better':round(float(delta.mean()),6),'bootstrap_95pct_ci':[round(float(z),6) for z in np.percentile(bs,[2.5,97.5])]}
    results={'protocol':protocol['protocol'],'precommit_sha256':pred['precommit_sha256'],'holdout_label_sha256':protocol['holdout_label_sha256'],
             'holdout_count':len(te),'results':outcome,'comparison':stats,
             'is_external_data':True,'is_external_sealed_challenge':False,'remote_plugin_modified':False}
    pack_json('holdout_results.json',results)
    pack_json('remote_holdout_probe_24.json',[{'id':f'digit-{int(i)}','language_view':{'ink_bucket':int(base[i,0]),'center_bucket':int(base[i,1])},'outcome':int(y[i]),'state':{'chosen0':int(b[i,protocol['frozen_features']['pair'][0]]),'chosen1':int(b[i,protocol['frozen_features']['pair'][1]])}} for i in te[:24]])
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'prepare'
    if mode=='prepare':prepare()
    elif mode=='evaluate':evaluate()
    else: raise ValueError(mode)
