import json, numpy as np

def step(states,rule):
    l=np.roll(states,1,axis=1); c=states; r=np.roll(states,-1,axis=1)
    idx=(l<<2)|(c<<1)|r
    return ((rule>>idx)&1).astype(np.uint8)

def gen_states(N,n,seed):
    rng=np.random.default_rng(seed)
    ps=rng.uniform(.12,.88,size=n)
    return np.vstack([(rng.random(N)<p).astype(np.uint8) for p in ps])

def program(states,rule,h,mask):
    s=states.copy()
    for _ in range(h):
        s=step(s,rule)
    codes=(np.roll(s,1,axis=1)<<2)|(s<<1)|np.roll(s,-1,axis=1)
    keep=np.zeros_like(codes,dtype=bool)
    for k in range(8):
        if (mask>>k)&1: keep |= (codes==k)
    return keep.sum(axis=1)

plan=json.load(open("exp012_frozen_plan.json"))
hidden={"T01":56,"T03":202,"T04":158,"T05":3,"T06":78}
for j,tid in enumerate(["T01","T03","T04","T05","T06"]):
    t=plan["trials"][tid]
    N=plan["prospective"]["sizes"][tid]
    states=gen_states(N,256,plan["prospective"]["state_seed_base"]+j)
    p=t["synthesized_program"]
    y=program(states,hidden[tid],p["horizon"],p["mask"])
    exact=[]
    for rule in t["survivor_rules"]:
        if np.array_equal(program(states,rule,p["horizon"],p["mask"]),y):
            exact.append(rule)
    print(tid,exact)

c=json.load(open("exp012c_frozen_plan.json"))
states=gen_states(c["prospective"]["N"],c["prospective"]["states"],c["prospective"]["state_seed"])
def even_active(states,rule):
    return step(states,rule)[:,::2].sum(axis=1)
y=even_active(states,3)
print("012C Rule3 mismatches",np.sum(even_active(states,3)!=y))
print("012C Rule17 mismatches",np.sum(even_active(states,17)!=y))
