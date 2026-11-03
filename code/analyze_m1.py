"""
Analysis for missing_experiment_v1.py (paper 2, Stage 1, exploratory; PROTOCOL_m1.md)
=====================================================================================
Usage:  python analyze_m1.py results_m1        (Jupyter: %run analyze_m1.py results_m1)

A  Mechanism (no models):
   A1 propagation  imputation RMSE on clean missing TEST cells, imputer fitted on contaminated vs
                   outlier-free training rows (ratio > 1 = outliers degrade imputation of clean cells)
   A2 masking      Isolation Forest recall@k of the true outlier rows: complete data vs median-filled
                   vs mean-imputed vs iterative-imputed training data
   A3 MNAR hiding  share of outlier cells that went missing; cell-rule precision / recall
B  Context: baseline (arm none) per imputer, relative to mean imputation
C  Arms vs. none (same imputer and family), per condition
D  Paired contrasts (dataset level, Wilcoxon two-sided, descriptive):
   dti - itd (order), cell - dti (cells vs rows), oracle_cell - oracle_row
Gains in balanced-accuracy points; seeds averaged within dataset; datasets weighted equally.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

out = Path(sys.argv[1] if len(sys.argv) > 1 else "results_m1")
parts = sorted((out / "parts").glob("*.pkl"))
if not parts:
    sys.exit(f"No finished jobs in {out / 'parts'}")
res = [pd.read_pickle(f) for f in parts]
df = pd.DataFrame([r for x in res for r in x["rows"]])
mech = pd.DataFrame([r for x in res for r in x["mech"]])
df["score"] = 100 * df["balanced_accuracy"]
FAMS = ["LogReg", "KNN", "RandomForest", "HistGB"]
IMPS = ["mean", "iter", "native"]
ARMS = ["itd", "dti", "cell", "oracle_row", "oracle_cell"]


def cond_key(c):
    o, m, r = c.split("|")
    return (["none", "gross", "gross_pos"].index(o), m != "complete", ["complete", "MCAR", "MAR", "MNAR", "MNARobs"].index(m), float(r))


CONDS = sorted(df["condition"].unique(), key=cond_key)


def wil(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    return wilcoxon(x).pvalue if len(x) >= 6 and np.any(x != 0) else np.nan


def ds_mean(d, keys, col):
    return d.groupby(["dataset"] + keys)[col].mean().reset_index()


md = ["# Paper 2, Stage 1: outliers in incomplete data (exploratory)\n",
      f"Datasets: {df['dataset'].nunique()} | seeds: {df['seed'].nunique()} | conditions: {len(CONDS)}\n",
      "Condition = outliers | missingness mechanism | missing rate.\n"]

# ------------------------------------------------------------------ A
g = mech[mech["outliers"].str.startswith("gross")].copy()
if len(g):
    cols1 = [c for c in g.columns if c.startswith("imp_rmse_")]
    if cols1:
        P = ds_mean(g[g["rate"] > 0], ["condition"], cols1)
        for imp in ["mean", "iter"]:
            a, b = f"imp_rmse_{imp}_contaminated_fit", f"imp_rmse_{imp}_clean_fit"
            if a in P:
                P[f"ratio_{imp}"] = P[a] / P[b]
        rc = [c for c in P.columns if c.startswith("ratio_")]
        A1 = P.groupby("condition")[cols1 + rc].median()
        for c in rc:
            A1[f"share_{c}_gt1.05"] = P.groupby("condition")[c].apply(lambda v: (v > 1.05).mean())
        md += ["## A1. Propagation: imputation error on clean test cells (clean-SD units; medians over datasets)\n",
               "contaminated_fit = imputer fitted on all training rows; clean_fit = on rows without "
               "outliers. ratio > 1 means the outliers degrade the imputation of clean cells.\n",
               A1.reindex(sorted(A1.index, key=cond_key)).round(3).to_markdown(), ""]
    cols2 = [c for c in g.columns if c.startswith("recall_IF_")]
    A2 = ds_mean(g, ["condition"], cols2).groupby("condition")[cols2].mean()
    md += ["## A2. Masking: Isolation Forest recall of the outlier rows (top k = number of outlier rows)\n",
           A2.reindex(sorted(A2.index, key=cond_key)).round(3).to_markdown(), ""]
    cols3 = ["outlier_cells_hidden_by_missing", "cell_flagged_share", "cell_precision", "cell_recall"]
    A3 = ds_mean(g, ["condition"], cols3).groupby("condition")[cols3].mean()
    md += ["## A3. Outlier cells hidden by missingness; cell rule (|modified z| > 3.5)\n",
           "cell_recall is over outlier cells that are still observed.\n",
           A3.reindex(sorted(A3.index, key=cond_key)).round(3).to_markdown(), ""]
nc = mech[mech["outliers"] == "none"]
if len(nc):
    B0 = ds_mean(nc, ["condition"], ["cell_flagged_share"]).groupby("condition")[["cell_flagged_share"]].mean()
    md += ["Share of cells the cell rule flags on outlier-free data (false alarms):\n",
           B0.reindex(sorted(B0.index, key=cond_key)).round(3).to_markdown(), ""]

# ------------------------------------------------------------------ B
nb = df[df["arm"] == "none"]
ref = nb[nb["imputer"] == "mean"].set_index(["dataset", "seed", "condition", "family"])["score"]
nb = nb.join(ref.rename("ref"), on=["dataset", "seed", "condition", "family"])
nb["vs_mean"] = nb["score"] - nb["ref"]
md += ["## B. Baselines (arm none): iterative / native minus mean imputation, points\n"]
for imp in ["iter", "native"]:
    s = nb[nb["imputer"] == imp]
    if len(s):
        T = (s.groupby(["family", "condition", "dataset"])["vs_mean"].mean()
               .groupby(["family", "condition"]).mean().unstack("condition"))
        md += [f"### {imp} - mean\n", T[[c for c in CONDS if c in T]].round(2).to_markdown(), ""]

# ------------------------------------------------------------------ C
key = ["dataset", "seed", "condition", "family", "imputer"]
base_ = df[df["arm"] == "none"].set_index(key)["score"].rename("base")
d = df.join(base_, on=key)
d["gain"] = d["score"] - d["base"]
md += ["## C. Gains vs. arm none (same imputer, same family), points\n"]
for fam in FAMS:
    for imp in IMPS:
        s = d[(d["family"] == fam) & (d["imputer"] == imp) & (d["arm"] != "none")]
        if s.empty:
            continue
        T = (s.groupby(["arm", "condition", "dataset"])["gain"].mean()
               .groupby(["arm", "condition"]).mean().unstack("condition"))
        T = T.reindex([a for a in ARMS if a in T.index])[[c for c in CONDS if c in T]].round(2)
        md += [f"### {fam} / {imp}\n", T.to_markdown(), ""]
        T.to_csv(out / f"m1_gains_{fam}_{imp}.csv")

# ------------------------------------------------------------------ D
piv = (d.groupby(["dataset", "condition", "family", "imputer", "arm"])["score"].mean()
         .unstack("arm"))
rows = []
for (a, b, label) in [("dti", "itd", "order: detect-then-impute - impute-then-detect"),
                      ("cell", "dti", "cells vs rows: cell - dti"),
                      ("oracle_cell", "oracle_row", "oracle cells - oracle rows")]:
    if a not in piv or b not in piv:
        continue
    diff = (piv[a] - piv[b]).dropna().reset_index(name="diff")
    for (cond, fam, imp), s in diff.groupby(["condition", "family", "imputer"]):
        if cond.startswith("none"):
            continue
        rows.append(dict(contrast=label, condition=cond, family=fam, imputer=imp,
                         n=len(s), mean=s["diff"].mean(), share_positive=(s["diff"] > 0).mean(),
                         p_two_sided=wil(s["diff"])))
D = pd.DataFrame(rows)
if len(D):
    D["k"] = D["condition"].map(cond_key)
    D = D.sort_values(["contrast", "imputer", "family", "k"]).drop(columns="k").round(3)
    md += ["## D. Paired contrasts on outlier conditions (descriptive, no correction)\n",
           D.to_markdown(index=False), ""]
    D.to_csv(out / "m1_contrasts.csv", index=False)

wip = df[df["arm"] != "none"].groupby("arm")["wiped_class"].mean().mul(100).round(2)
md += ["## E. Removals that deleted a whole class (%)\n", wip.to_frame("% wiped").to_markdown(), ""]

(out / "summary_m1.md").write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
print(f"\nSaved: {out / 'summary_m1.md'}")
