import unittest, trace, sys, time, io, json
t0=time.perf_counter()
tr=trace.Trace(count=1,trace=0)
res=unittest.TestResult()
def go():
    import test_jobtracker
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_jobtracker)
    suite.run(res)
tr.runfunc(go)
el=time.perf_counter()-t0
counts=tr.results().counts
import dis
src=open('jobtracker.py').read().splitlines()
code=compile(open('jobtracker.py').read(),'jobtracker.py','exec')
def lines(c,acc):
    for _,_,l in c.co_lines():
        if l: acc.add(l)
    for k in c.co_consts:
        if hasattr(k,'co_code'): lines(k,acc)
    return acc
allx=lines(code,set())
hit={l for (f,l),n in counts.items() if f.endswith('jobtracker.py')}
# exclude the seeded-fault function from the denominator
fs=[i+1 for i,s in enumerate(src) if s.startswith('def reminder_level_faulty')][0]
exe=sorted(l for l in allx if l<fs)
cov=len([l for l in exe if l in hit])/len(exe)*100
print(json.dumps(dict(run=res.testsRun,fail=len(res.failures)+len(res.errors),time=round(el,3),line_cov=round(cov,1),missed=[l for l in exe if l not in hit])))
