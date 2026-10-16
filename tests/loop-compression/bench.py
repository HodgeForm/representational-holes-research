import random, signal, time, tracemalloc, json, sys, statistics
from fractions import Fraction
SEED=20261016; N_TASKS=160; BUDGET=2.0
class TO(Exception): pass
def _alarm(*a): raise TO()
signal.signal(signal.SIGALRM,_alarm)
OOR={'sq','mod','pw','data'}
# ---------- generator ----------
def gen(rng):
    e=rng.randint(3,18); n=10**e; A=[-1,0,1] if e>=5 else [-2,-1,0,1,2]
    oor=rng.random()<0.3
    def body(depth):
        ops=[]
        for _ in range(rng.randint(1,3)):
            k=rng.random()
            if depth<2 and k<0.25: ops.append(('loop',rng.randint(2,5),body(depth+1)))
            elif k<0.6: ops.append(('aff',rng.choice(A),rng.randint(-9,9)))
            else: ops.append(('cost',rng.randint(-5,5),rng.randint(-5,5),rng.randint(-5,5)))
        return ops
    b=body(0)
    if oor:
        t=rng.choice(['sq','mod','pw','data'])
        op={'sq':('sq',),'mod':('mod',rng.randint(5,97)),'pw':('pw',rng.randint(0,50),rng.randint(1,9)),
            'data':('data',tuple(rng.randint(-5,5) for _ in range(rng.randint(2,4))))}[t]
        b.insert(rng.randint(0,len(b)),op)
    return {'x0':rng.randint(-9,9),'n':n,'body':b,'oor':oor}
def has_oor(b): return any(o[0] in OOR or (o[0]=='loop' and has_oor(o[2])) for o in b)
# ---------- M: tuple composition ----------
def comp(f,g):
    a,b,r,s,t=f; c,d,u,v,w=g
    return (c*a,c*b+d,r+u*a*a,s+2*u*a*b+v*a,t+u*b*b+v*b+w)
def tpow(f,n):
    R=(1,0,0,0,0)
    while n:
        if n&1: R=comp(R,f)
        f=comp(f,f); n>>=1
    return R
def summ(b):
    S=(1,0,0,0,0)
    for o in b:
        if o[0]=='aff': S=comp(S,(o[1],o[2],0,0,0))
        elif o[0]=='cost': S=comp(S,(1,0,o[1],o[2],o[3]))
        elif o[0]=='loop': S=comp(S,tpow(summ(o[2]),o[1]))
        else: return None
    return S
def M(p):
    S=summ(p['body'])
    if S is None: return None
    a,b,r,s,t=tpow(S,p['n']); x=p['x0']; return (a*x+b, r*x*x+s*x+t)
# ---------- B1: simulation ----------
def run_body(b,x,C,i):
    for o in b:
        k=o[0]
        if k=='aff': x=o[1]*x+o[2]
        elif k=='cost': C+=o[1]*x*x+o[2]*x+o[3]
        elif k=='loop':
            for j in range(o[1]): x,C=run_body(o[2],x,C,j)
        elif k=='sq': x=x*x+1
        elif k=='mod': x%=o[1]
        elif k=='pw': x=x-o[2] if x>o[1] else 2*x
        elif k=='data': x+=o[1][i%len(o[1])]
    return x,C
def B1(p):
    x,C=p['x0'],0
    for i in range(p['n']): x,C=run_body(p['body'],x,C,i)
    return (x,C)
# ---------- B2: 4x4 matrix power, state [x^2,x,1,C] ----------
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
I4=[[int(i==j) for j in range(4)] for i in range(4)]
def mpow(A,n):
    R=I4
    while n:
        if n&1: R=mm(A,R)
        A=mm(A,A); n>>=1
    return R
def mat(b):
    T=I4
    for o in b:
        if o[0]=='aff':
            a,c=o[1],o[2]; Mx=[[a*a,2*a*c,c*c,0],[0,a,c,0],[0,0,1,0],[0,0,0,1]]
        elif o[0]=='cost': Mx=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[o[1],o[2],o[3],1]]
        elif o[0]=='loop':
            Mx=mat(o[2])
            if Mx is None: return None
            Mx=mpow(Mx,o[1])
        else: return None
        T=mm(Mx,T)
    return T
def B2(p):
    T=mat(p['body'])
    if T is None: return None
    T=mpow(T,p['n']); x=p['x0']; v=[x*x,x,1,0]
    r=[sum(T[i][j]*v[j] for j in range(4)) for i in range(4)]; return (r[1],r[3])
# ---------- B3: sympy rsolve + summation ----------
import sympy as sp
X,K=sp.symbols('X k',integer=True)
def sym_body(b,xe,ce):
    for o in b:
        if o[0]=='aff': xe=sp.expand(o[1]*xe+o[2])
        elif o[0]=='cost': ce=sp.expand(ce+o[1]*xe**2+o[2]*xe+o[3])
        elif o[0]=='loop':
            r=sym_loop(o[2],o[1],xe)
            if r is None: return None
            xe,cc=r; ce=sp.expand(ce+cc)
        else: return None
    return xe,ce
def sym_loop(b,n,xin):
    r=sym_body(b,X,sp.Integer(0))
    if r is None: return None
    fx,fc=r; P=sp.Poly(fx,X)
    if P.degree()>1: return None
    A=P.coeff_monomial(X); Bc=P.coeff_monomial(1)
    y=sp.Function('y')
    sol=sp.rsolve(y(K+1)-A*y(K)-Bc,y(K),{y(0):X})
    if sol is None: return None
    tot=sp.summation(fc.subs(X,sol),(K,0,n-1))
    xn=sol.subs(K,n)
    return sp.expand(xn.subs(X,xin)),sp.expand(tot.subs(X,xin))
def B3(p):
    r=sym_loop(p['body'],p['n'],sp.Integer(p['x0']))
    if r is None: return None
    a,b=sp.nsimplify(r[0]),sp.nsimplify(r[1])
    if not (a.is_Integer and b.is_Integer): return None
    return (int(a),int(b))
# ---------- B4: fake control ----------
def B4(p):
    m=min(p['n'],1000); x,C=p['x0'],0; h=[]
    for i in range(m): x,C=run_body(p['body'],x,C,i); h.append((x,C)) 
    if m==p['n'] or m<2: return (x,C)
    dx=h[-1][0]-h[-2][0]; dc=h[-1][1]-h[-2][1]; k=p['n']-m
    return (x+dx*k, C+dc*k)
METHODS={'M_summary':M,'B1_sim':B1,'B2_matrix':B2,'B3_sympy':B3,'B4_fake':B4}
def timed(f,p,budget=BUDGET):
    tracemalloc.start(); t=time.perf_counter(); signal.setitimer(signal.ITIMER_REAL,budget)
    try: out,st=f(p),'ok'
    except TO: out,st=None,'timeout'
    except Exception as e: out,st=None,'error'
    finally: signal.setitimer(signal.ITIMER_REAL,0)
    dt=time.perf_counter()-t; peak=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    return out,st,dt,peak
