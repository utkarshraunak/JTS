"""Green SE benchmarks: baseline vs optimized (20k applications, 1k lookups, 100k log rows)."""
import time, json, gzip, random, sqlite3, os, heapq
from datetime import date, timedelta
random.seed(7)
N=20000
STAT=["Saved","Applied","Interview","Offer","Accepted","Rejected","Withdrawn"]
base=date(2026,11,19)
apps=[dict(app_id=i,company=f"Company {i%900}",role="Software Engineer",status=random.choice(STAT),
           deadline=(base+timedelta(days=random.randint(-5,60))).isoformat()) for i in range(N)]
def cpu(f,rep=3):
    best=1e9
    for _ in range(rep):
        t=time.process_time(); f(); best=min(best,time.process_time()-t)
    return best
# W1 lookup
ids=[random.randrange(N) for _ in range(1000)]
lst=list(apps); idx={a['app_id']:a for a in apps}
def w1_base():
    for i in ids:
        for a in lst:
            if a['app_id']==i: break
def w1_opt():
    for i in ids: idx[i]
w1b,w1o=cpu(w1_base,1),cpu(w1_opt)
# W2 deadline monitor: 100 polling ticks scanning every record vs event-driven min-heap
due_days=3
def w2_base():
    for _ in range(100):
        [a for a in apps if a['deadline']<=(base+timedelta(days=due_days)).isoformat()]
h=[(a['deadline'],a['app_id']) for a in apps]; heapq.heapify(h)
def w2_opt():
    hh=list(h); lim=(base+timedelta(days=due_days)).isoformat()
    while hh and hh[0][0]<=lim: heapq.heappop(hh)   # work only when an event is due
w2b,w2o=cpu(w2_base,1),cpu(w2_opt)
# W3 data transfer for one dashboard load
full=json.dumps(apps,indent=2).encode()
page=gzip.compress(json.dumps(apps[:50],separators=(',',':')).encode())
w3b,w3o=len(full),len(page)
# W4 storage: 100k log rows
def mk(path,coded):
    if os.path.exists(path): os.remove(path)
    c=sqlite3.connect(path)
    if coded:
        c.execute("create table log(id integer primary key,app_id integer,status integer,day integer)")
        c.executemany("insert into log(app_id,status,day) values(?,?,?)",[(random.randrange(N),random.randrange(7),random.randrange(365)) for _ in range(100000)])
    else:
        c.execute("create table log(id integer primary key,app_id integer,status text,logged_at text)")
        c.executemany("insert into log(app_id,status,logged_at) values(?,?,?)",[(random.randrange(N),random.choice(STAT),(base+timedelta(days=random.randrange(365))).isoformat()+" 10:30:00") for _ in range(100000)])
    c.commit(); c.close(); s=os.path.getsize(path); os.remove(path); return s
w4b,w4o=mk('b.db',0),mk('o.db',1)
# SCI proxy (operational): E = cpu*15W + network 0.06 kWh/GB ; I = 0.71 kgCO2/kWh ; R = 1 dashboard session
I=0.71*1000/1  # gCO2e per kWh
def sci(cpu_s,bytes_):
    kwh=cpu_s*15/3.6e6 + bytes_/1e9*0.06
    return kwh*I
sb=sci(w1b+w2b,w3b); so=sci(w1o+w2o,w3o)
red=lambda b,o:(1-o/b)*100
r=dict(w1=(w1b,w1o,red(w1b,w1o)),w2=(w2b,w2o,red(w2b,w2o)),w3=(w3b,w3o,red(w3b,w3o)),w4=(w4b,w4o,red(w4b,w4o)),sci=(sb,so,red(sb,so)))
for k,v in r.items(): print(k,v)
json.dump(r,open('bench.json','w'))
