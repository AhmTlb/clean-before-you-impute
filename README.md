# Clean Before You Impute

Code, pre-specified protocols and per-run results for the paper
**"Clean Before You Impute: Outliers Corrupt Iterative Imputation in Incomplete Tabular Data."**

> Archived version: DOI `10.5281/zenodo.23911674` (added after the first Zenodo release)

## What is here

| Folder | Contents |
|---|---|
| `code/` | Experiment and analysis scripts (Python) |
| `protocols/` | The written protocol of each stage (hypotheses and decision criteria fixed before the run) |
| `results/` | Per-run results as compressed CSV and the summary tables produced by the analysis scripts |
| `figures/` | Figures of the paper (PDF and 300 dpi PNG) |

The datasets are **not** redistributed: they are downloaded from OpenML (benchmark suite 99, OpenML-CC18) by the scripts.
The protocols are written in Arabic (the authors' working language); every hypothesis and decision rule they contain is restated in English in the paper.

## Stages, scripts and protocols

| Stage | Datasets (CC18 suite order) | Run | Analyse | Protocol |
|---|---|---|---|---|
| 1 exploration | 1–20 | `missing_experiment_v1.py` | `analyze_m1.py` | `PROTOCOL_m1.md` |
| 1b revised exploration | 1–20 | `missing_experiment_v2.py` | `analyze_m1.py` | `PROTOCOL_m1b.md` |
| 2 confirmation | 21–40 | `missing_experiment_v2.py` | `analyze_m2.py` | `PROTOCOL_m2.md` |
| 3 independent replication | all eligible after 40 (19) | `missing_experiment_v2.py` | `analyze_m2.py` | `PROTOCOL_m3.md` |
| 4 robustness across imputers | 21 onwards (39) | `missing_experiment_v3.py` | `analyze_m4.py`, `analyze_m5_absolute.py` | `PROTOCOL_m4.md` |
| Decision-rule check (Section 4.8) | 21 onwards (39) | `missing_experiment_v2.py` | `analyze_m2.py` with metric `ba_prior` / `auc_macro` | `PROTOCOL_m_ba_check.md` |

`overlap_experiment.py` (data loading) and `experiment_v2.py`–`experiment_v4.py` (shared helpers) come from the companion study *Tune Before You Clean*.

## Installation

Python 3.10 or later.

```bash
pip install -r requirements.txt
```

## Reproducing the results

All commands are run from `code/`. Each run is resumable: finished (dataset, seed) jobs are stored in `<out>/parts/` and skipped on restart.

```bash
# quick offline check
python missing_experiment_v2.py --source sklearn --max-datasets 1 --seeds 1 --n-jobs 1 --preset smoke --out m_smoke

# Stage 1 and 1b (discovery, datasets 1-20)
python missing_experiment_v1.py --source openml --max-datasets 20 --seeds 3 --n-jobs 10 --out results_m1
python analyze_m1.py results_m1
python missing_experiment_v2.py --source openml --max-datasets 20 --seeds 3 --n-jobs 10 --out results_m1b
python analyze_m1.py results_m1b
# Stage 2 (confirmation, datasets 21-40)
python missing_experiment_v2.py --source openml --max-datasets 40 --start 20 --seeds 3 --n-jobs 10 --out results_m2
python analyze_m2.py results_m2
# Stage 3 (independent replication, datasets after 40)
python missing_experiment_v2.py --source openml --max-datasets 72 --start 40 --seeds 3 --n-jobs 10 --out results_m3
python analyze_m2.py results_m3
python analyze_m2.py results_m2 results_m3            # pooled effect sizes
# Stage 4 (robustness across imputers)
python missing_experiment_v3.py --source openml --preset robust --max-datasets 72 --start 20 --seeds 3 --n-jobs 10 --imputers mean,iter,knn,et --arms none,itd,dti,oracle_row --out results_m4
python analyze_m4.py results_m4
python analyze_m5_absolute.py results_m2 results_m3
# Decision-rule check (Section 4.8)
python missing_experiment_v2.py --source openml --max-datasets 40 --start 20 --seeds 3 --n-jobs 10 --out results_m2b
python missing_experiment_v2.py --source openml --max-datasets 72 --start 40 --seeds 3 --n-jobs 10 --out results_m3b
python analyze_m2.py results_m2b results_m3b ba_prior
python analyze_m2.py results_m2b results_m3b auc_macro
# Figures
python make_figures_p2.py
```

Rows are capped at 2,000 per dataset (fixed stratified subsample). To export the per-run results to CSV:

```bash
python export_results.py --dest ../results --only results_m1 results_m1b results_m2 results_m3 results_m4 results_m2b results_m3b
```

## License

Code: MIT (see `LICENSE`). Results and figures: CC BY 4.0.

## Citation

See `CITATION.cff`.
