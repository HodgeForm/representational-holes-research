import random,json,statistics,hashlib,sys
sys.setrecursionlimit(10000)
from bench import *
import verify
rng=random.Random(SEED); tasks=[gen(rng) for _ in range(N_TASKS)]
for p in tasks: p['oor']=has_oor(p['body'])
# sanity check on chat example shape is done separately in check_chat.py
rows=[]; agg={k:dict(correct=0,abstain_ok=0,wrong=0,miss=0,times=[],mem=[]) for k in METHODS}
nin=sum(not p['oor'] for p in tasks); nout=len(tasks)-nin
for i,p in enumerate(tasks):
    gt,how=verify.truth(p)
    for k,f in METHODS.items():
        out,st,dt,peak=timed(f,p)
        a=agg[k]; a['times'].append(dt); a['mem'].append(peak)
        if out is None:
            if p['oor']: a['abstain_ok']+=1; v='abstain_ok'
            else: a['miss']+=1; v='miss('+st+')'
        elif gt is not None and tuple(out)==tuple(gt): a['correct']+=1; v='correct'
        else: a['wrong']+=1; v='WRONG'
        rows.append(dict(task=i,n_exp=len(str(p['n']))-1,oor=p['oor'],truth=how,method=k,verdict=v,sec=round(dt,4)))
    print(i,how,{r['method']:r['verdict'] for r in rows[-5:]},flush=True)
res={}
for k,a in agg.items():
    oor_ok=a['abstain_ok']+sum(1 for r in rows if r['method']==k and r['oor'] and r['verdict']=='correct')
    res[k]=dict(in_rep_correct=f"{sum(1 for r in rows if r['method']==k and not r['oor'] and r['verdict']=='correct')}/{nin}",
       oor_handled_ok=f"{oor_ok}/{nout}",wrong=a['wrong'],missed_in_rep=a['miss'],
       median_ms=round(statistics.median(a['times'])*1000,3),max_ms=round(max(a['times'])*1000,1),
       peak_mem_kb_max=round(max(a['mem'])/1024,1))
json.dump(dict(tasks=len(tasks),in_rep=nin,out_rep=nout,summary=res),open('results.json','w'),indent=1)
json.dump(rows,open('rows.json','w'))
print(json.dumps(res,indent=1))
