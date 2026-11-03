"""
Paper 2, Stage 1b (exploratory, revised after Stage 1): outliers in incomplete tabular data
========================================================================================
Changes from v1 (see PROTOCOL_m1b.md): KNN without missingness indicators; cell rule also applied to
the test set; one-sided outliers (gross_pos) added; propagation measured in clean-SD units per dataset.

Questions (PROTOCOL_m1.md)
  RQ1 order      impute-then-detect (itd) vs detect-then-impute (dti) vs leave missing values to the model
  RQ2 mechanism  (a) propagation: do outliers in the training data degrade the imputation of CLEAN cells?
                 (b) masking: does imputation hide outlier rows from the detector?
                 (c) under MNAR, how many outlier cells disappear because they went missing?
  RQ3 cells      set suspicious cells to missing (cell) vs remove whole rows (itd/dti)

Data flow per (dataset, seed, condition)
  complete data X (pre-existing NaN median-filled by base.to_numeric; recorded as a limitation)
  -> split train/test exactly as in paper 1
  -> inject gross outliers in 10% of TRAIN rows (about 20% of the features of each row, 5-10 SD); cell mask kept
  -> inject missing cells in train AND test with the same mechanism: MCAR, MAR (driven by the true values of
     always-observed features), MNAR (self-masking on the true value: high values more likely missing),
     at 10% or 30% of maskable cells; plus MNARobs at 30% (extreme RECORDED values go missing; stress case)
  Test labels and test feature values are never corrupted; only missingness is applied to the test set.

Arms (row removal = top 10% by Isolation Forest, as in paper 1)
  none        impute -> model
  itd         impute (fit on all train rows) -> IF on the imputed data -> remove rows -> model
  dti         IF on a median-filled copy (detection only) -> remove rows -> fit imputer on remaining rows -> model
  cell        cells with |modified z| > 3.5 (median/MAD on observed train values) -> NaN -> impute -> model
  oracle_row  remove the true outlier rows -> impute -> model
  oracle_cell set the true outlier cells to NaN -> impute -> model
Imputers: mean (+ missingness indicators), iter (IterativeImputer, BayesianRidge, + indicators),
          native (no imputation; only for model families that accept NaN: RandomForest, HistGB).
Models: LogReg, KNN, RandomForest, HistGB with default settings (as paper 1).

Usage
  python missing_experiment_v2.py --source openml --max-datasets 20 --seeds 3 --n-jobs 10 --out results_m1b
  python missing_experiment_v2.py --source openml --max-datasets 40 --start 20 --seeds 3 --n-jobs 10 --out results_m2   (confirmation)
  python missing_experiment_v1.py --source sklearn --max-datasets 2 --seeds 1 --n-jobs 2 --preset smoke --out m1_smoke
Then:  python analyze_m1.py results_m1
"""
from __future__ import annotations

import argparse
import time
import traceback
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed, parallel_config
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import experiment_v4 as v4     # threshold_free_metrics (BA-threshold check, PROTOCOL_m_ba_check.md)
import overlap_experiment as base

MECHS = ["MCAR", "MAR", "MNAR"]
PRESETS = {
    "full": ([("none", "MCAR", 0.0), ("gross", "MCAR", 0.0), ("gross_pos", "MCAR", 0.0)] +
             [(o, m, r) for o in ["none", "gross"] for m in MECHS for r in [0.1, 0.3]] +
             [("gross_pos", m, 0.3) for m in MECHS] +
             [("none", "MNARobs", 0.3), ("gross", "MNARobs", 0.3)]),
    "smoke": [("none", "MCAR", 0.0), ("gross", "MCAR", 0.3), ("gross_pos", "MCAR", 0.3),
              ("none", "MCAR", 0.3)],
}
REMOVE_FRAC = 0.10
CELL_Z = 3.5            # Iglewicz & Hoaglin modified z-score rule
FAMILIES = ["LogReg", "KNN", "RandomForest", "HistGB"]
NATIVE = {"RandomForest", "HistGB"}


# ---------------------------------------------------------------- corruption
def inject_outliers(X, rate, rng, lo=5.0, hi=10.0, one_sided=False):
    X = X.copy()
    n, p = X.shape
    cells = np.zeros_like(X, dtype=bool)
    m = int(round(rate * n))
    if m == 0:
        return X, cells
    med, sd = np.median(X, axis=0), X.std(axis=0)
    sd = np.where(sd == 0, 1.0, sd)
    n_f = max(1, int(np.ceil(0.2 * p)))
    for i in rng.choice(n, m, replace=False):
        f = rng.choice(p, n_f, replace=False)
        sign = np.ones(n_f) if one_sided else rng.choice([-1, 1], n_f)
        X[i, f] = med[f] + sign * rng.uniform(lo, hi, n_f) * sd[f]
        cells[i, f] = True
    return X, cells


def robust_scale(X):
    """median and robust spread per column (MAD*1.4826, falling back to SD, then 1)."""
    med = np.nanmedian(X, axis=0)
    mad = 1.4826 * np.nanmedian(np.abs(X - med), axis=0)
    sd = np.nanstd(X, axis=0)
    s = np.where(mad > 0, mad, np.where(sd > 0, sd, 1.0))
    return med, s


def _calibrated_mask(score, rate, rng, slope=2.0):
    """P(missing) = sigmoid(slope*score + b), b chosen by bisection so that mean P = rate."""
    lo, hi = -30.0, 30.0
    for _ in range(60):
        b = (lo + hi) / 2
        pr = 1 / (1 + np.exp(-(slope * score + b)))
        lo, hi = (b, hi) if pr.mean() < rate else (lo, b)
    return rng.random(score.shape) < pr


def inject_missing(X, mech, rate, rng, med, s, drivers, X_true):
    """Returns X with NaN and the missing mask. `med`, `s` come from the CLEAN training data.
    MAR and MNAR depend on the TRUE (uncorrupted) values X_true: the data-generating process decides
    what goes missing, independently of recording errors. MNAR = high true values more likely missing.
    MNARobs = extreme RECORDED values more likely missing (|z| of the observed, possibly corrupted value),
    a deliberate stress case in which missingness can swallow the outliers."""
    X = X.copy()
    n, p = X.shape
    miss = np.zeros_like(X, dtype=bool)
    if rate <= 0:
        return X, miss
    z = np.clip((X_true - med) / s, -20, 20)
    z_obs = np.clip((X - med) / s, -20, 20)
    targets = [j for j in range(p) if j not in drivers] if mech == "MAR" else list(range(p))
    for j in targets:
        if mech == "MCAR":
            miss[:, j] = rng.random(n) < rate
        elif mech == "MAR":
            miss[:, j] = _calibrated_mask(z[:, drivers[j % len(drivers)]], rate, rng)
        elif mech == "MNAR":  # self-masking on the true value: large values go missing
            miss[:, j] = _calibrated_mask(z[:, j], rate, rng)
        else:                 # MNARobs: extreme recorded values go missing
            miss[:, j] = _calibrated_mask(np.abs(z_obs[:, j]) - 1.0, rate, rng)
    X[miss] = np.nan
    return X, miss


# ---------------------------------------------------------------- models and imputers
NO_INDICATOR = {"KNN"}   # Stage 1: indicators + scaling distort KNN distances (documented in PROTOCOL_m1b)


def make_imputer(kind, p, seed, indicator=True):
    if kind == "mean":
        return SimpleImputer(strategy="mean", add_indicator=indicator, keep_empty_features=True)
    if kind == "iter":
        return IterativeImputer(max_iter=5, n_nearest_features=min(20, max(1, p - 1)),
                                random_state=seed, add_indicator=indicator, keep_empty_features=True)
    raise ValueError(kind)


def make_model(family, seed):
    if family == "LogReg":
        return make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))
    if family == "KNN":
        return make_pipeline(StandardScaler(), KNeighborsClassifier())
    if family == "RandomForest":
        return RandomForestClassifier(n_estimators=150, random_state=seed, n_jobs=1)
    return HistGradientBoostingClassifier(random_state=seed)


def fit_eval(Xtr, ytr, Xte, yte, imputer, family, seed):
    """imputer: a fitted transformer, or None for native NaN handling."""
    if imputer is not None:
        Xtr, Xte = imputer.transform(Xtr), imputer.transform(Xte)
    est = make_model(family, seed).fit(Xtr, ytr)
    pred = est.predict(Xte)
    extra = v4.threshold_free_metrics(est, Xte, yte, ytr)
    return balanced_accuracy_score(yte, pred), accuracy_score(yte, pred), extra


def top_rows(X_filled, frac, seed):
    Xs = StandardScaler().fit_transform(X_filled)
    k = max(1, int(round(frac * len(Xs))))
    return np.argsort(-base.score_iforest(Xs, seed), kind="stable")[:k], Xs


def recall_at_k(X_filled, truth_rows, seed):
    k = int(truth_rows.sum())
    if k == 0:
        return np.nan
    idx, _ = top_rows(X_filled, k / len(X_filled), seed)
    return float(truth_rows[idx[:k]].mean())


# ---------------------------------------------------------------- one job
def run_job(name, X, y, seed, conditions, part_path):
    warnings.filterwarnings("ignore")
    t0 = time.time()
    rows, mech_rows, log = [], [], []
    try:
        X_tv, X_te0, y_tv, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
        X_tr0, _, y_tr, _ = train_test_split(X_tv, y_tv, test_size=0.2, stratify=y_tv, random_state=seed)
        n, p = X_tr0.shape
        K = len(np.unique(y_tr))
        med_c, s_c = robust_scale(X_tr0)                       # clean reference, for MNAR/MAR scores
        sd_c = X_tr0.std(axis=0)
        sd_c = np.where(sd_c > 0, sd_c, 1.0)                   # propagation is measured in clean-SD units
        drng = np.random.default_rng(1000 + seed)
        drivers = list(drng.choice(p, max(1, int(np.ceil(0.3 * p))), replace=False)) if p > 1 else [0]
        for outl, mech, rate in conditions:
            cond = f"{outl}|{mech if rate > 0 else 'complete'}|{rate:g}"
            rng = np.random.default_rng(10_000 * seed + int(rate * 1000) + 97 * len(mech) + 7 * len(outl))
            X_out, ocell = (inject_outliers(X_tr0, REMOVE_FRAC, rng, one_sided=(outl == "gross_pos"))
                            if outl.startswith("gross") else (X_tr0.copy(), np.zeros_like(X_tr0, dtype=bool)))
            orow = ocell.any(axis=1)
            X_tr, mtr = inject_missing(X_out, mech, rate, rng, med_c, s_c, drivers, X_tr0)
            X_te, mte = inject_missing(X_te0, mech, rate, rng, med_c, s_c, drivers, X_te0)
            common = dict(dataset=name, seed=seed, condition=cond, outliers=outl,
                          mechanism=mech if rate > 0 else "complete", rate=rate, n_classes=K, n_train=n)

            # -------- row sets for each arm
            med_fill = np.where(np.isnan(X_tr), np.nanmedian(X_tr, axis=0), X_tr)
            med_fill = np.where(np.isnan(med_fill), 0.0, med_fill)
            dti_drop, _ = top_rows(med_fill, REMOVE_FRAC, seed)
            mz, ms = robust_scale(X_tr)
            cell_flag = np.abs((X_tr - mz) / ms) > CELL_Z   # (x-med)/(1.4826 MAD) = 0.6745 (x-med)/MAD
            cell_flag &= ~np.isnan(X_tr)
            X_cell = X_tr.copy()
            X_cell[cell_flag] = np.nan
            te_flag = (np.abs((X_te - mz) / ms) > CELL_Z) & ~np.isnan(X_te)   # same fitted rule on test
            X_te_cell = X_te.copy()
            X_te_cell[te_flag] = np.nan
            X_ocell = X_tr.copy()
            X_ocell[ocell] = np.nan
            keep_all = np.arange(n)

            # -------- mechanism metrics (no models)
            mrow = dict(**common,
                        outlier_cells=int(ocell.sum()),
                        outlier_cells_hidden_by_missing=float((ocell & mtr).sum() / max(1, ocell.sum())),
                        cell_flagged_share=float(cell_flag.sum() / max(1, (~np.isnan(X_tr)).sum())),
                        cell_precision=float((cell_flag & ocell).sum() / max(1, cell_flag.sum())) if outl.startswith("gross") else np.nan,
                        cell_recall=float((cell_flag & ocell).sum() / max(1, (ocell & ~mtr).sum())) if outl.startswith("gross") else np.nan,
                        recall_IF_complete=recall_at_k(X_out, orow, seed) if outl.startswith("gross") else np.nan,
                        recall_IF_medianfill=recall_at_k(med_fill, orow, seed) if outl.startswith("gross") else np.nan)

            imputers = {}
            for imp in ["mean", "iter"]:
                try:
                    for ind in (True, False):
                        imputers[(imp, "all", ind)] = make_imputer(imp, p, seed, indicator=ind).fit(X_tr)
                    det = make_imputer(imp, p, seed, indicator=False).fit(X_tr)
                    X_imp = det.transform(X_tr)
                    imputers[(imp, "itd_drop")] = top_rows(X_imp, REMOVE_FRAC, seed)[0]
                    if outl.startswith("gross"):
                        mrow[f"recall_IF_{imp}_imputed"] = recall_at_k(X_imp, orow, seed)
                    # propagation: error on CLEAN missing test cells, imputer fit with vs without outlier rows
                    if rate > 0:
                        clean_fit = make_imputer(imp, p, seed, indicator=False).fit(X_tr[~orow])
                        Te_all, Te_cln = det.transform(X_te), clean_fit.transform(X_te)
                        err = lambda A: float(np.sqrt(np.mean((((A - X_te0) / sd_c)[mte]) ** 2))) if mte.any() else np.nan
                        mrow[f"imp_rmse_{imp}_contaminated_fit"] = err(Te_all)
                        mrow[f"imp_rmse_{imp}_clean_fit"] = err(Te_cln)
                except Exception as e:
                    log.append(f"{cond} imputer {imp}: {e}")
            mech_rows.append(mrow)

            # -------- arms (cell arm applies the same fitted cell rule to the test set)
            arms = {"none": (X_tr, keep_all, "all", X_te),
                    "itd": (X_tr, None, "itd", X_te),
                    "dti": (X_tr, np.setdiff1d(keep_all, dti_drop), "refit", X_te),
                    "cell": (X_cell, keep_all, "refit", X_te_cell)}
            if outl.startswith("gross"):
                arms["oracle_row"] = (X_tr, np.where(~orow)[0], "refit", X_te)
                arms["oracle_cell"] = (X_ocell, keep_all, "refit", X_te)
            for arm, (Xa, keep, fit_mode, Xt) in arms.items():
                for imp in ["mean", "iter", "native"]:
                    if imp == "native" and arm == "itd":
                        continue
                    fams = [f for f in FAMILIES if imp != "native" or f in NATIVE]
                    kp = (np.setdiff1d(keep_all, imputers[(imp, "itd_drop")])
                          if fit_mode == "itd" and (imp, "itd_drop") in imputers else keep)
                    if kp is None:
                        continue
                    Xf, yf = Xa[kp], y_tr[kp]
                    wiped = len(np.unique(yf)) < K
                    fitted = {}
                    for fam in fams:
                        ind = fam not in NO_INDICATOR
                        try:
                            if imp == "native":
                                imputer = None
                            elif fit_mode in ("all", "itd"):          # itd: imputer fitted before removal
                                imputer = imputers[(imp, "all", ind)]
                            else:
                                if ind not in fitted:
                                    fitted[ind] = make_imputer(imp, p, seed, indicator=ind).fit(Xf)
                                imputer = fitted[ind]
                            ba, acc, extra = fit_eval(Xf, yf, Xt, y_te, imputer, fam, seed)
                        except Exception as e:
                            log.append(f"{cond} {arm}/{imp}/{fam}: {e}")
                            continue
                        rows.append(dict(**common, arm=arm, imputer=imp, family=fam, indicator=ind and imp != "native",
                                         removed=n - len(kp), balanced_accuracy=ba, accuracy=acc, wiped_class=wiped,
                                         **extra))
        result = dict(rows=rows, mech=mech_rows, log=log, seconds=time.time() - t0)
        tmp = part_path.with_suffix(".tmp")
        pd.to_pickle(result, tmp)
        tmp.replace(part_path)
        return name, seed, time.time() - t0, log, None
    except Exception:
        return name, seed, time.time() - t0, log, traceback.format_exc()


def run(args):
    out = Path(args.out)
    parts = out / "parts"
    parts.mkdir(parents=True, exist_ok=True)
    conditions = PRESETS[args.preset]
    datasets = (list(base.load_sklearn_datasets())[: args.max_datasets] if args.source == "sklearn"
                else base.load_openml_cc18(args.max_datasets, args.max_rows, args.max_features))
    jobs, skipped, info = [], 0, []
    for i_ds, (name, X_raw, y_raw) in enumerate(datasets):
        if i_ds < args.start:                       # confirmation runs skip the discovery datasets
            continue
        native_missing = float(X_raw.isna().to_numpy().mean())
        X, y = base.to_numeric(X_raw, y_raw)
        info.append(dict(dataset=name, n=len(y), p=X.shape[1], classes=len(np.unique(y)),
                         native_missing_share=native_missing))
        if len(np.unique(y)) < 2 or len(y) < 100:
            continue
        for seed in range(args.seeds):
            part = parts / f"{base.safe_name(name)}__seed{seed}.pkl"
            if part.exists():
                skipped += 1
                continue
            jobs.append((name, X, y, seed, part))
        print(f"queued {name}: n={len(y)} p={X.shape[1]} classes={len(np.unique(y))} "
              f"native missing={native_missing:.1%}")
    pd.DataFrame(info).to_csv(out / "datasets.csv", index=False)
    jobs.sort(key=lambda j: -len(j[2]) * j[1].shape[1])
    print(f"\n{len(conditions)} conditions, {len(jobs)} jobs to run, {skipped} already done. "
          f"Workers: {args.n_jobs}\n")
    t0 = time.time()
    with parallel_config(backend="loky", inner_max_num_threads=1):
        results = Parallel(n_jobs=args.n_jobs, return_as="generator_unordered")(
            delayed(run_job)(n, X, y, s, conditions, p) for n, X, y, s, p in jobs)
        with open(out / "failures.log", "a", encoding="utf-8") as flog:
            for i, (name, seed, secs, log, err) in enumerate(results, 1):
                print(f"[{i}/{len(jobs)}] {name} seed={seed} {'FAILED' if err else 'ok'} "
                      f"({secs:.0f}s, elapsed {(time.time() - t0) / 60:.1f} min)")
                for line in log:
                    flog.write(f"{name} seed={seed}: {line}\n")
                if err:
                    flog.write(f"{name} seed={seed}: JOB FAILED\n{err}\n")
                flog.flush()
    print(f"\nDone. Now run:  python analyze_m1.py {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["openml", "sklearn"], default="openml")
    ap.add_argument("--preset", choices=list(PRESETS), default="full")
    ap.add_argument("--max-datasets", type=int, default=20)
    ap.add_argument("--start", type=int, default=0,
                    help="skip the first START eligible datasets (confirmation: --max-datasets 40 --start 20)")
    ap.add_argument("--max-rows", type=int, default=2000)
    ap.add_argument("--max-features", type=int, default=200)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--n-jobs", type=int, default=10)
    ap.add_argument("--out", default="results_m1b")
    run(ap.parse_args())
