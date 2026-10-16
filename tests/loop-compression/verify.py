# Independent ground truth. Shares no code with bench.py methods.
import signal,time
from fractions import Fraction
class Late(Exception): pass
def _h(*a): raise Late()
def step(ops,state,ctr):
    xv,cv=state
    for op in ops:
        tag=op[0]
        if tag=='aff': xv=xv*op[1]+op[2]
        elif tag=='cost': cv=cv+op[3]+op[2]*xv+op[1]*xv*xv
        elif tag=='loop':
            st=(xv,cv)
            for jj in range(op[1]): st=step(op[2],st,jj)
            xv,cv=st
        elif tag=='sq': xv=xv*xv+1
        elif tag=='mod': xv=xv%op[1]
        elif tag=='pw': xv=(xv-op[2]) if xv>op[1] else xv+xv
        elif tag=='data': xv=xv+op[1][ctr%len(op[1])]
    return xv,cv
def simulate(prog,N):
    st=(prog['x0'],0)
    for c in range(N): st=step(prog['body'],st,c)
    return st
def lagrange(pts,N):
    tot=Fraction(0)
    for i,(xi,yi) in enumerate(pts):
        term=Fraction(yi)
        for j,(xj,_) in enumerate(pts):
            if j!=i: term*=Fraction(N-xj,xi-xj)
        tot+=term
    assert tot.denominator==1; return int(tot)
def truth(prog,cap=5.0):
    """returns (answer or None, how)"""
    signal.signal(signal.SIGALRM,_h); signal.setitimer(signal.ITIMER_REAL,cap)
    try:
        if prog['n']<=10**5: 
            r=simulate(prog,prog['n']); return r,'simulation'
    except Late: pass
    finally: signal.setitimer(signal.ITIMER_REAL,0)
    if prog['oor']: return None,'none'
    par=prog['n']%2
    ns=[par+2*k for k in range(1,11)]
    vals={m:simulate(prog,m) for m in ns}
    for idx in (0,1):
        fit=[(m,vals[m][idx]) for m in ns[:8]]
        for m in ns[8:]:
            assert lagrange(fit,m)==vals[m][idx], 'poly check failed'
    return (lagrange([(m,vals[m][0]) for m in ns[:8]],prog['n']),
            lagrange([(m,vals[m][1]) for m in ns[:8]],prog['n'])),'interpolation'
