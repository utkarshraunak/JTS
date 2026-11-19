import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
NAVY='#1b365d'; 
dft=json.load(open('dft.json')); b=json.load(open('bench.json'))
fig=plt.figure(figsize=(15.7,7.0),dpi=200)
def box(ax,x,y,w,h,txt,fc,fs=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.01,rounding_size=0.02",fc=fc,ec=NAVY,lw=2))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,color='#1a1a1a')
def arr(ax,a,b_):
    ax.annotate('',xy=b_,xytext=a,arrowprops=dict(arrowstyle='->',color='#2d3a4f',lw=2))
def panel(pos,title):
    ax=fig.add_axes(pos); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.set_title(title,color=NAVY,fontsize=13,pad=6); return ax
ax=panel([0.02,0.52,0.46,0.38],'(a) Level-1 Data Flow & Core Modules (Exp 1–4)')
W,H=0.24,0.22
box(ax,0.05,0.62,W,H,'1.0 Auth &\nUser Profile','#eef4ff'); box(ax,0.38,0.62,W,H,'2.0 Application\nManager (CRUD)','#eef4ff'); box(ax,0.72,0.62,W,H,'3.0 Interview &\nReminder Engine','#eef4ff')
box(ax,0.38,0.12,W,H,'D1/D2/D3: 3NF\nSQLite (Users,\nApplications, Interviews)','#dff7e6',fs=9.5)
arr(ax,(0.29,0.73),(0.38,0.73)); arr(ax,(0.62,0.73),(0.72,0.73)); arr(ax,(0.50,0.62),(0.50,0.34)); arr(ax,(0.84,0.62),(0.62,0.30))
ax=panel([0.52,0.52,0.46,0.38],'(b) UML State-Chart: Application Status Flow (Exp 5–10)')
box(ax,0.03,0.62,W,H,'Saved\n(shortlisted job)','#dff7e6',fs=10); box(ax,0.38,0.62,W,H,'Applied\n(follow-up due)','#fff3c4',fs=10); box(ax,0.72,0.62,W,H,'Interview\nScheduled','#dbe8ff',fs=10)
box(ax,0.55,0.12,0.30,H,'Offer Received\n→ Accepted','#e3f5e1',fs=10); box(ax,0.08,0.12,0.30,H,'Rejected /\nWithdrawn (closed)','#fde0e0',fs=10)
arr(ax,(0.27,0.73),(0.38,0.73)); arr(ax,(0.62,0.73),(0.72,0.73)); arr(ax,(0.84,0.62),(0.76,0.34)); arr(ax,(0.55,0.23),(0.38,0.23)); arr(ax,(0.45,0.62),(0.30,0.34))
ax=fig.add_axes([0.06,0.08,0.40,0.36]); 
x=[d[0] for d in dft]
ax.plot(x,[d[3] for d in dft],'-o',color=NAVY,lw=3,ms=9,label='All-Defs (%)'); ax.plot(x,[d[4] for d in dft],'-s',color='#0f9488',lw=3,ms=9,label='All-Uses (9 DU pairs)')
ax.set_ylim(0,115); ax.set_ylabel('Coverage (%)'); ax.grid(ls='--',alpha=.4); ax.legend(loc='lower right'); ax.set_title('(c) Data Flow Testing DU Coverage (Exp 14)',color=NAVY,fontsize=13)
ax=fig.add_axes([0.56,0.08,0.41,0.36])
labs=['W1 CPU\n(Lookup)','W2 CPU\n(Reminder\nMonitor)','W3 Data\nTransfer','W4 DB\nStorage','SCI\n(gCO2e/R)']
vals=[b['w1'][2],b['w2'][2],b['w3'][2],b['w4'][2],b['sci'][2]]
bars=ax.bar(labs,vals,width=.5,color=[NAVY,'#2563eb','#0f9488','#059669','#188038'])
for r,v in zip(bars,vals): ax.text(r.get_x()+r.get_width()/2,v+1.5,f'{v:.2f}%',ha='center',fontsize=9)
ax.set_ylim(0,115); ax.set_ylabel('Reduction (%)'); ax.grid(axis='y',ls='--',alpha=.4); ax.set_title('(d) Green SE Optimization Gains (Exp 15)',color=NAVY,fontsize=13); ax.tick_params(axis='x',labelsize=9)
fig.savefig('figure.png'); 
