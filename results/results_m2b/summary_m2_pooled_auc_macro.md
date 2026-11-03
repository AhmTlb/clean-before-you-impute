# Paper 2: confirmatory test on held-out datasets (results_m2b + results_m3b)

Datasets: 39 | seeds: 3 | primary conditions: gross|MCAR|0.1, gross|MCAR|0.3, gross|MAR|0.1, gross|MAR|0.3, gross|MNAR|0.1, gross|MNAR|0.3

## Primary hypotheses (one-sided Wilcoxon over datasets, Holm over 7 tests)

| hypothesis                                        | family       |   n |   mean | ci95         |   median |   share_positive |      p |   p_holm | supported   |
|:--------------------------------------------------|:-------------|----:|-------:|:-------------|---------:|-----------------:|-------:|---------:|:------------|
| H1 order: dti - itd (iterative)                   | LogReg       |  39 | 0.4054 | [0.22, 0.62] |   0.1255 |           0.8205 | 0      |   0      | True        |
| H1 order: dti - itd (iterative)                   | KNN          |  39 | 0.6707 | [0.37, 0.99] |   0.4285 |           0.7436 | 0      |   0.0001 | True        |
| H1 order: dti - itd (iterative)                   | RandomForest |  39 | 0.2944 | [0.15, 0.44] |   0.2361 |           0.8462 | 0      |   0.0001 | True        |
| H1 order: dti - itd (iterative)                   | HistGB       |  39 | 0.3091 | [0.14, 0.46] |   0.2331 |           0.7949 | 0      |   0      | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | RandomForest |  39 | 0.2045 | [0.06, 0.35] |   0.1755 |           0.7692 | 0.0039 |   0.0039 | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | HistGB       |  39 | 0.3176 | [0.14, 0.48] |   0.1578 |           0.8462 | 0      |   0      | True        |
| H3 propagation: log RMSE ratio (iterative)        | -            |  39 | 0.1046 | [0.05, 0.16] |   0.0878 |           0.8718 | 0      |   0      | True        |

- **H1: 4 of 4 tests supported**
- **H2: 2 of 2 tests supported**
- **H3: 1 of 1 tests supported**

## Secondary contrasts (descriptive, uncorrected)

| contrast                             | outliers   | family       |   n |   mean |   share_positive |   p_two_sided |
|:-------------------------------------|:-----------|:-------------|----:|-------:|-----------------:|--------------:|
| order with mean imputation           | symmetric  | LogReg       |  39 |  0.043 |            0.667 |         0.037 |
| oracle_row - itd (iterative)         | symmetric  | LogReg       |  39 |  0.51  |            0.821 |         0     |
| cell - dti (iterative)               | symmetric  | LogReg       |  39 |  0.518 |            0.692 |         0.01  |
| cell - dti (mean)                    | symmetric  | LogReg       |  39 |  0.468 |            0.692 |         0.041 |
| oracle_cell - oracle_row (iterative) | symmetric  | LogReg       |  39 |  0.278 |            0.923 |         0     |
| order with mean imputation           | one-sided  | LogReg       |  39 | -0.003 |            0.359 |         0.044 |
| oracle_row - itd (iterative)         | one-sided  | LogReg       |  39 |  0.677 |            0.821 |         0     |
| cell - dti (iterative)               | one-sided  | LogReg       |  39 |  0.661 |            0.744 |         0     |
| cell - dti (mean)                    | one-sided  | LogReg       |  39 |  0.67  |            0.795 |         0     |
| oracle_cell - oracle_row (iterative) | one-sided  | LogReg       |  39 |  0.388 |            0.923 |         0     |
| order with mean imputation           | symmetric  | KNN          |  39 |  0.107 |            0.538 |         0.372 |
| oracle_row - itd (iterative)         | symmetric  | KNN          |  39 |  0.674 |            0.897 |         0     |
| cell - dti (iterative)               | symmetric  | KNN          |  39 | -0.535 |            0.462 |         0.154 |
| cell - dti (mean)                    | symmetric  | KNN          |  39 | -0.566 |            0.359 |         0.033 |
| oracle_cell - oracle_row (iterative) | symmetric  | KNN          |  39 |  0.065 |            0.59  |         0.135 |
| order with mean imputation           | one-sided  | KNN          |  39 | -0.438 |            0.231 |         0.001 |
| oracle_row - itd (iterative)         | one-sided  | KNN          |  39 |  0.777 |            0.692 |         0.002 |
| cell - dti (iterative)               | one-sided  | KNN          |  39 | -0.004 |            0.59  |         0.746 |
| cell - dti (mean)                    | one-sided  | KNN          |  39 | -0.359 |            0.41  |         0.176 |
| oracle_cell - oracle_row (iterative) | one-sided  | KNN          |  39 |  0.296 |            0.692 |         0.009 |
| order with mean imputation           | symmetric  | RandomForest |  39 |  0.064 |            0.718 |         0.016 |
| oracle_row - itd (iterative)         | symmetric  | RandomForest |  39 |  0.345 |            0.872 |         0     |
| cell - dti (iterative)               | symmetric  | RandomForest |  39 | -0.236 |            0.462 |         0.271 |
| cell - dti (mean)                    | symmetric  | RandomForest |  39 | -0.214 |            0.487 |         0.403 |
| oracle_cell - oracle_row (iterative) | symmetric  | RandomForest |  39 |  0.099 |            0.692 |         0.039 |
| order with mean imputation           | one-sided  | RandomForest |  39 | -0.057 |            0.462 |         0.521 |
| oracle_row - itd (iterative)         | one-sided  | RandomForest |  39 |  0.615 |            0.872 |         0     |
| cell - dti (iterative)               | one-sided  | RandomForest |  39 | -0.259 |            0.487 |         0.46  |
| cell - dti (mean)                    | one-sided  | RandomForest |  39 | -0.179 |            0.462 |         0.664 |
| oracle_cell - oracle_row (iterative) | one-sided  | RandomForest |  39 |  0.209 |            0.744 |         0     |
| oracle_row gain (iter)               | symmetric  | RandomForest |  39 |  0.112 |            0.744 |         0.008 |
| oracle_row gain (mean)               | symmetric  | RandomForest |  39 | -0.134 |            0.385 |         0.043 |
| oracle_row gain (native)             | symmetric  | RandomForest |  39 | -0.065 |            0.359 |         0.18  |
| order with mean imputation           | symmetric  | HistGB       |  39 |  0.016 |            0.667 |         0.093 |
| oracle_row - itd (iterative)         | symmetric  | HistGB       |  39 |  0.404 |            0.846 |         0     |
| cell - dti (iterative)               | symmetric  | HistGB       |  39 | -0.112 |            0.59  |         0.972 |
| cell - dti (mean)                    | symmetric  | HistGB       |  39 | -0.139 |            0.615 |         0.664 |
| oracle_cell - oracle_row (iterative) | symmetric  | HistGB       |  39 |  0.213 |            0.846 |         0     |
| order with mean imputation           | one-sided  | HistGB       |  39 | -0.175 |            0.333 |         0.086 |
| oracle_row - itd (iterative)         | one-sided  | HistGB       |  39 |  0.557 |            0.821 |         0     |
| cell - dti (iterative)               | one-sided  | HistGB       |  39 | -0.232 |            0.462 |         0.477 |
| cell - dti (mean)                    | one-sided  | HistGB       |  39 | -0.041 |            0.59  |         0.468 |
| oracle_cell - oracle_row (iterative) | one-sided  | HistGB       |  39 |  0.137 |            0.59  |         0.199 |
| oracle_row gain (iter)               | symmetric  | HistGB       |  39 |  0.41  |            0.718 |         0     |
| oracle_row gain (mean)               | symmetric  | HistGB       |  39 |  0.037 |            0.41  |         0.961 |
| oracle_row gain (native)             | symmetric  | HistGB       |  39 |  0.095 |            0.487 |         0.419 |

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
