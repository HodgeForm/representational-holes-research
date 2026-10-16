#!/usr/bin/env python3
"""ORB Genesis -> HodgeForm proposal bridge (outbox only; store != admit)."""
import sys, json, sqlite3, pathlib, subprocess, glob, time
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parent
sys.path.insert(0,str(ROOT)); import orb_genesis as og
sys.path.insert(0,str(ROOT/'v2')); import leancert
LEDGER=HERE/'ledger.json'; OUT=HERE/'outbox'; OUT.mkdir(exist_ok=True)
LEAN=subprocess.run([str(pathlib.Path.home()/'.elan/bin/elan'),'which','lean'],capture_output=True,text=True,cwd=ROOT).stdout.strip() or None
NOTE_OLD=("The Lean KERNEL_CHECKED status covers only the fixed built-in lemma 'obstruction' (no function maps 0 to both 0 and 1), "
      "identical for every study. It does NOT verify this study; the data link and scoring are checked by Python recomputation only. "
      "Baselines are exact-lookup tables. Admission status: PROPOSED (store != admit).")
NOTE=("verification.lean_status (KERNEL_CHECKED) covers only the fixed built-in lemma, not this study. study_lean (v2) encodes this study's "
      "actual rows and proves (a) the original-representation conflict and (b) the held-out claim, by `decide`. It is finite-data only, not a general theorem; "
      "see v2/LIMITS.md in this orb-genesis directory. Baselines are exact-lookup tables. Admission status: PROPOSED (store != admit).")
ledger=json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
dbs=[pathlib.Path(p) for p in sys.argv[1:]] or [pathlib.Path(p) for p in glob.glob(str(ROOT/'**/*.db'),recursive=True)]
report=[]
for db in dbs:
    for (body,) in sqlite3.connect(db).execute('SELECT body FROM runs'):
        run=json.loads(body); b=og.bundle(run); h=og.digest(b); rid=run['id']; ev=run.get('evaluation')
        st=ev and ev['status']
        if h in ledger: report.append((rid,db.name,'SKIP already bridged')); continue
        if st!='HELDOUT_SUPPORTED': report.append((rid,db.name,f'SKIP status={st}')); continue
        try: v=og.verify(b,LEAN)
        except Exception as e: report.append((rid,db.name,f'SKIP verify failed: {e}')); continue
        if v.get('python_recomputation')!='PASSED': report.append((rid,db.name,'SKIP verify not passed')); continue
        src,_,_=leancert.generate(b); sl=leancert.check(src,LEAN) if LEAN else {'lean_status':'NOT_RUN'}
        if sl['lean_status']!='STUDY_KERNEL_CHECKED': report.append((rid,db.name,'SKIP per-study Lean failed')); continue
        sl['lean_source']=src
        payload={'schema':'orb-genesis-bridge/1','study_hash':h,'run_id':rid,'title':run['input']['title'],'source':run['input']['source'],
          'freeze_hash':run['freeze_hash'],'input_hash':run['input_hash'],'selected':next((c['expression'] for c in run['candidates'] if c['id']==run['selected_id']),None),
          'results':{'status':st,'selected_result':ev['selected_result'],'labels_hash':ev['labels_hash']},
          'baseline_comparison':{'baseline_advantage':ev['baseline_advantage'],'baselines':[{'name':x['name'],**x['metrics']} for x in ev['baselines']]},
          'verification':v,'study_lean':sl,'lean_scope_note':NOTE,'admission':'PROPOSED','study':run['input']}
        f=OUT/f'{h[:16]}.json'; f.write_text(json.dumps(payload,indent=1))
        ledger[h]={'run_id':rid,'outbox':f.name,'queued_at':time.time(),'attached':None}
        report.append((rid,db.name,f'QUEUED {f.name}'))
LEDGER.write_text(json.dumps(ledger,indent=1))
for r in report: print(*r,sep=' | ')
