# Paper 2: confirmatory test on held-out datasets

Datasets: 20 | seeds: 3 | primary conditions: gross|MCAR|0.1, gross|MCAR|0.3, gross|MAR|0.1, gross|MAR|0.3, gross|MNAR|0.1, gross|MNAR|0.3

## Primary hypotheses (one-sided Wilcoxon over datasets, Holm over 7 tests)

| hypothesis                                        | family       |   n |   mean |   median |   share_positive |      p |   p_holm | supported   |
|:--------------------------------------------------|:-------------|----:|-------:|---------:|-----------------:|-------:|---------:|:------------|
| H1 order: dti - itd (iterative)                   | LogReg       |  20 | 0.5034 |   0.363  |             0.65 | 0.022  |   0.0655 | False       |
| H1 order: dti - itd (iterative)                   | KNN          |  20 | 1.003  |   0.5323 |             0.85 | 0.0014 |   0.0095 | True        |
| H1 order: dti - itd (iterative)                   | RandomForest |  20 | 0.4232 |   0.3947 |             0.7  | 0.012  |   0.0599 | False       |
| H1 order: dti - itd (iterative)                   | HistGB       |  20 | 0.3399 |   0.1974 |             0.7  | 0.02   |   0.0655 | False       |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | RandomForest |  20 | 0.4665 |   0.3624 |             0.7  | 0.0164 |   0.0655 | False       |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | HistGB       |  20 | 0.0882 |   0.2077 |             0.55 | 0.4062 |   0.4062 | False       |
| H3 propagation: log RMSE ratio (iterative)        | -            |  20 | 0.0754 |   0.0778 |             0.8  | 0.0086 |   0.0515 | False       |

- **H1: 1 of 4 tests supported**
- **H2: 0 of 2 tests supported**
- **H3: 0 of 1 tests supported**

## Secondary contrasts (descriptive, uncorrected)

| contrast                             | outliers   | family       |   n |   mean |   share_positive |   p_two_sided |
|:-------------------------------------|:-----------|:-------------|----:|-------:|-----------------:|--------------:|
| order with mean imputation           | symmetric  | LogReg       |  20 | -0.006 |             0.5  |         0.756 |
| oracle_row - itd (iterative)         | symmetric  | LogReg       |  20 |  0.669 |             0.75 |         0.008 |
| cell - dti (iterative)               | symmetric  | LogReg       |  20 |  0.376 |             0.55 |         0.812 |
| cell - dti (mean)                    | symmetric  | LogReg       |  20 |  0.255 |             0.45 |         0.812 |
| oracle_cell - oracle_row (iterative) | symmetric  | LogReg       |  20 | -0.039 |             0.45 |         0.841 |
| order with mean imputation           | one-sided  | LogReg       |  20 | -0.051 |             0.5  |         0.522 |
| oracle_row - itd (iterative)         | one-sided  | LogReg       |  20 |  0.956 |             0.8  |         0.008 |
| cell - dti (iterative)               | one-sided  | LogReg       |  20 |  0.719 |             0.6  |         0.216 |
| cell - dti (mean)                    | one-sided  | LogReg       |  20 |  0.4   |             0.5  |         0.898 |
| oracle_cell - oracle_row (iterative) | one-sided  | LogReg       |  20 | -0.03  |             0.45 |         0.784 |
| order with mean imputation           | symmetric  | KNN          |  20 |  0.193 |             0.55 |         0.869 |
| oracle_row - itd (iterative)         | symmetric  | KNN          |  20 |  1.409 |             0.9  |         0     |
| cell - dti (iterative)               | symmetric  | KNN          |  20 | -0.039 |             0.5  |         0.985 |
| cell - dti (mean)                    | symmetric  | KNN          |  20 | -0.274 |             0.4  |         0.674 |
| oracle_cell - oracle_row (iterative) | symmetric  | KNN          |  20 |  0.307 |             0.55 |         0.294 |
| order with mean imputation           | one-sided  | KNN          |  20 | -0.428 |             0.35 |         0.123 |
| oracle_row - itd (iterative)         | one-sided  | KNN          |  20 |  1.635 |             0.75 |         0.001 |
| cell - dti (iterative)               | one-sided  | KNN          |  20 | -0.167 |             0.4  |         0.596 |
| cell - dti (mean)                    | one-sided  | KNN          |  20 |  0.017 |             0.5  |         0.869 |
| oracle_cell - oracle_row (iterative) | one-sided  | KNN          |  20 | -0.028 |             0.45 |         0.956 |
| order with mean imputation           | symmetric  | RandomForest |  20 |  0.024 |             0.5  |         0.729 |
| oracle_row - itd (iterative)         | symmetric  | RandomForest |  20 |  0.566 |             0.7  |         0.004 |
| cell - dti (iterative)               | symmetric  | RandomForest |  20 | -0.724 |             0.4  |         0.154 |
| cell - dti (mean)                    | symmetric  | RandomForest |  20 | -0.505 |             0.5  |         0.216 |
| oracle_cell - oracle_row (iterative) | symmetric  | RandomForest |  20 |  0.073 |             0.6  |         0.475 |
| order with mean imputation           | one-sided  | RandomForest |  20 | -0.122 |             0.35 |         0.231 |
| oracle_row - itd (iterative)         | one-sided  | RandomForest |  20 |  1.267 |             0.95 |         0     |
| cell - dti (iterative)               | one-sided  | RandomForest |  20 | -0.629 |             0.45 |         0.475 |
| cell - dti (mean)                    | one-sided  | RandomForest |  20 | -0.174 |             0.55 |         0.409 |
| oracle_cell - oracle_row (iterative) | one-sided  | RandomForest |  20 |  0.113 |             0.45 |         0.927 |
| oracle_row gain (iter)               | symmetric  | RandomForest |  20 |  0.749 |             0.8  |         0.001 |
| oracle_row gain (mean)               | symmetric  | RandomForest |  20 | -0.011 |             0.4  |         0.674 |
| oracle_row gain (native)             | symmetric  | RandomForest |  20 |  0.178 |             0.55 |         0.261 |
| order with mean imputation           | symmetric  | HistGB       |  20 |  0.02  |             0.6  |         0.368 |
| oracle_row - itd (iterative)         | symmetric  | HistGB       |  20 |  0.746 |             0.85 |         0     |
| cell - dti (iterative)               | symmetric  | HistGB       |  20 | -0.262 |             0.5  |         0.956 |
| cell - dti (mean)                    | symmetric  | HistGB       |  20 | -0.401 |             0.45 |         0.784 |
| oracle_cell - oracle_row (iterative) | symmetric  | HistGB       |  20 |  0.131 |             0.65 |         0.216 |
| order with mean imputation           | one-sided  | HistGB       |  20 | -0.128 |             0.65 |         0.927 |
| oracle_row - itd (iterative)         | one-sided  | HistGB       |  20 |  0.84  |             0.8  |         0.009 |
| cell - dti (iterative)               | one-sided  | HistGB       |  20 | -0.595 |             0.4  |         0.154 |
| cell - dti (mean)                    | one-sided  | HistGB       |  20 | -0.614 |             0.45 |         0.216 |
| oracle_cell - oracle_row (iterative) | one-sided  | HistGB       |  20 | -0.129 |             0.55 |         0.927 |
| oracle_row gain (iter)               | symmetric  | HistGB       |  20 |  0.62  |             0.7  |         0.008 |
| oracle_row gain (mean)               | symmetric  | HistGB       |  20 |  0.093 |             0.65 |         0.452 |
| oracle_row gain (native)             | symmetric  | HistGB       |  20 | -0     |             0.6  |         1     |

## Propagation ratio by condition (median over datasets)

| condition          |   ratio_mean |   ratio_iter |
|:-------------------|-------------:|-------------:|
| gross_pos|MAR|0.3  |        0.992 |        1.051 |
| gross_pos|MCAR|0.3 |        1.012 |        1.133 |
| gross_pos|MNAR|0.3 |        0.938 |        1.033 |
| gross|MAR|0.1      |        1.001 |        1.103 |
| gross|MAR|0.3      |        1     |        1.059 |
| gross|MCAR|0.1     |        1.001 |        1.199 |
| gross|MCAR|0.3     |        1.001 |        1.247 |
| gross|MNAR|0.1     |        0.999 |        1.042 |
| gross|MNAR|0.3     |        0.998 |        1.053 |
