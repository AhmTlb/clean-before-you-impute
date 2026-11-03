"""
Robustness analysis for paper 2 (PROTOCOL_m4.md): do H1-H3 hold for other imputers?
=================================================================================
Usage:  python analyze_m4.py results_m4        (Jupyter: %run analyze_m4.py results_m4)

For every imputer that was run (mean, iter = BayesianRidge, knn = KNNImputer, et = ExtraTrees):
  H1-type  gain(dti) - gain(itd) per family                      (order)
  H2-type  gain(dti | imputer) - gain(dti | native), RF and HistGB (removal helps trees via the imputer)
  H3-type  log(RMSE contaminated fit / RMSE clean fit)           (propagation)
  plus     gain(oracle_row) per family                           (benefit of perfect removal)
Per dataset: mean over seeds, then over the 6 primary conditions. Mean, 95% bootstrap CI, share of
datasets > 0, one-sided Wilcoxon p. DESCRIPTIVE: no multiplicity correction, no confirmatory claim.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

out = Path(sys.argv[1] if len(sys.argv) > 1 else "results_m4")
parts = sorted((out / "parts").glob("*.pkl"))
if not parts:
    sys.exit(f"No finished jobs in {out / 'parts'}")
res = [pd.read_pickle(f) for f in parts]
df = pd.DataFrame([r for x in res for r in x["rows"]])
mech = pd.DataFrame([r for x in res for r in x["mech"]])
df["score"] = 100 * df["balanced_accuracy"]
key = ["dataset", "seed", "condition", "family", "imputer"]
df = df.join(df[df["arm"] == "none"].set_index(key)["score"].rename("base"), on=key)
df["gain"] = df["score"] - df["base"]
S = [f"gross|{m}|{r:g}" for m in ["MCAR", "MAR", "MNAR"] for r in [0.1, 0.3]]
FAMS = ["LogReg", "KNN", "RandomForest", "HistGB"]
IMPS = [i for i in ["mean", "iter", "knn", "et"] if i in set(df["imputer"])]
NAMES = {"mean": "mean", "iter": "iterative (BayesianRidge)", "knn": "KNNImputer", "et": "iterative (ExtraTrees)"}


def per_ds(arm, imp, fam):
    s = df[(df["arm"] == arm) & (df["imputer"] == imp) & (df["family"] == fam) & df["condition"].isin(S)]
    return s.groupby(["dataset", "condition"])["gain"].mean().groupby("dataset").mean()


def stats(d):
    d = d.dropna()
    x = d.to_numpy(float)
    rng = np.random.default_rng(0)
    bm = rng.choice(x, (5000, len(x)), replace=True).mean(axis=1) if len(x) > 1 else np.array([np.nan])
    p = wilcoxon(x, alternative="greater").pvalue if len(x) >= 6 and np.any(x != 0) else np.nan
    return dict(n=len(x), mean=x.mean(), ci95=f"[{np.percentile(bm, 2.5):.2f}, {np.percentile(bm, 97.5):.2f}]",
                share_positive=(x > 0).mean(), p_one_sided=p)


rows = []
for imp in IMPS:
    for fam in FAMS:
        rows.append(dict(quantity="H1 order: dti - itd", imputer=NAMES[imp], family=fam,
                         **stats(per_ds("dti", imp, fam) - per_ds("itd", imp, fam))))
    for fam in ["RandomForest", "HistGB"]:
        rows.append(dict(quantity="H2 via imputer: gain(dti|imp) - gain(dti|native)", imputer=NAMES[imp],
                         family=fam, **stats(per_ds("dti", imp, fam) - per_ds("dti", "native", fam))))
    a, b = f"imp_rmse_{imp}_contaminated_fit", f"imp_rmse_{imp}_clean_fit"
    if a in mech:
        m = mech[mech["condition"].isin(S)].copy()
        m["lr"] = np.log(m[a] / m[b])
        d = m.groupby(["dataset", "condition"])["lr"].mean().groupby("dataset").mean()
        rows.append(dict(quantity="H3 propagation: log RMSE ratio", imputer=NAMES[imp], family="-", **stats(d)))
    for fam in FAMS:
        rows.append(dict(quantity="oracle_row gain", imputer=NAMES[imp], family=fam,
                         **stats(per_ds("oracle_row", imp, fam))))
for fam in ["RandomForest", "HistGB"]:
    rows.append(dict(quantity="oracle_row gain", imputer="native", family=fam, **stats(per_ds("oracle_row", "native", fam))))
T = pd.DataFrame(rows)
T["p_one_sided"] = T["p_one_sided"].round(4)
T = T.round(3)
md = ["# Paper 2, Stage 4: robustness to the choice of imputer (descriptive)\n",
      f"Datasets: {df['dataset'].nunique()} | seeds: {df['seed'].nunique()} | conditions: {', '.join(S)}\n",
      "No multiplicity correction; these results qualify, but do not replace, the confirmatory tests.\n"]
for q in T["quantity"].unique():
    md += [f"## {q}\n", T[T["quantity"] == q].drop(columns="quantity").to_markdown(index=False), ""]
(out / "summary_m4.md").write_text("\n".join(md), encoding="utf-8")
T.to_csv(out / "m4_robustness.csv", index=False)
print("\n".join(md))
print(f"\nSaved: {out / 'summary_m4.md'}")
