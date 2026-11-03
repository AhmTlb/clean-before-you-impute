"""
Confirmatory analysis for paper 2 (PROTOCOL_m2.md): datasets 21-40, never used in Stages 1/1b
==========================================================================================
Usage:  python analyze_m2.py results_m2                     (one held-out set)
        python analyze_m2.py results_m3                     (independent replication, PROTOCOL_m3.md)
        python analyze_m2.py results_m2 results_m3          (pooled held-out datasets; summary in the first folder,
                                                             file summary_m2_pooled.md)

Primary conditions S = symmetric gross outliers x {MCAR, MAR, MNAR} x {10%, 30%} (6 conditions).
For each dataset, a quantity is averaged over seeds and then over the 6 conditions of S.
  H1 (order)       for each family F: gain(dti) - gain(itd) with the iterative imputer > 0   (4 tests)
  H2 (via imputer) for F in {RF, HistGB}: gain(dti | iterative) - gain(dti | native) > 0     (2 tests)
                   gain = BA(arm) - BA(arm none) within the same imputer and family
  H3 (propagation) log(RMSE_contaminated_fit / RMSE_clean_fit) of the iterative imputer > 0  (1 test)
One-sided Wilcoxon signed-rank tests over datasets, Holm correction over the 7 tests.
A hypothesis is SUPPORTED if p_Holm < 0.05 and the mean difference is in the predicted direction.
Secondary (descriptive, uncorrected): the same quantities with mean imputation; oracle_row versions of
H1-H2; cell - dti; oracle_cell - oracle_row; one-sided outliers (gross_pos); MNARobs.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

METRIC = "balanced_accuracy"          # optional last argument: ba_prior | auc_macro (BA-threshold check)
args = sys.argv[1:]
if args and args[-1] in ("ba_prior", "auc_macro", "balanced_accuracy"):
    METRIC = args.pop()
folders = [Path(a) for a in args] or [Path("results_m2")]
SUF = "" if METRIC == "balanced_accuracy" else f"_{METRIC}"
out = folders[0]
parts = sorted(f for d in folders for f in (d / "parts").glob("*.pkl"))
if not parts:
    sys.exit(f"No finished jobs in {[str(d / 'parts') for d in folders]}")
SUMMARY = ("summary_m2" if len(folders) == 1 else "summary_m2_pooled") + SUF + ".md"
res = [pd.read_pickle(f) for f in parts]
df = pd.DataFrame([r for x in res for r in x["rows"]])
mech = pd.DataFrame([r for x in res for r in x["mech"]])
df["score"] = 100 * df[METRIC]
key = ["dataset", "seed", "condition", "family", "imputer"]
df = df.join(df[df["arm"] == "none"].set_index(key)["score"].rename("base"), on=key)
df["gain"] = df["score"] - df["base"]

S = [f"gross|{m}|{r:g}" for m in ["MCAR", "MAR", "MNAR"] for r in [0.1, 0.3]]
POS = [f"gross_pos|{m}|0.3" for m in ["MCAR", "MAR", "MNAR"]]


def per_ds(arm, imputer, family, conds):
    s = df[(df["arm"] == arm) & (df["imputer"] == imputer) & (df["family"] == family)
           & df["condition"].isin(conds)]
    return s.groupby(["dataset", "condition"])["gain"].mean().groupby("dataset").mean()


def wil(x, alt):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    return wilcoxon(x, alternative=alt).pvalue if len(x) >= 6 and np.any(x != 0) else np.nan


def boot_ci(x, reps=5000, seed=0):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    m = rng.choice(x, (reps, len(x)), replace=True).mean(axis=1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


def holm(p):
    p = np.asarray(p, float)
    adj = np.full_like(p, np.nan)
    ok = np.where(~np.isnan(p))[0]
    run = 0.0
    for r, i in enumerate(ok[np.argsort(p[ok])]):
        run = max(run, min(1.0, (len(ok) - r) * p[i]))
        adj[i] = run
    return adj


rows = []
for fam in ["LogReg", "KNN", "RandomForest", "HistGB"]:
    d = (per_ds("dti", "iter", fam, S) - per_ds("itd", "iter", fam, S)).dropna()
    rows.append(dict(hypothesis="H1 order: dti - itd (iterative)", family=fam, n=len(d), mean=d.mean(),
                     ci95=boot_ci(d), median=d.median(), share_positive=(d > 0).mean(), p=wil(d, "greater")))
for fam in ["RandomForest", "HistGB"]:
    d = (per_ds("dti", "iter", fam, S) - per_ds("dti", "native", fam, S)).dropna()
    rows.append(dict(hypothesis="H2 via imputer: gain(dti|iter) - gain(dti|native)", family=fam, n=len(d),
                     mean=d.mean(), ci95=boot_ci(d), median=d.median(), share_positive=(d > 0).mean(),
                     p=wil(d, "greater")))
m = mech[mech["condition"].isin(S)].copy()
m["log_ratio"] = np.log(m["imp_rmse_iter_contaminated_fit"] / m["imp_rmse_iter_clean_fit"])
d = m.groupby(["dataset", "condition"])["log_ratio"].mean().groupby("dataset").mean().dropna()
rows.append(dict(hypothesis="H3 propagation: log RMSE ratio (iterative)", family="-", n=len(d), mean=d.mean(),
                 ci95=boot_ci(d), median=d.median(), share_positive=(d > 0).mean(), p=wil(d, "greater")))
T = pd.DataFrame(rows)
T["p_holm"] = holm(T["p"].values)
T["supported"] = (T["p_holm"] < 0.05) & (T["mean"] > 0)
T["ci95"] = T["ci95"].map(lambda c: f"[{c[0]:.2f}, {c[1]:.2f}]")
md = [f"# Paper 2: confirmatory test on held-out datasets ({' + '.join(str(d) for d in folders)})\n",
      f"Datasets: {df['dataset'].nunique()} | seeds: {df['seed'].nunique()} | primary conditions: {', '.join(S)}\n",
      "## Primary hypotheses (one-sided Wilcoxon over datasets, Holm over 7 tests)\n",
      T.round(4).to_markdown(index=False), ""]
for h in ["H1", "H2", "H3"]:
    t = T[T["hypothesis"].str.startswith(h)]
    md.append(f"- **{h}: {int(t['supported'].sum())} of {len(t)} tests supported**")
md.append("")

# ---------------------------------------------------------------- secondary
sec = []
for fam in ["LogReg", "KNN", "RandomForest", "HistGB"]:
    for conds, lab in [(S, "symmetric"), (POS, "one-sided")]:
        for a, b, imp, name in [("dti", "itd", "mean", "order with mean imputation"),
                                ("oracle_row", "itd", "iter", "oracle_row - itd (iterative)"),
                                ("cell", "dti", "iter", "cell - dti (iterative)"),
                                ("cell", "dti", "mean", "cell - dti (mean)"),
                                ("oracle_cell", "oracle_row", "iter", "oracle_cell - oracle_row (iterative)")]:
            d = (per_ds(a, imp, fam, conds) - per_ds(b, imp, fam, conds)).dropna()
            sec.append(dict(contrast=name, outliers=lab, family=fam, n=len(d), mean=d.mean(),
                            share_positive=(d > 0).mean(), p_two_sided=wil(d, "two-sided")))
    if fam in ("RandomForest", "HistGB"):
        for imp in ["iter", "mean", "native"]:
            d = per_ds("oracle_row", imp, fam, S).dropna()
            sec.append(dict(contrast=f"oracle_row gain ({imp})", outliers="symmetric", family=fam, n=len(d),
                            mean=d.mean(), share_positive=(d > 0).mean(), p_two_sided=wil(d, "two-sided")))
SEC = pd.DataFrame(sec).round(3)
md += ["## Secondary contrasts (descriptive, uncorrected)\n", SEC.to_markdown(index=False), ""]
mm = mech[mech["condition"].isin(S + POS)].copy()
for imp in ["mean", "iter"]:
    mm[f"ratio_{imp}"] = mm[f"imp_rmse_{imp}_contaminated_fit"] / mm[f"imp_rmse_{imp}_clean_fit"]
R = (mm.groupby(["dataset", "condition"])[["ratio_mean", "ratio_iter"]].mean()
       .groupby("condition").median().round(3))
md += ["## Propagation ratio by condition (median over datasets)\n", R.to_markdown(), ""]

(out / SUMMARY).write_text("\n".join(md), encoding="utf-8")
T.to_csv(out / SUMMARY.replace("summary", "tests").replace(".md", ".csv"), index=False)
SEC.to_csv(out / f"m2_secondary{SUF}.csv", index=False)
print("\n".join(md))
print(f"\nSaved: {out / SUMMARY}")
