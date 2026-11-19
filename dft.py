"""Data-flow testing of reminder_level(): DU pairs inferred from executed-line traces."""
import sys, json, inspect
import jobtracker as jt

def trace_lines(fn,*args):
    seq=[]; code=fn.__code__
    def tr(frame,ev,arg):
        if frame.f_code is code:
            if ev=='line': seq.append(frame.f_lineno)
            return tr
    sys.settrace(tr)
    try: r=fn(*args)
    except Exception as e: r=type(e).__name__
    finally: sys.settrace(None)
    return seq,r

src,start=inspect.getsourcelines(jt.reminder_level)
L={}
for i,s in enumerate(src):
    n=start+i; t=s.strip()
    if t.startswith('if status in'): L['A']=n
    elif t.startswith('if days_left < 0'): L['B']=n
    elif t.startswith('elif days_left <= 3'): L['C']=n
    elif t=='level = "Overdue"': L['L1']=n
    elif t=='level = "Urgent"': L['L2']=n
    elif t=='level = "Normal"': L['L3']=n
    elif t=='return level': L['R']=n
    elif t=='return "Closed"': L['K']=n
PAIRS=['status->A:T','status->A:F','days->B:T','days->B:F','days->C:T','days->C:F','L1->return','L2->return','L3->return']
DEFS={'status':['status->A:T','status->A:F'],'days_left':['days->B:T','days->B:F','days->C:T','days->C:F'],
      'L1':['L1->return'],'L2':['L2->return'],'L3':['L3->return']}
def pairs(seq):
    p=set()
    def nxt(k):
        i=seq.index(L[k]); return seq[i+1] if i+1<len(seq) else None
    if L['A'] in seq: p.add('status->A:T' if nxt('A')==L['K'] else 'status->A:F')
    if L['B'] in seq: p.add('days->B:T' if nxt('B')==L['L1'] else 'days->B:F')
    if L['C'] in seq: p.add('days->C:T' if nxt('C')==L['L2'] else 'days->C:F')
    for k in ('L1','L2','L3'):
        if L[k] in seq and L['R'] in seq: p.add(k+'->return')
    return p
tests=[('TC-1',(5,'Rejected')),('TC-2',(-1,'Applied')),('TC-3',(2,'Applied')),('TC-4',(10,'Saved'))]
cov=set(); out=[]
for n,a in tests:
    s,r=trace_lines(jt.reminder_level,*a); cov|=pairs(s)
    d=sum(1 for v in DEFS.values() if any(x in cov for x in v))
    out.append((n,a,r,round(d/5*100,1),round(len(cov)/9*100,1)))
    print(n,a,r,'All-Defs %.1f%%'%(d/5*100),'All-Uses %.1f%% (%d/9)'%(len(cov)/9*100,len(cov)))
# faulty function: statement coverage vs data-flow
fl=jt.reminder_level_faulty.__code__
body=set(l for _,_,l in fl.co_lines() if l)
hit=set()
for a in [(5,'Rejected'),(-1,'Applied'),(2,'Applied'),(10,'Saved')]:
    seq=[];
    def tr(f,e,g):
        if f.f_code is fl:
            if e=='line': seq.append(f.f_lineno)
            return tr
    sys.settrace(tr)
    try: jt.reminder_level_faulty(*a)
    finally: sys.settrace(None)
    hit|=set(seq)
print('faulty: statement coverage by TC-1..4 (excl. def line):',len(hit),'of',len(body)-1)
print('faulty(3,Saved):',trace_lines(jt.reminder_level_faulty,3,'Saved')[1])
print('correct(3,Saved):',jt.reminder_level(3,'Saved'))
json.dump(out,open('dft.json','w'))
