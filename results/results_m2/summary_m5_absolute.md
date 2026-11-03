# Absolute balanced accuracy of complete pipelines (results_m2 + results_m3)

Six primary conditions; difference to mean imputation without cleaning. Descriptive.

| family       | pipeline      |   datasets |   mean_BA |   diff_vs_mean_none | ci95           |   share_better |
|:-------------|:--------------|-----------:|----------:|--------------------:|:---------------|---------------:|
| LogReg       | mean + none   |         39 |    58.611 |               0     | [+0.00, +0.00] |          0     |
| LogReg       | mean + dti    |         39 |    63.316 |               4.705 | [+3.38, +6.21] |          0.974 |
| LogReg       | iter + none   |         39 |    58.814 |               0.203 | [+0.02, +0.39] |          0.667 |
| LogReg       | iter + itd    |         39 |    63.303 |               4.692 | [+3.45, +6.09] |          0.974 |
| LogReg       | iter + dti    |         39 |    63.804 |               5.193 | [+3.86, +6.67] |          0.974 |
| KNN          | mean + none   |         39 |    62.785 |               0     | [+0.00, +0.00] |          0     |
| KNN          | mean + dti    |         39 |    62.963 |               0.178 | [-0.25, +0.79] |          0.487 |
| KNN          | iter + none   |         39 |    63.689 |               0.904 | [+0.49, +1.39] |          0.744 |
| KNN          | iter + itd    |         39 |    63.646 |               0.861 | [+0.24, +1.60] |          0.718 |
| KNN          | iter + dti    |         39 |    64.477 |               1.691 | [+0.99, +2.49] |          0.821 |
| RandomForest | mean + none   |         39 |    66.56  |               0     | [+0.00, +0.00] |          0     |
| RandomForest | mean + dti    |         39 |    66.58  |               0.02  | [-0.22, +0.27] |          0.41  |
| RandomForest | iter + none   |         39 |    66.473 |              -0.087 | [-0.34, +0.19] |          0.436 |
| RandomForest | iter + itd    |         39 |    66.626 |               0.067 | [-0.25, +0.40] |          0.513 |
| RandomForest | iter + dti    |         39 |    67.13  |               0.57  | [+0.19, +0.97] |          0.641 |
| RandomForest | native + none |         39 |    67.428 |               0.868 | [+0.50, +1.29] |          0.821 |
| RandomForest | native + dti  |         39 |    67.544 |               0.984 | [+0.58, +1.42] |          0.769 |
| HistGB       | mean + none   |         39 |    69.247 |               0     | [+0.00, +0.00] |          0     |
| HistGB       | mean + dti    |         39 |    69.362 |               0.115 | [-0.15, +0.38] |          0.538 |
| HistGB       | iter + none   |         39 |    69.099 |              -0.148 | [-0.47, +0.16] |          0.462 |
| HistGB       | iter + itd    |         39 |    69.139 |              -0.108 | [-0.41, +0.20] |          0.385 |
| HistGB       | iter + dti    |         39 |    69.497 |               0.25  | [-0.03, +0.54] |          0.615 |
| HistGB       | native + none |         39 |    69.296 |               0.049 | [-0.19, +0.29] |          0.513 |
| HistGB       | native + dti  |         39 |    69.407 |               0.16  | [-0.11, +0.45] |          0.538 |
