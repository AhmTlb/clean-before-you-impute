# Results

Fill this folder by running, from `code/`:

    python export_results.py --dest ../results --only results_m1 results_m1b results_m2 results_m3 results_m4 results_m2b results_m3b

One sub-folder per run folder. Each contains one compressed CSV per record type (`rows.csv.gz` for the
downstream scores, `mech.csv.gz` for the imputation-error and masking measures) and the summary tables
(`summary_*.md`, `*.csv`) produced by the analysis scripts. Balanced accuracy and ROC AUC are stored
as fractions; the paper reports points (x100).
