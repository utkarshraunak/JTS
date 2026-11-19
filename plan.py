# Function points
EI,EO,EQ,ILF,EIF=8,5,4,5,1
w=dict(EI=4,EO=5,EQ=4,ILF=10,EIF=7)
ufp=EI*w['EI']+EO*w['EO']+EQ*w['EQ']+ILF*w['ILF']+EIF*w['EIF']
gsc=[4,3,3,2,3,4,3,2,2,2,2,3,2,3]   # 14 general system characteristics (0-5)
tdi=sum(gsc); vaf=0.65+0.01*tdi; afp=ufp*vaf
pm=afp/10   # productivity 10 FP / person-month
print('UFP',ufp,'TDI',tdi,'VAF',round(vaf,2),'AFP',round(afp,2),'PM',round(pm,1),'months(3 eng)',round(pm/3,2),'weeks',round(pm/3*4.33,1))
# PERT: (name,o,m,p,preds)
acts=[('A Requirements & SRS',1,2,3,[]),('B DFD & ER design',1,2,3,['A']),('C UML design',1,2,3,['A']),
('D 3NF schema & DB setup',1,1,2,['B']),('E Auth + Application CRUD (Inc 1)',2,3,5,['C','D']),
('F Status FSM + Interviews (Inc 2)',2,3,4,['E']),('G Reminders + Dashboard (Inc 3)',2,3,4,['F']),
('H UI screens',2,3,4,['E']),('I Integration',1,2,3,['G','H']),('J Testing (unit, DFT)',2,2,3,['I']),
('K Green optimisation + report',1,1,2,['J'])]
te={a[0][0]:(a[1]+4*a[2]+a[3])/6 for a in acts}; pre={a[0][0]:[p for p in a[4]] for a in acts}
ES={};EF={}
for a in acts:
    k=a[0][0]; ES[k]=max([EF[p] for p in pre[k]],default=0); EF[k]=ES[k]+te[k]
T=max(EF.values()); LF={};LS={}
for a in reversed(acts):
    k=a[0][0]; succ=[b[0][0] for b in acts if k in b[4]]
    LF[k]=min([LS[s] for s in succ],default=T); LS[k]=LF[k]-te[k]
for a in acts:
    k=a[0][0]; print(a[0],round(te[k],2),round(ES[k],2),round(EF[k],2),'slack',round(LS[k]-ES[k],2))
print('CP length',round(T,2),'critical:',[a[0][0] for a in acts if abs(LS[a[0][0]]-ES[a[0][0]])<1e-9])
