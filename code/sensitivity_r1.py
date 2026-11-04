"""
Sensitivity analysis for "Clean Before You Impute" (pre-submission review; no new experiments)
==============================================================================================
Re-estimates the pooled primary effects (H1 order, H2 route, H3 propagation; 39 held-out datasets,
Stages 2 and 3) on subsets of datasets, to check two possible confounders:
  1. pre-existing missing values, which were median-filled on the whole dataset before splitting;
  2. categorical features, which were ordinal-encoded and then treated as numbers.

Usage (from code/, with the OpenML cache used for the experiments):
    python sensitivity_r1.py ../results            (Jupyter: %run sensitivity_r1.py ../results)
Reads ../results/results_m2b and ../results/results_m3b (rows.csv.gz, mech.csv.gz), the reruns of
Stages 2 and 3 that record all three metrics. Dataset properties (share of categorical columns, share of
pre-existing missing cells) are read from OpenML through the same loader as the experiments and saved
to ../results/dataset_properties.csv. Writes ../results/summary_sensitivity_r1.md.

Subsets (fixed before looking at any subset result):
  all            the 39 held-out datasets
  no_native_nan  datasets without pre-existing missing values
  mostly_numeric datasets with at most 20% categorical columns
  majority_numeric      datasets with at most 50% categorical columns
  numeric_and_complete  both conditions
  mostly_categorical    datasets with more than 50% categorical columns (for contrast)
Effects are pooled means over datasets with 95% bootstrap CIs; p = one-sided Wilcoxon (descriptive).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

root = Path(sys.argv[1] if len(sys.argv) > 1 else "../results")
FOLDERS = ["results_m2b", "results_m3b"]
FAMS = ["LogReg", "KNN", "RandomForest", "HistGB"]
S = [f"gross|{m}|{r:g}" for m in ["MCAR", "MAR", "MNAR"] for r in [0.1, 0.3]]
RNG = np.random.default_rng(0)


def read(table):
    fs = [root / d / f"{table}.csv.gz" for d in FOLDERS]
    miss = [str(f) for f in fs if not f.exists()]
    if miss:
        sys.exit(f"Missing: {miss}")
    return pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)


rows, mech = read("rows"), read("mech")
names = sorted(rows["dataset"].unique())
print(f"{len(names)} datasets in {FOLDERS}")

# ------------------------------------------------------------ dataset properties
prop_file = root / "dataset_properties.csv"
if prop_file.exists():
    props = pd.read_csv(prop_file)
else:
    import overlap_experiment as base
    recs = []
    for name, X, y in base.load_openml_cc18(10_000, 2000, 200):
        if name not in names:
            continue
        cat = [c for c in X.columns if not pd.api.types.is_numeric_dtype(X[c])]
        recs.append(dict(dataset=name, n_cols=X.shape[1], cat_share=len(cat) / max(1, X.shape[1]),
                         native_missing_share=float(X.isna().to_numpy().mean())))
        print(f"  {name}: categorical {len(cat)}/{X.shape[1]}, missing {recs[-1]['native_missing_share']:.4f}")
    props = pd.DataFrame(recs)
    props.to_csv(prop_file, index=False)
missing_props = sorted(set(names) - set(props["dataset"]))
if missing_props:
    print("WARNING: no properties for", missing_props)
P = props.set_index("dataset")

SUBSETS = {
    "all": names,
    "no_native_nan": [d for d in names if d in P.index and P.at[d, "native_missing_share"] == 0],
    "mostly_numeric": [d for d in names if d in P.index and P.at[d, "cat_share"] <= 0.2],
    "majority_numeric": [d for d in names if d in P.index and P.at[d, "cat_share"] <= 0.5],
    "numeric_and_complete": [d for d in names if d in P.index and P.at[d, "cat_share"] <= 0.2
                             and P.at[d, "native_missing_share"] == 0],
    "mostly_categorical": [d for d in names if d in P.index and P.at[d, "cat_share"] > 0.5],
}


def ci(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 3:
        return np.nan, np.nan, np.nan
    bs = RNG.choice(x, (5000, len(x)), replace=True).mean(1)
    return x.mean(), *np.percentile(bs, [2.5, 97.5])


def wil(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    return wilcoxon(x, alternative="greater").pvalue if len(x) >= 6 and np.any(x != 0) else np.nan


def effects(metric):
    df = rows.copy()
    df["score"] = 100 * df[metric]
    key = ["dataset", "seed", "condition", "family", "imputer"]
    df = df.join(df[df["arm"] == "none"].set_index(key)["score"].rename("base"), on=key)
    df["gain"] = df["score"] - df["base"]

    def per_ds(arm, imp, fam):
        s = df[(df["arm"] == arm) & (df["imputer"] == imp) & (df["family"] == fam) & df["condition"].isin(S)]
        return s.groupby(["dataset", "condition"])["gain"].mean().groupby("dataset").mean()

    out = {}
    for fam in FAMS:
        out[f"H1 order, {fam}"] = per_ds("dti", "iter", fam) - per_ds("itd", "iter", fam)
    for fam in ["RandomForest", "HistGB"]:
        out[f"H2 route, {fam}"] = per_ds("dti", "iter", fam) - per_ds("dti", "native", fam)
    return out


m = mech[mech["condition"].isin(S)].copy()
m["log_ratio"] = np.log(m["imp_rmse_iter_contaminated_fit"] / m["imp_rmse_iter_clean_fit"])
h3 = m.groupby(["dataset", "condition"])["log_ratio"].mean().groupby("dataset").mean()

md = ["# Paper 2: sensitivity of the primary effects to pre-existing missing values and categorical features\n",
      "Post hoc (after a pre-submission review). Pooled Stages 2 and 3; six primary conditions; iterative "
      "imputation. Mean [95% bootstrap CI], one-sided Wilcoxon p (descriptive), n datasets.\n",
      "## Subsets\n",
      pd.DataFrame([dict(subset=k, n=len(v)) for k, v in SUBSETS.items()]).to_markdown(index=False), "",
      "## Dataset properties\n",
      props.sort_values("cat_share").round(4).to_markdown(index=False), ""]
for metric, lab in [("balanced_accuracy", "default rule"), ("ba_prior", "prior-corrected rule"),
                    ("auc_macro", "ROC AUC")]:
    if metric not in rows.columns:
        continue
    E = effects(metric)
    if metric == "balanced_accuracy":
        E["H3 propagation, log RMSE ratio"] = h3
    tab = []
    for h, s in E.items():
        r = dict(hypothesis=h)
        for sub, ds in SUBSETS.items():
            x = s.reindex(ds).dropna()
            mu, lo, hi = ci(x)
            r[sub] = f"{mu:+.3f} [{lo:+.2f}, {hi:+.2f}] p={wil(x):.3f} n={len(x)}"
        tab.append(r)
    md += [f"## Effects, {lab}\n", pd.DataFrame(tab).to_markdown(index=False), ""]

text = "\n".join(md)
(root / "summary_sensitivity_r1.md").write_text(text, encoding="utf-8")
print(text)
print(f"\nSaved: {root / 'summary_sensitivity_r1.md'}")
