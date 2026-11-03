"""Figures for 'Clean Before You Impute'. Numbers copied from summary_m2.md (Stage 2, results_m2),
results_m3/summary_m2.md (Stage 3), summary_m2_pooled.md (pooled) and summary_m4.md (Stage 4)."""
import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e2dc"
GREY, BLUE, ORANGE, AQUA = "#8a8880", "#2a78d6", "#eb6834", "#1baf7a"
mpl.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.spines.top":False,"axes.spines.right":False,
  "axes.edgecolor":INK2,"xtick.color":INK2,"ytick.color":INK2,"axes.linewidth":.6,"legend.frameon":False,
  "savefig.bbox":"tight","pdf.fonttype":42})
def save(fig,n):
    fig.savefig(f"figures/{n}.pdf"); fig.savefig(f"figures/{n}.png",dpi=300); plt.close(fig)

# ---------------- Figure 1: confirmatory tests across held-out sets
rows = [  # label, stage2 mean, stage2 supported, stage3 mean, stage3 supported, pooled mean, lo, hi
 ("H1 order · KNN",                1.003,True, 0.649,True, 0.831,0.46,1.28),
 ("H1 order · random forest",      0.423,False,0.589,True, 0.504,0.23,0.79),
 ("H1 order · logistic regression",0.503,False,0.499,False,0.501,0.17,0.88),
 ("H1 order · gradient boosting",  0.340,False,0.376,False,0.358,0.10,0.59),
 ("H2 route · random forest",      0.467,False,0.620,True, 0.541,0.26,0.84),
 ("H2 route · gradient boosting",  0.088,False,0.498,False,0.288,-0.03,0.62),
]
fig, ax = plt.subplots(figsize=(6.4,3.3))
y = np.arange(len(rows))[::-1]
ax.axvline(0,color=INK2,lw=.7); ax.xaxis.grid(True,color=GRID,lw=.6); ax.set_axisbelow(True)
for yi,(lab,s2,ok2,s3,ok3,pm,lo,hi) in zip(y,rows):
    ax.plot([lo,hi],[yi,yi],color=INK,lw=1.2,zorder=2)
    ax.scatter(pm,yi,s=40,color=INK,zorder=3,marker="D")
    ax.scatter(s2,yi+.25,s=26,color=BLUE,zorder=3,marker="o",facecolors=BLUE if ok2 else "white",edgecolors=BLUE,lw=1.2)
    ax.scatter(s3,yi-.25,s=26,color=ORANGE,zorder=3,marker="s",facecolors=ORANGE if ok3 else "white",edgecolors=ORANGE,lw=1.2)
ax.set_yticks(y,[r[0] for r in rows]); ax.tick_params(axis="y",length=0)
ax.set_xlabel("Effect, balanced-accuracy points (iterative imputation)")
ax.scatter([],[],color=BLUE,marker="o",s=26,label="Stage 2 confirmation (20 datasets)")
ax.scatter([],[],color=ORANGE,marker="s",s=26,label="Stage 3 replication (19 datasets)")
ax.scatter([],[],color=INK,marker="D",s=34,label="Pooled mean, 95% CI (39 datasets)")
ax.scatter([],[],facecolors="white",edgecolors=GREY,marker="o",s=26,label="open marker: not significant after Holm")
ax.legend(loc="upper center",bbox_to_anchor=(0.45,-0.2),ncol=2,fontsize=7,handletextpad=.3,columnspacing=1.2)
ax.set_xlim(-0.3,1.5)
ax.set_title("Detecting outliers before iterative imputation: no effect reversed in either held-out set",loc="left",fontsize=8.5)
save(fig,"fig1_confirmation")

# ---------------- Figure 2: imputers
imps = ["Iterative\n(Bayes.\nridge)","Iterative\n(extra\ntrees)","k-nearest\nneighbours","Mean"]
prop = [0.105,0.106,0.036,0.0]; plo=[0.05,0.08,0.02,-0.001]; phi=[0.16,0.14,0.05,0.001]
pct = lambda v: 100*(np.exp(v)-1)
order = {  # family: list over imputers of (mean, lo, hi)
 "LogReg":[(0.501,.17,.88),(0.363,.21,.53),(0.297,.10,.54),(-0.001,-.06,.06)],
 "KNN":[(0.831,.46,1.28),(0.688,.42,.95),(0.093,-.02,.23),(0.155,-.15,.56)],
 "RandomForest":[(0.504,.23,.79),(0.48,.31,.65),(-0.016,-.13,.10),(0.032,-.09,.15)],
 "HistGB":[(0.358,.10,.59),(0.614,.39,.87),(0.255,.07,.45),(0.034,-.11,.17)]}
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.4,3.1),gridspec_kw=dict(width_ratios=[1,1.6]))
x=np.arange(4)
a1.bar(x,[pct(v) for v in prop],.55,color=[BLUE,BLUE,GREY,GREY],zorder=2)
a1.errorbar(x,[pct(v) for v in prop],yerr=[[pct(v)-pct(l) for v,l in zip(prop,plo)],[pct(h)-pct(v) for v,h in zip(prop,phi)]],fmt="none",ecolor=INK,lw=1,capsize=2,zorder=3)
a1.set_xticks(x,imps,fontsize=7); a1.tick_params(axis="x",length=0)
a1.set_ylabel("Imputation error on clean cells,\nincrease caused by outliers (%)")
a1.yaxis.grid(True,color=GRID,lw=.6); a1.set_axisbelow(True); a1.axhline(0,color=INK2,lw=.7)
a1.set_title("Propagation",loc="left",fontsize=8.5)
cols=[BLUE,AQUA,ORANGE,GREY]; fams=list(order); w=.19
for k,(f,c) in enumerate(zip(fams,cols)):
    m=[order[f][i][0] for i in range(4)]; lo=[order[f][i][1] for i in range(4)]; hi=[order[f][i][2] for i in range(4)]
    xx=x+(k-1.5)*w
    a2.errorbar(xx,m,yerr=[np.subtract(m,lo),np.subtract(hi,m)],fmt="o",color=c,ms=4,lw=1,capsize=0,label=f.replace("RandomForest","Random forest").replace("HistGB","Gradient boosting").replace("LogReg","Logistic regression"))
a2.axhline(0,color=INK2,lw=.7); a2.yaxis.grid(True,color=GRID,lw=.6); a2.set_axisbelow(True)
a2.set_xticks(x,imps,fontsize=7); a2.tick_params(axis="x",length=0)
a2.set_ylabel("Detect-then-impute minus\nimpute-then-detect (points)")
a2.set_title("Order effect, mean and 95% CI",loc="left",fontsize=8.5)
a2.legend(fontsize=6.8,loc="upper right",ncol=2,handletextpad=.2,columnspacing=.8)
fig.suptitle("Iterative imputers, linear or tree-based, propagate outliers; neighbour and mean imputation barely do",x=.01,ha="left",fontsize=8.5,y=1.02)
fig.tight_layout()
save(fig,"fig2_imputers")
print("ok")
