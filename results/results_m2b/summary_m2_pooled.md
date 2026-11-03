# Paper 2: confirmatory test on held-out datasets (results_m2b + results_m3b)

Datasets: 39 | seeds: 3 | primary conditions: gross|MCAR|0.1, gross|MCAR|0.3, gross|MAR|0.1, gross|MAR|0.3, gross|MNAR|0.1, gross|MNAR|0.3

## Primary hypotheses (one-sided Wilcoxon over datasets, Holm over 7 tests)

| hypothesis                                        | family       |   n |   mean | ci95          |   median |   share_positive |      p |   p_holm | supported   |
|:--------------------------------------------------|:-------------|----:|-------:|:--------------|---------:|-----------------:|-------:|---------:|:------------|
| H1 order: dti - itd (iterative)                   | LogReg       |  39 | 0.5014 | [0.17, 0.88]  |   0.3283 |           0.6154 | 0.0063 |   0.0126 | True        |
| H1 order: dti - itd (iterative)                   | KNN          |  39 | 0.8307 | [0.46, 1.28]  |   0.519  |           0.8462 | 0      |   0      | True        |
| H1 order: dti - itd (iterative)                   | RandomForest |  39 | 0.5038 | [0.23, 0.79]  |   0.3473 |           0.7179 | 0.0004 |   0.0022 | True        |
| H1 order: dti - itd (iterative)                   | HistGB       |  39 | 0.3577 | [0.10, 0.59]  |   0.3424 |           0.6923 | 0.0019 |   0.0056 | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | RandomForest |  39 | 0.541  | [0.26, 0.84]  |   0.4053 |           0.7179 | 0.0007 |   0.0028 | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | HistGB       |  39 | 0.2877 | [-0.03, 0.62] |   0.2777 |           0.641  | 0.0375 |   0.0375 | True        |
| H3 propagation: log RMSE ratio (iterative)        | -            |  39 | 0.1046 | [0.05, 0.16]  |   0.0878 |           0.8718 | 0      |   0      | True        |

- **H1: 4 of 4 tests supported**
- **H2: 2 of 2 tests supported**
- **H3: 1 of 1 tests supported**

## Secondary contrasts (descriptive, uncorrected)

| contrast                             | outliers   | family       |   n |   mean |   share_positive |   p_two_sided |
|:-------------------------------------|:-----------|:-------------|----:|-------:|-----------------:|--------------:|
| order with mean imputation           | symmetric  | LogReg       |  39 | -0.001 |            0.487 |         0.811 |
| oracle_row - itd (iterative)         | symmetric  | LogReg       |  39 |  0.632 |            0.718 |         0.001 |
| cell - dti (iterative)               | symmetric  | LogReg       |  39 |  0.491 |            0.513 |         0.395 |
| cell - dti (mean)                    | symmetric  | LogReg       |  39 |  0.438 |            0.538 |         0.548 |
| oracle_cell - oracle_row (iterative) | symmetric  | LogReg       |  39 |  0.068 |            0.538 |         0.403 |
| order with mean imputation           | one-sided  | LogReg       |  39 | -0.005 |            0.564 |         0.95  |
| oracle_row - itd (iterative)         | one-sided  | LogReg       |  39 |  0.709 |            0.744 |         0.002 |
| cell - dti (iterative)               | one-sided  | LogReg       |  39 |  0.756 |            0.667 |         0.056 |
| cell - dti (mean)                    | one-sided  | LogReg       |  39 |  0.292 |            0.564 |         0.644 |
| oracle_cell - oracle_row (iterative) | one-sided  | LogReg       |  39 |  0.146 |            0.564 |         0.277 |
| order with mean imputation           | symmetric  | KNN          |  39 |  0.155 |            0.513 |         0.704 |
| oracle_row - itd (iterative)         | symmetric  | KNN          |  39 |  0.985 |            0.897 |         0     |
| cell - dti (iterative)               | symmetric  | KNN          |  39 | -0.183 |            0.513 |         0.95  |
| cell - dti (mean)                    | symmetric  | KNN          |  39 | -0.335 |            0.41  |         0.336 |
| oracle_cell - oracle_row (iterative) | symmetric  | KNN          |  39 |  0.196 |            0.59  |         0.158 |
| order with mean imputation           | one-sided  | KNN          |  39 | -0.535 |            0.333 |         0.005 |
| oracle_row - itd (iterative)         | one-sided  | KNN          |  39 |  1.181 |            0.692 |         0.001 |
| cell - dti (iterative)               | one-sided  | KNN          |  39 | -0.234 |            0.436 |         0.443 |
| cell - dti (mean)                    | one-sided  | KNN          |  39 | -0.064 |            0.513 |         0.972 |
| oracle_cell - oracle_row (iterative) | one-sided  | KNN          |  39 |  0.201 |            0.59  |         0.068 |
| order with mean imputation           | symmetric  | RandomForest |  39 |  0.032 |            0.513 |         0.53  |
| oracle_row - itd (iterative)         | symmetric  | RandomForest |  39 |  0.685 |            0.744 |         0     |
| cell - dti (iterative)               | symmetric  | RandomForest |  39 | -0.426 |            0.462 |         0.343 |
| cell - dti (mean)                    | symmetric  | RandomForest |  39 | -0.447 |            0.487 |         0.286 |
| oracle_cell - oracle_row (iterative) | symmetric  | RandomForest |  39 |  0.049 |            0.564 |         0.468 |
| order with mean imputation           | one-sided  | RandomForest |  39 | -0.028 |            0.385 |         0.35  |
| oracle_row - itd (iterative)         | one-sided  | RandomForest |  39 |  1.012 |            0.821 |         0     |
| cell - dti (iterative)               | one-sided  | RandomForest |  39 | -0.159 |            0.615 |         0.435 |
| cell - dti (mean)                    | one-sided  | RandomForest |  39 | -0.118 |            0.538 |         0.464 |
| oracle_cell - oracle_row (iterative) | one-sided  | RandomForest |  39 |  0.209 |            0.538 |         0.302 |
| oracle_row gain (iter)               | symmetric  | RandomForest |  39 |  0.839 |            0.795 |         0     |
| oracle_row gain (mean)               | symmetric  | RandomForest |  39 |  0.002 |            0.462 |         0.664 |
| oracle_row gain (native)             | symmetric  | RandomForest |  39 |  0.188 |            0.538 |         0.162 |
| order with mean imputation           | symmetric  | HistGB       |  39 |  0.034 |            0.59  |         0.315 |
| oracle_row - itd (iterative)         | symmetric  | HistGB       |  39 |  0.681 |            0.795 |         0     |
| cell - dti (iterative)               | symmetric  | HistGB       |  39 | -0.272 |            0.487 |         0.82  |
| cell - dti (mean)                    | symmetric  | HistGB       |  39 | -0.44  |            0.513 |         0.38  |
| oracle_cell - oracle_row (iterative) | symmetric  | HistGB       |  39 |  0.091 |            0.615 |         0.162 |
| order with mean imputation           | one-sided  | HistGB       |  39 | -0.145 |            0.538 |         0.388 |
| oracle_row - itd (iterative)         | one-sided  | HistGB       |  39 |  1.032 |            0.821 |         0     |
| cell - dti (iterative)               | one-sided  | HistGB       |  39 | -0.418 |            0.462 |         0.204 |
| cell - dti (mean)                    | one-sided  | HistGB       |  39 | -0.408 |            0.513 |         0.427 |
| oracle_cell - oracle_row (iterative) | one-sided  | HistGB       |  39 |  0.048 |            0.59  |         0.315 |
| oracle_row gain (iter)               | symmetric  | HistGB       |  39 |  0.721 |            0.769 |         0     |
| oracle_row gain (mean)               | symmetric  | HistGB       |  39 |  0.188 |            0.564 |         0.176 |
| oracle_row gain (native)             | symmetric  | HistGB       |  39 |  0.119 |            0.564 |         0.468 |

## Propagation ratio by condition (median over datasets)

| condition          |   ratio_mean |   ratio_iter |
|:-------------------|-------------:|-------------:|
| gross_pos|MAR|0.3  |        0.998 |        1.091 |
| gross_pos|MCAR|0.3 |        1.013 |        1.129 |
| gross_pos|MNAR|0.3 |        0.924 |        1.033 |
| gross|MAR|0.1      |        1.001 |        1.12  |
| gross|MAR|0.3      |        1     |        1.095 |
| gross|MCAR|0.1     |        1.001 |        1.16  |
| gross|MCAR|0.3     |        1.001 |        1.182 |
| gross|MNAR|0.1     |        0.999 |        1.05  |
| gross|MNAR|0.3     |        0.998 |        1.066 |
