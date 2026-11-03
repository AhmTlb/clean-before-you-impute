# Paper 2: confirmatory test on held-out datasets (results_m2b + results_m3b)

Datasets: 39 | seeds: 3 | primary conditions: gross|MCAR|0.1, gross|MCAR|0.3, gross|MAR|0.1, gross|MAR|0.3, gross|MNAR|0.1, gross|MNAR|0.3

## Primary hypotheses (one-sided Wilcoxon over datasets, Holm over 7 tests)

| hypothesis                                        | family       |   n |   mean | ci95         |   median |   share_positive |      p |   p_holm | supported   |
|:--------------------------------------------------|:-------------|----:|-------:|:-------------|---------:|-----------------:|-------:|---------:|:------------|
| H1 order: dti - itd (iterative)                   | LogReg       |  39 | 0.4602 | [0.27, 0.68] |   0.3922 |           0.7436 | 0      |   0.0001 | True        |
| H1 order: dti - itd (iterative)                   | KNN          |  39 | 0.8402 | [0.47, 1.24] |   0.8066 |           0.7692 | 0      |   0.0002 | True        |
| H1 order: dti - itd (iterative)                   | RandomForest |  39 | 0.4804 | [0.24, 0.72] |   0.3985 |           0.7949 | 0.0001 |   0.0003 | True        |
| H1 order: dti - itd (iterative)                   | HistGB       |  39 | 0.4187 | [0.20, 0.63] |   0.4248 |           0.7949 | 0.0002 |   0.0003 | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | RandomForest |  39 | 0.493  | [0.26, 0.72] |   0.5907 |           0.7436 | 0.0001 |   0.0003 | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | HistGB       |  39 | 0.4694 | [0.25, 0.71] |   0.3223 |           0.7949 | 0      |   0.0002 | True        |
| H3 propagation: log RMSE ratio (iterative)        | -            |  39 | 0.1046 | [0.05, 0.16] |   0.0878 |           0.8718 | 0      |   0      | True        |

- **H1: 4 of 4 tests supported**
- **H2: 2 of 2 tests supported**
- **H3: 1 of 1 tests supported**

## Secondary contrasts (descriptive, uncorrected)

| contrast                             | outliers   | family       |   n |   mean |   share_positive |   p_two_sided |
|:-------------------------------------|:-----------|:-------------|----:|-------:|-----------------:|--------------:|
| order with mean imputation           | symmetric  | LogReg       |  39 |  0.015 |            0.538 |         0.809 |
| oracle_row - itd (iterative)         | symmetric  | LogReg       |  39 |  0.692 |            0.846 |         0     |
| cell - dti (iterative)               | symmetric  | LogReg       |  39 |  0.791 |            0.615 |         0.014 |
| cell - dti (mean)                    | symmetric  | LogReg       |  39 |  0.641 |            0.564 |         0.117 |
| oracle_cell - oracle_row (iterative) | symmetric  | LogReg       |  39 |  0.313 |            0.718 |         0     |
| order with mean imputation           | one-sided  | LogReg       |  39 | -0.021 |            0.385 |         0.38  |
| oracle_row - itd (iterative)         | one-sided  | LogReg       |  39 |  0.96  |            0.718 |         0.001 |
| cell - dti (iterative)               | one-sided  | LogReg       |  39 |  0.655 |            0.615 |         0.027 |
| cell - dti (mean)                    | one-sided  | LogReg       |  39 |  0.599 |            0.513 |         0.154 |
| oracle_cell - oracle_row (iterative) | one-sided  | LogReg       |  39 |  0.469 |            0.718 |         0.001 |
| order with mean imputation           | symmetric  | KNN          |  39 |  0.05  |            0.385 |         0.715 |
| oracle_row - itd (iterative)         | symmetric  | KNN          |  39 |  0.838 |            0.846 |         0     |
| cell - dti (iterative)               | symmetric  | KNN          |  39 | -0.392 |            0.462 |         0.259 |
| cell - dti (mean)                    | symmetric  | KNN          |  39 | -0.347 |            0.436 |         0.219 |
| oracle_cell - oracle_row (iterative) | symmetric  | KNN          |  39 |  0.148 |            0.564 |         0.127 |
| order with mean imputation           | one-sided  | KNN          |  39 | -0.559 |            0.231 |         0.001 |
| oracle_row - itd (iterative)         | one-sided  | KNN          |  39 |  1.155 |            0.667 |         0.001 |
| cell - dti (iterative)               | one-sided  | KNN          |  39 |  0.146 |            0.41  |         0.799 |
| cell - dti (mean)                    | one-sided  | KNN          |  39 | -0.368 |            0.436 |         0.265 |
| oracle_cell - oracle_row (iterative) | one-sided  | KNN          |  39 |  0.405 |            0.641 |         0.004 |
| order with mean imputation           | symmetric  | RandomForest |  39 | -0.029 |            0.513 |         0.82  |
| oracle_row - itd (iterative)         | symmetric  | RandomForest |  39 |  0.492 |            0.795 |         0     |
| cell - dti (iterative)               | symmetric  | RandomForest |  39 | -0.144 |            0.564 |         0.918 |
| cell - dti (mean)                    | symmetric  | RandomForest |  39 | -0.118 |            0.59  |         0.512 |
| oracle_cell - oracle_row (iterative) | symmetric  | RandomForest |  39 |  0.238 |            0.667 |         0.007 |
| order with mean imputation           | one-sided  | RandomForest |  39 | -0.138 |            0.487 |         0.521 |
| oracle_row - itd (iterative)         | one-sided  | RandomForest |  39 |  1.127 |            0.897 |         0     |
| cell - dti (iterative)               | one-sided  | RandomForest |  39 | -0.129 |            0.59  |         0.777 |
| cell - dti (mean)                    | one-sided  | RandomForest |  39 | -0.228 |            0.436 |         0.485 |
| oracle_cell - oracle_row (iterative) | one-sided  | RandomForest |  39 |  0.253 |            0.59  |         0.049 |
| oracle_row gain (iter)               | symmetric  | RandomForest |  39 |  0.134 |            0.564 |         0.309 |
| oracle_row gain (mean)               | symmetric  | RandomForest |  39 | -0.273 |            0.359 |         0.058 |
| oracle_row gain (native)             | symmetric  | RandomForest |  39 | -0.285 |            0.256 |         0.002 |
| order with mean imputation           | symmetric  | HistGB       |  39 |  0.047 |            0.513 |         0.38  |
| oracle_row - itd (iterative)         | symmetric  | HistGB       |  39 |  0.673 |            0.769 |         0     |
| cell - dti (iterative)               | symmetric  | HistGB       |  39 | -0.138 |            0.513 |         0.788 |
| cell - dti (mean)                    | symmetric  | HistGB       |  39 | -0.222 |            0.564 |         0.896 |
| oracle_cell - oracle_row (iterative) | symmetric  | HistGB       |  39 |  0.24  |            0.744 |         0.009 |
| order with mean imputation           | one-sided  | HistGB       |  39 |  0.088 |            0.538 |         0.464 |
| oracle_row - itd (iterative)         | one-sided  | HistGB       |  39 |  1.332 |            0.872 |         0     |
| cell - dti (iterative)               | one-sided  | HistGB       |  39 | -0.15  |            0.564 |         0.852 |
| cell - dti (mean)                    | one-sided  | HistGB       |  39 | -0.084 |            0.513 |         0.874 |
| oracle_cell - oracle_row (iterative) | one-sided  | HistGB       |  39 |  0.137 |            0.641 |         0.225 |
| oracle_row gain (iter)               | symmetric  | HistGB       |  39 |  0.69  |            0.846 |         0     |
| oracle_row gain (mean)               | symmetric  | HistGB       |  39 | -0.085 |            0.359 |         0.185 |
| oracle_row gain (native)             | symmetric  | HistGB       |  39 |  0.157 |            0.564 |         0.085 |

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
