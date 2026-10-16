import json
def row(i,a,b,n,c=None,sp="t"):
    o={"site":"lab","a":a,"b":b,"noise":n}
    if c is not None:o["c"]=c
    return {"id":f"{sp}{i}","observables":o}
def lab(a,b): return "on" if a^b else "off"
combos=[(0,0),(0,1),(1,0),(1,1)]
def study(trap=False):
    f=["site","a","b","noise"]+(["c"] if trap else [])
    tr=[];va=[];lb=[]
    i=0
    for n in range(1,5):
        for a,b in combos:
            r=row(i,a,b,n,(a^b) if trap else None,"train-");r["outcome"]=lab(a,b);tr.append(r);i+=1
    for n in (11,12):
        for a,b in combos:
            c=(1-(a^b)) if (trap and n==11) else ((a^b) if trap else None)
            # trap: n=11 rows have c anti-correlated -> c-model wrong on 4/8
            r=row(i,a,b,n,c,"val-");va.append(r);lb.append({"id":r["id"],"outcome":lab(a,b)});i+=1
    req={"title":"Hard XOR"+(" trap" if trap else ""),"source":"synthetic; no measurement","fields":f,"language":["site"],"training":tr,"validation_inputs":va}
    return req,lb
r,l=study();json.dump(r,open("h1-request.json","w"),indent=1);json.dump(l,open("h1-labels.json","w"))
l2=[dict(x) for x in l];
for k in (0,5): l2[k]["outcome"]="off" if l2[k]["outcome"]=="on" else "on"
json.dump(l2,open("h2-labels-flipped.json","w"))
r,l=study(True);json.dump(r,open("h3-request.json","w"),indent=1);json.dump(l,open("h3-labels.json","w"))
