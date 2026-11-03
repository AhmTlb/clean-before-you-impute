"""
Absolute comparison of complete pipelines (paper 2, requested in the manuscript revision)
=====================================================================================
Usage:  python analyze_m5_absolute.py results_m2 results_m3            (Jupyter: %run ...)
        python analyze_m5_absolute.py results_m4                       (adds knn / et imputers)

Question a practitioner asks: is "detect outliers, then iterative imputation" better or worse in ABSOLUTE
balanced accuracy than simply using mean imputation or native missing-value handling, with or without cleaning?
Per dataset: mean over seeds, then over the 6 primary conditions (symmetric outliers x MCAR/MAR/MNAR x 10/30%).
Reported: mean balanced accuracy (points) per pipeline and family, and the difference to "mean imputation,
no cleaning" with a 95% bootstrap interval over datasets and the share of datasets where it is positive.
Descriptive (no confirmatory claim).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

folders = [Path(a) for a in sys.argv[1:]] or [Path("results_m2"), Path("results_m3")]
parts = sorted(f for d in folders for f in (d / "parts").glob("*.pkl"))
if not parts:
    sys.exit("No finished jobs found")
df = pd.DataFrame([r for f in parts for r in pd.read_pickle(f)["rows"]])
S = [f"gross|{m}|{r:g}" for m in ["MCAR", "MAR", "MNAR"] for r in [0.1, 0.3]]
df = df[df["condition"].isin(S)].copy()
df["score"] = 100 * df["balanced_accuracy"]
ds = (df.groupby(["dataset", "condition", "family", "imputer", "arm"])["score"].mean()
        .groupby(["dataset", "family", "imputer", "arm"]).mean())

PIPES = [("mean", "none"), ("mean", "dti"), ("iter", "none"), ("iter", "itd"), ("iter", "dti"),
         ("knn", "none"), ("knn", "dti"), ("et", "none"), ("et", "dti"), ("native", "none"), ("native", "dti")]


def ci(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2:
        return "", np.nan
    m = np.random.default_rng(0).choice(x, (5000, len(x)), replace=True).mean(axis=1)
    return f"[{np.percentile(m, 2.5):+.2f}, {np.percentile(m, 97.5):+.2f}]", (x > 0).mean()


rows = []
for fam in ["LogReg", "KNN", "RandomForest", "HistGB"]:
    try:
        ref = ds.xs((fam, "mean", "none"), level=("family", "imputer", "arm"))
    except KeyError:
        continue
    for imp, arm in PIPES:
        try:
            s = ds.xs((fam, imp, arm), level=("family", "imputer", "arm"))
        except KeyError:
            continue
        if s.dropna().empty:
            continue
        d = (s - ref).dropna()
        c, share = ci(d)
        rows.append(dict(family=fam, pipeline=f"{imp} + {arm}", datasets=len(s), mean_BA=s.mean(),
                         diff_vs_mean_none=d.mean(), ci95=c, share_better=share))
T = pd.DataFrame(rows).round(3)
md = [f"# Absolute balanced accuracy of complete pipelines ({' + '.join(map(str, folders))})\n",
      "Six primary conditions; difference to mean imputation without cleaning. Descriptive.\n",
      T.to_markdown(index=False), ""]
out = folders[0] / "summary_m5_absolute.md"
out.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
print(f"\nSaved: {out}")
