"""Per-study Lean certificate: encodes the actual rows and proves the study's specific claims."""
import json, hashlib, subprocess, tempfile, pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).parent)); import orb_genesis as og
def lv(v):
    if type(v) is bool: return f"V.b {'true' if v else 'false'}"
    if type(v) is int: return f"V.i ({v})"
    return "V.s "+json.dumps(v)
def lrow(r,out): return "{ id := %s, obs := [%s], out := %s }"%(json.dumps(r['id']),", ".join(f"({json.dumps(k)}, {lv(v)})" for k,v in sorted(r['observables'].items())),json.dumps(out))
def le(e):
    if e['op']=='field': return f"E.field {json.dumps(e['a'])}"
    return f"E.{ {'eq':'eq','xor':'xor','sum':'sum','difference':'diff'}[e['op']] } {json.dumps(e['a'])} {json.dumps(e['b'])}"
HDR='''set_option maxRecDepth 200000
set_option maxHeartbeats 0
inductive V | i (n : Int) | s (x : String) | b (x : Bool) deriving DecidableEq
structure Row where
  id : String
  obs : List (String × V)
  out : String
deriving DecidableEq
inductive E | field (a : String) | eq (a b : String) | xor (a b : String) | sum (a b : String) | diff (a b : String)
def get (r : Row) (f : String) : V := (r.obs.lookup f).getD (V.s "")
def truthy : V → Bool | V.i n => n != 0 | V.b x => x | V.s x => x != ""
def ev (r : Row) : E → V
  | E.field a => get r a
  | E.eq a b => V.b (decide (get r a = get r b))
  | E.xor a b => V.b (truthy (get r a) != truthy (get r b))
  | E.sum a b => match get r a, get r b with | V.i x, V.i y => V.i (x+y) | _, _ => V.s "type-error"
  | E.diff a b => match get r a, get r b with | V.i x, V.i y => V.i (x-y) | _, _ => V.s "type-error"
def key (m : List E) (r : Row) : List V := m.map (ev r)
def predict (train : List Row) (m : List E) (r : Row) : Option String :=
  match train.filter (fun t => decide (key m t = key m r)) with
  | [] => none
  | h :: rest => if rest.all (fun t => decide (t.out = h.out)) then some h.out else none
'''
def generate(b, status_override=None, rule_override=None):
    run=b['run']; inp=run['input']; ev=run['evaluation']; h=og.digest(b)
    status=status_override or ev['status']
    sel=rule_override or next(c for c in run['candidates'] if c['id']==run['selected_id'])['model']
    lang=[{'op':'field','a':f} for f in inp['language']]
    labels={l['id']:l['outcome'] for l in ev['labels']}
    w=run['collisions']['witnesses'][0]; tr={r['id']:r for r in inp['training']}
    L=[HDR, f'def studyHash : String := "{h}"', f'def claimedStatus : String := "{status}"',
       "def train : List Row := [\n  "+",\n  ".join(lrow(r,r['outcome']) for r in inp['training'])+"]",
       "def val : List Row := [\n  "+",\n  ".join(lrow(r,labels[r['id']]) for r in inp['validation_inputs'])+"]",
       "def lang : List E := ["+", ".join(le(e) for e in lang)+"]",
       "def rule : List E := ["+", ".join(le(e) for e in sel)+"]",
       f"def r1 : Row := {lrow(tr[w[0]],tr[w[0]]['outcome'])}", f"def r2 : Row := {lrow(tr[w[1]],tr[w[1]]['outcome'])}",
       "theorem r1_in : r1 ∈ train := by decide", "theorem r2_in : r2 ∈ train := by decide",
       "theorem conflict : key lang r1 = key lang r2 ∧ r1.out ≠ r2.out := by decide",
       "theorem obstruction : ¬ ∃ f : List V → String, f (key lang r1) = r1.out ∧ f (key lang r2) = r2.out := by\n  intro ⟨f, h1, h2⟩\n  rw [conflict.1] at h1\n  exact conflict.2 (h1.symm.trans h2)"]
    if status=='HELDOUT_SUPPORTED':
        L.append("theorem heldout_supported : val.all (fun r => decide (predict train rule r = some r.out)) = true := by decide"); thm=['obstruction','heldout_supported']
    elif status=='REFUTED':
        cx=ev['selected_result']['counterexamples'][0]['id']; vr=next(r for r in inp['validation_inputs'] if r['id']==cx)
        L+= [f"def cx : Row := {lrow(vr,labels[cx])}", "theorem cx_in : cx ∈ val := by decide",
             "theorem refuted : (predict train rule cx).isSome = true ∧ predict train rule cx ≠ some cx.out := by decide"]; thm=['obstruction','refuted']
    else: raise ValueError('unsupported status '+status)
    L+= [f"#print axioms {t}" for t in thm]
    return "\n".join(L)+"\n", h, thm
def check(src, lean):
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d)/'Study.lean'; p.write_text(src)
        c=subprocess.run([lean,str(p)],capture_output=True,text=True,timeout=600)
    out=(c.stdout+c.stderr).strip()
    ok=c.returncode==0 and 'sorry' not in out and 'error' not in out
    ax=[l for l in out.splitlines() if 'axiom' in l]
    return {'lean_status':'STUDY_KERNEL_CHECKED' if ok else 'LEAN_FAILED','source_sha256':hashlib.sha256(src.encode()).hexdigest(),
            'axioms_output':ax,'native_decide_used':'native_decide' in src,'output':out[-1500:]}
