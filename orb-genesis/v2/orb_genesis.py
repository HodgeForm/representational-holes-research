#!/usr/bin/env python3
"""ORB Genesis 0.3: bounded discovery, SQLite memory, Lean verification, stdio MCP.
Standard library only. Arbitrary Lean/code execution is deliberately not an API.
"""
import argparse, collections, hashlib, itertools, json, os, pathlib, shutil, sqlite3, subprocess, sys, tempfile, time, uuid
VERSION = '0.3.0'
LEAN_VERSION = '4.19.0'
PROOF = '''-- Generated finite collision certificate; encoding must be verified against the data.
theorem obstruction : ¬ ∃ f : Nat → Nat, f 0 = 0 ∧ f 0 = 1 := by
  intro ⟨f, ha, hb⟩
  have impossible : (0 : Nat) = 1 := ha.symm.trans hb
  cases impossible
#print axioms obstruction
'''
def canonical(x):
    def normalize(v):
        if type(v) is float and v.is_integer(): return int(v)
        if isinstance(v,dict): return {k:normalize(w) for k,w in v.items()}
        if isinstance(v,list): return [normalize(w) for w in v]
        return v
    return json.dumps(normalize(x), sort_keys=True, separators=(',', ':'), ensure_ascii=False)
def digest(x):
    return hashlib.sha256((x if isinstance(x, str) else canonical(x)).encode()).hexdigest()
def value(v):
    return type(v) is bool or (type(v) is str and len(v) <= 80) or (type(v) is int and abs(v) <= 1000000)
def expression(e, o):
    a = o[e['a']]
    if e['op'] == 'field': return a
    b = o[e['b']]
    if e['op'] == 'eq': return canonical(a) == canonical(b)
    if e['op'] == 'xor': return bool(a) != bool(b)
    if e['op'] == 'difference': return a-b
    if e['op'] == 'sum': return a+b
    raise ValueError('Unknown expression')
def key(model, row):
    return canonical([expression(e, row['observables']) for e in model])
def groups(rows, model):
    out = collections.defaultdict(list)
    for row in rows: out[key(model, row)].append(row)
    return out
def collisions(rows, model):
    pairs = [(a['id'], b['id']) for group in groups(rows, model).values() for a,b in itertools.combinations(group,2) if canonical(a['outcome']) != canonical(b['outcome'])]
    return {'count':len(pairs), 'witnesses':[list(p) for p in pairs[:16]]}
def fit(rows, model):
    table, repeated = {}, 0
    for k, group in groups(rows, model).items():
        if len({canonical(r['outcome']) for r in group}) == 1:
            table[k] = group[0]['outcome']
            if len(group) >= 2: repeated += len(group)
    return table, repeated / len(rows)
def predict(table, model, rows):
    return [{'id':r['id'], 'covered':key(model,r) in table, 'prediction':table.get(key(model,r))} for r in rows]
def validate(a):
    import re
    if not isinstance(a.get('title'),str) or not a['title'].strip() or len(a['title'])>160: raise ValueError('Invalid title')
    if not isinstance(a.get('source'),str) or not a['source'].strip() or len(a['source'])>1000: raise ValueError('Invalid source')
    fields=a['fields']; language=a['language']
    if not isinstance(fields,list) or not 1<=len(fields)<=6 or any(not isinstance(f,str) or not re.fullmatch('[a-z][a-z0-9_]{0,31}',f) or f in ['id','outcome','target','label'] for f in fields) or len(set(fields))!=len(fields): raise ValueError('Invalid fields')
    if not isinstance(language,list) or len(set(language))!=len(language) or any(f not in fields for f in language): raise ValueError('Invalid language')
    cleaned={}
    for split,labelled in [('training',True),('validation_inputs',False)]:
        rows=a[split]
        if not isinstance(rows,list) or not 2<=len(rows)<=128: raise ValueError('Use 2–128 rows in each split')
        ids=set(); clean=[]
        for r in rows:
            if not isinstance(r.get('id'),str) or not r['id'].strip() or len(r['id'])>80 or r['id'] in ids: raise ValueError('Invalid/duplicate ID')
            ids.add(r['id'])
            if set(r['observables'])!=set(fields) or not all(value(v) for v in r['observables'].values()): raise ValueError('Invalid observables')
            if labelled and not value(r.get('outcome')): raise ValueError('Invalid outcome')
            if not labelled and 'outcome' in r: raise ValueError('Validation outcomes must remain separate until predictions freeze')
            clean.append({'id':r['id'],'observables':r['observables'],**({'outcome':r['outcome']} if labelled else {})})
        cleaned[split]=clean
    seen={canonical(r['observables']) for r in cleaned['training']}; ids={r['id'] for r in cleaned['training']}
    if any(canonical(r['observables']) in seen or r['id'] in ids for r in cleaned['validation_inputs']): raise ValueError('Training/validation overlap')
    costs={f:a.get('costs',{}).get(f,1) for f in fields}
    if any(type(c) is not int or not 0<c<=100 for c in costs.values()): raise ValueError('Invalid costs')
    return {'title':a['title'],'source':a['source'],'fields':fields,'language':language,**cleaned,'costs':costs}
def generate(inp):
    remaining=[f for f in inp['fields'] if f not in inp['language']]
    expressions=[{'op':'field','a':f} for f in remaining]; rows=inp['training']+inp['validation_inputs']
    for a,b in itertools.combinations(remaining,2):
        expressions.append({'op':'eq','a':a,'b':b})
        if all(type(r['observables'][f]) is bool or (type(r['observables'][f]) is int and r['observables'][f] in (0,1)) for r in rows for f in (a,b)): expressions.append({'op':'xor','a':a,'b':b})
        if all(type(r['observables'][f]) is int for r in rows for f in (a,b)):
            expressions.extend([{'op':op,'a':a,'b':b} for op in ('difference','sum')])
    candidates=[]
    for i,e in enumerate(expressions):
        model=[{'op':'field','a':f} for f in inp['language']]+[e]; c=collisions(inp['training'],model); table,repeated=fit(inp['training'],model)
        candidates.append({'id':'candidate-'+str(i),'expression':e,'model':model,'cost':inp['costs'][e['a']]+(inp['costs'][e['b']] if 'b' in e else 0),'complexity':2 if 'b' in e else 1,'training_conflicts':c['count'],'training_witnesses':c['witnesses'],'repeated_fraction':repeated,'predictions':predict(table,model,inp['validation_inputs'])})
    return sorted(candidates,key=lambda c:(c['training_conflicts'],-c['repeated_fraction'],c['cost'],c['complexity'],c['id']))
def freeze(args):
    inp=validate(args); base=[{'op':'field','a':f} for f in inp['language']]; candidates=generate(inp)
    selected=next((c['id'] for c in candidates if c['training_conflicts']==0 and c['repeated_fraction']>=.5),None) if collisions(inp['training'],base)['count'] else None
    baseline_models=[('current_language',base)]+[('single_field:'+f,base+[{'op':'field','a':f}]) for f in inp['fields'] if f not in inp['language']]+[('all_fields',[{'op':'field','a':f} for f in inp['fields']])]
    baselines=[]
    for name,model in baseline_models:
        table,_=fit(inp['training'],model);baselines.append({'name':name,'model':model,'training_conflicts':collisions(inp['training'],model)['count'],'predictions':predict(table,model,inp['validation_inputs'])})
    run={'id':str(uuid.uuid4()),'created_at':time.time(),'engine':VERSION,'input':inp,'input_hash':digest(inp),'collisions':collisions(inp['training'],base),'candidates':candidates,'selected_id':selected,'baselines':baselines,'evaluation':None,'admission':'PROPOSED'}
    run['freeze_hash']=digest({k:run[k] for k in ('input_hash','candidates','selected_id','baselines')})
    return run
def metrics(predictions, labels):
    correct=wrong=abstained=0; counter=[]
    for p in predictions:
        if not p['covered']: abstained+=1
        elif canonical(p['prediction'])==canonical(labels[p['id']]): correct+=1
        else: wrong+=1;counter.append({'id':p['id'],'predicted':p['prediction'],'observed':labels[p['id']]})
    n=len(predictions)
    return {'metrics':{'correct':correct,'wrong':wrong,'abstained':abstained,'total':n,'coverage':(correct+wrong)/n,'accuracy_all':correct/n},'counterexamples':counter}
def score(run, labels):
    if run.get('evaluation'): raise ValueError('One-shot validation already completed')
    expected={r['id'] for r in run['input']['validation_inputs']}
    if len(labels)!=len(expected) or {r['id'] for r in labels}!=expected or not all(value(r['outcome']) for r in labels): raise ValueError('Labels must match frozen inputs exactly')
    truth={r['id']:r['outcome'] for r in labels}
    candidates=[{'id':c['id'],**metrics(c['predictions'],truth)} for c in run['candidates']]
    baselines=[{'name':b['name'],**metrics(b['predictions'],truth)} for b in run['baselines']]
    selected=next((c for c in candidates if c['id']==run['selected_id']),None)
    status='ABSTAIN' if selected is None else 'REFUTED' if selected['metrics']['wrong'] else 'INCONCLUSIVE' if selected['metrics']['abstained'] else 'HELDOUT_SUPPORTED'
    return {'status':status,'labels':labels,'labels_hash':digest(labels),'freeze_hash':run['freeze_hash'],'candidates':candidates,'baselines':baselines,'selected_result':selected,'baseline_advantage':selected['metrics']['accuracy_all']-max(b['metrics']['accuracy_all'] for b in baselines) if selected else None}
def bundle(run):
    cert=None
    if run['collisions']['witnesses']:
        ids=run['collisions']['witnesses'][0];a,b=[next(r for r in run['input']['training'] if r['id']==x) for x in ids]
        cert={'witness_ids':ids,'encoding':{'representation':key([{'op':'field','a':f} for f in run['input']['language']],a),'outcome_zero':a['outcome'],'outcome_one':b['outcome']},'theorem':'obstruction','source':PROOF,'source_hash':digest(PROOF),'status':'SOURCE_ONLY_UNCHECKED'}
    return {'schema':'orb-genesis-bundle/1','run':run,'certificate':cert}
def verify(data, lean=None):
    if data.get('schema')!='orb-genesis-bundle/1': raise ValueError('Unsupported bundle')
    r=data['run']; regenerated=freeze(r['input'])
    for field in ['collisions','candidates','selected_id','baselines']:
        if canonical(r[field])!=canonical(regenerated[field]): raise ValueError('Recomputation mismatch: '+field)
    if r['input_hash'] != digest(r['input']): raise ValueError('Input hash mismatch')
    if r['freeze_hash'] != digest({k:r[k] for k in ('input_hash','candidates','selected_id','baselines')}): raise ValueError('Freeze hash mismatch')
    if r.get('evaluation'):
        recomputed=score({**r,'evaluation':None},r['evaluation']['labels'])
        for field in ['status','candidates','baselines','selected_result','baseline_advantage']:
            if canonical(r['evaluation'][field])!=canonical(recomputed[field]): raise ValueError('Evaluation mismatch: '+field)
    expected=bundle(r)['certificate']; cert=data.get('certificate')
    if canonical(cert)!=canonical(expected): raise ValueError('Certificate/data encoding mismatch')
    result={'schema':'orb-genesis-verification/1','bundle_hash':digest(data),'verifier_version':VERSION,'python_recomputation':'PASSED','lean_status':'NOT_RUN','scope':'Exact finite collision obstruction only. Does not prove measurement validity, useful representation, causality, novelty, or a general discovery ability.'}
    if cert and lean:
        compiler=pathlib.Path(lean).resolve()
        version=subprocess.run([str(compiler),'--version'],capture_output=True,text=True,timeout=15)
        if version.returncode or ('version '+LEAN_VERSION+',') not in version.stdout: raise ValueError('Use pinned Lean '+LEAN_VERSION+'; actual: '+version.stdout+version.stderr)
        with tempfile.TemporaryDirectory(prefix='orb-proof-') as directory:
            path=pathlib.Path(directory)/'Obstruction.lean';path.write_text(PROOF,encoding='utf-8')
            checked=subprocess.run([str(compiler),str(path)],cwd=directory,capture_output=True,text=True,timeout=30)
        audit=checked.stdout+checked.stderr
        if checked.returncode or "'obstruction' does not depend on any axioms" not in audit or 'warning:' in audit or 'sorry' in audit: raise ValueError('Lean verification failed: '+audit)
        result.update(lean_status='KERNEL_CHECKED',lean_version=version.stdout.strip(),compiler_sha256=hashlib.sha256(compiler.read_bytes()).hexdigest(),source_hash=digest(PROOF),axioms=[],output=audit.strip())
        preload=os.environ.get('LD_PRELOAD')
        if preload: result['runtime_compatibility_shim']={'path':preload,'sha256':hashlib.sha256(pathlib.Path(preload).read_bytes()).hexdigest()}
    return result
class Store:
    def __init__(self,path):
        pathlib.Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path);self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, body TEXT NOT NULL)');self.db.execute('CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY, body TEXT NOT NULL, hash TEXT NOT NULL)')
    def event(self,kind,payload):
        row=self.db.execute('SELECT hash FROM events ORDER BY seq DESC LIMIT 1').fetchone();e={'at':time.time(),'kind':kind,'previous':row[0] if row else None,'payload':payload};self.db.execute('INSERT INTO events(body,hash) VALUES (?,?)',(canonical(e),digest(e)))
    def add(self,args):
        r=freeze(args)
        r['related_refuters']=[]
        for (body,) in self.db.execute('SELECT body FROM runs'):
            old=json.loads(body)
            if old['input']['source']==r['input']['source'] and old.get('evaluation'):
                for c in old['evaluation']['candidates']:
                    if c['metrics']['wrong']:
                        r['related_refuters'].append({'run_id':old['id'],'expression':next(x['expression'] for x in old['candidates'] if x['id']==c['id']),'witnesses':c['counterexamples']})
        r['related_refuters']=r['related_refuters'][-16:]
        with self.db:self.db.execute('INSERT INTO runs VALUES (?,?)',(r['id'],canonical(r)));self.event('freeze',{'run_id':r['id'],'freeze_hash':r['freeze_hash']})
        return bundle(r)
    def get(self,id):
        row=self.db.execute('SELECT body FROM runs WHERE id=?',(id,)).fetchone()
        if not row: raise ValueError('Unknown run')
        return json.loads(row[0])
    def score(self,id,labels):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE');r=self.get(id);r['evaluation']=score(r,labels);self.db.execute('UPDATE runs SET body=? WHERE id=?',(canonical(r),id));self.event('score',{'run_id':id,'evaluation_hash':digest(r['evaluation'])})
        return bundle(r)
    def history(self):
        return [{'id':id,'title':(r:=json.loads(body))['input']['title'],'status':(r.get('evaluation') or {}).get('status','PREDICTIONS_FROZEN'),'admission':r['admission']} for id,body in self.db.execute('SELECT id,body FROM runs')]
def serve(store,lean):
    tools=[{'name':'genesis_discover','description':'Generate bounded representations and freeze predictions before validation labels. No admission.','inputSchema':{'type':'object','required':['request'],'properties':{'request':{'type':'object'}}}}, {'name':'genesis_validate','description':'Score one frozen local run once, using measured or explicitly synthetic labels.','inputSchema':{'type':'object','required':['run_id','labels'],'properties':{'run_id':{'type':'string'},'labels':{'type':'array','items':{'type':'object'}}}}}, {'name':'genesis_verify_bundle','description':'Recompute a discovery bundle in Python and check generated finite obstruction proof with pinned Lean when configured. No arbitrary source executes.','inputSchema':{'type':'object','required':['bundle'],'properties':{'bundle':{'type':'object'}}}}, {'name':'genesis_local_history','description':'Read local SQLite run history.','inputSchema':{'type':'object','properties':{}}}]
    for line in sys.stdin:
        id=None
        try:
            if len(line)>2000000: raise ValueError('Request exceeds 2 MB')
            msg=json.loads(line);id=msg.get('id');method=msg['method']
            if method.startswith('notifications/'): continue
            if method=='initialize': result={'protocolVersion':'2024-11-05','capabilities':{'tools':{}},'serverInfo':{'name':'orb-genesis-local','version':VERSION}}
            elif method=='tools/list': result={'tools':tools}
            elif method=='ping': result={}
            elif method=='tools/call':
                p=msg['params'];a=p.get('arguments',{});name=p['name']
                if name=='genesis_discover': data=store.add(a['request'])
                elif name=='genesis_validate': data=store.score(a['run_id'],a['labels'])
                elif name=='genesis_verify_bundle': data=verify(a['bundle'],lean)
                elif name=='genesis_local_history': data=store.history()
                else: raise ValueError('Unknown tool')
                result={'content':[{'type':'text','text':json.dumps(data,ensure_ascii=False)}],'isError':False}
            else: raise ValueError('Unknown method')
            response={'jsonrpc':'2.0','id':id,'result':result}
        except Exception as exc: response={'jsonrpc':'2.0','id':id,'error':{'code':-32603,'message':str(exc)}}
        print(json.dumps(response,ensure_ascii=False),flush=True)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',default=str(pathlib.Path.home()/'.orb-genesis'/'research.db'));p.add_argument('--lean',default=os.environ.get('ORB_LEAN') or shutil.which('lean'));sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('mcp');sub.add_parser('history');d=sub.add_parser('discover');d.add_argument('request');v=sub.add_parser('validate');v.add_argument('run_id');v.add_argument('labels');c=sub.add_parser('verify');c.add_argument('bundle');
    a=p.parse_args();store=Store(a.db)
    if a.cmd=='mcp': serve(store,a.lean);return
    if a.cmd=='discover': result=store.add(json.loads(pathlib.Path(a.request).read_text(encoding='utf-8')))
    elif a.cmd=='validate': result=store.score(a.run_id,json.loads(pathlib.Path(a.labels).read_text(encoding='utf-8')))
    elif a.cmd=='verify': result=verify(json.loads(pathlib.Path(a.bundle).read_text(encoding='utf-8')),a.lean)
    else: result=store.history()
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':
    try: main()
    except Exception as e: print(json.dumps({'error':str(e)}),file=sys.stderr);sys.exit(1)
