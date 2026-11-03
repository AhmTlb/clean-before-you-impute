# Paper 2: confirmatory test on held-out datasets (results_m3)

Datasets: 19 | seeds: 3 | primary conditions: gross|MCAR|0.1, gross|MCAR|0.3, gross|MAR|0.1, gross|MAR|0.3, gross|MNAR|0.1, gross|MNAR|0.3

## Primary hypotheses (one-sided Wilcoxon over datasets, Holm over 7 tests)

| hypothesis                                        | family       |   n |   mean | ci95          |   median |   share_positive |      p |   p_holm | supported   |
|:--------------------------------------------------|:-------------|----:|-------:|:--------------|---------:|-----------------:|-------:|---------:|:------------|
| H1 order: dti - itd (iterative)                   | LogReg       |  19 | 0.4993 | [-0.01, 1.19] |   0.0667 |           0.5789 | 0.0978 |   0.0978 | False       |
| H1 order: dti - itd (iterative)                   | KNN          |  19 | 0.6493 | [0.37, 0.92]  |   0.484  |           0.8421 | 0.0002 |   0.0013 | True        |
| H1 order: dti - itd (iterative)                   | RandomForest |  19 | 0.5886 | [0.16, 1.04]  |   0.3473 |           0.7368 | 0.009  |   0.0452 | True        |
| H1 order: dti - itd (iterative)                   | HistGB       |  19 | 0.3763 | [-0.06, 0.76] |   0.5997 |           0.6842 | 0.0273 |   0.0546 | False       |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | RandomForest |  19 | 0.6195 | [0.19, 1.06]  |   0.4053 |           0.7368 | 0.0102 |   0.0452 | True        |
| H2 via imputer: gain(dti|iter) - gain(dti|native) | HistGB       |  19 | 0.4977 | [-0.02, 1.04] |   0.6271 |           0.7368 | 0.018  |   0.0541 | False       |
| H3 propagation: log RMSE ratio (iterative)        | -            |  19 | 0.1354 | [0.08, 0.20]  |   0.1161 |           0.9474 | 0      |   0.0001 | True        |

- **H1: 2 of 4 tests supported**
- **H2: 1 of 2 tests supported**
- **H3: 1 of 1 tests supported**

## Secondary contrasts (descriptive, uncorrected)

| contrast                             | outliers   | family       |   n |   mean |   share_positive |   p_two_sided |
|:-------------------------------------|:-----------|:-------------|----:|-------:|-----------------:|--------------:|
| order with mean imputation           | symmetric  | LogReg       |  19 |  0.004 |            0.474 |         0.777 |
| oracle_row - itd (iterative)         | symmetric  | LogReg       |  19 |  0.593 |            0.684 |         0.055 |
| cell - dti (iterative)               | symmetric  | LogReg       |  19 |  0.611 |            0.474 |         0.395 |
| cell - dti (mean)                    | symmetric  | LogReg       |  19 |  0.63  |            0.632 |         0.258 |
| oracle_cell - oracle_row (iterative) | symmetric  | LogReg       |  19 |  0.181 |            0.632 |         0.123 |
| order with mean imputation           | one-sided  | LogReg       |  19 |  0.043 |            0.632 |         0.49  |
| oracle_row - itd (iterative)         | one-sided  | LogReg       |  19 |  0.449 |            0.684 |         0.113 |
| cell - dti (iterative)               | one-sided  | LogReg       |  19 |  0.796 |            0.737 |         0.123 |
| cell - dti (mean)                    | one-sided  | LogReg       |  19 |  0.178 |            0.632 |         0.623 |
| oracle_cell - oracle_row (iterative) | one-sided  | LogReg       |  19 |  0.331 |            0.684 |         0.182 |
| order with mean imputation           | symmetric  | KNN          |  19 |  0.115 |            0.474 |         0.768 |
| oracle_row - itd (iterative)         | symmetric  | KNN          |  19 |  0.538 |            0.895 |         0.002 |
| cell - dti (iterative)               | symmetric  | KNN          |  19 | -0.335 |            0.526 |         0.891 |
| cell - dti (mean)                    | symmetric  | KNN          |  19 | -0.399 |            0.421 |         0.465 |
| oracle_cell - oracle_row (iterative) | symmetric  | KNN          |  19 |  0.079 |            0.632 |         0.441 |
| order with mean imputation           | one-sided  | KNN          |  19 | -0.646 |            0.316 |         0.014 |
| oracle_row - itd (iterative)         | one-sided  | KNN          |  19 |  0.704 |            0.632 |         0.113 |
| cell - dti (iterative)               | one-sided  | KNN          |  19 | -0.305 |            0.474 |         0.541 |
| cell - dti (mean)                    | one-sided  | KNN          |  19 | -0.149 |            0.526 |         1     |
| oracle_cell - oracle_row (iterative) | one-sided  | KNN          |  19 |  0.442 |            0.737 |         0.011 |
| order with mean imputation           | symmetric  | RandomForest |  19 |  0.04  |            0.526 |         0.623 |
| oracle_row - itd (iterative)         | symmetric  | RandomForest |  19 |  0.81  |            0.789 |         0.003 |
| cell - dti (iterative)               | symmetric  | RandomForest |  19 | -0.112 |            0.526 |         0.86  |
| cell - dti (mean)                    | symmetric  | RandomForest |  19 | -0.386 |            0.474 |         0.744 |
| oracle_cell - oracle_row (iterative) | symmetric  | RandomForest |  19 |  0.023 |            0.526 |         0.768 |
| order with mean imputation           | one-sided  | RandomForest |  19 |  0.071 |            0.421 |         0.984 |
| oracle_row - itd (iterative)         | one-sided  | RandomForest |  19 |  0.744 |            0.684 |         0.035 |
| cell - dti (iterative)               | one-sided  | RandomForest |  19 |  0.335 |            0.789 |         0.087 |
| cell - dti (mean)                    | one-sided  | RandomForest |  19 | -0.058 |            0.526 |         0.845 |
| oracle_cell - oracle_row (iterative) | one-sided  | RandomForest |  19 |  0.311 |            0.632 |         0.113 |
| oracle_row gain (iter)               | symmetric  | RandomForest |  19 |  0.933 |            0.789 |         0.009 |
| oracle_row gain (mean)               | symmetric  | RandomForest |  19 |  0.017 |            0.526 |         0.891 |
| oracle_row gain (native)             | symmetric  | RandomForest |  19 |  0.199 |            0.526 |         0.441 |
| order with mean imputation           | symmetric  | HistGB       |  19 |  0.049 |            0.579 |         0.829 |
| oracle_row - itd (iterative)         | symmetric  | HistGB       |  19 |  0.612 |            0.737 |         0.011 |
| cell - dti (iterative)               | symmetric  | HistGB       |  19 | -0.284 |            0.474 |         0.679 |
| cell - dti (mean)                    | symmetric  | HistGB       |  19 | -0.481 |            0.579 |         0.418 |
| oracle_cell - oracle_row (iterative) | symmetric  | HistGB       |  19 |  0.049 |            0.579 |         0.465 |
| order with mean imputation           | one-sided  | HistGB       |  19 | -0.163 |            0.421 |         0.231 |
| oracle_row - itd (iterative)         | one-sided  | HistGB       |  19 |  1.235 |            0.842 |         0     |
| cell - dti (iterative)               | one-sided  | HistGB       |  19 | -0.232 |            0.526 |         0.623 |
| cell - dti (mean)                    | one-sided  | HistGB       |  19 | -0.191 |            0.579 |         0.953 |
| oracle_cell - oracle_row (iterative) | one-sided  | HistGB       |  19 |  0.235 |            0.632 |         0.156 |
| oracle_row gain (iter)               | symmetric  | HistGB       |  19 |  0.827 |            0.842 |         0.001 |
| oracle_row gain (mean)               | symmetric  | HistGB       |  19 |  0.289 |            0.474 |         0.418 |
| oracle_row gain (native)             | symmetric  | HistGB       |  19 |  0.244 |            0.526 |         0.395 |

## Propagation ratio by condition (median over datasets)

| condition          |   ratio_mean |   ratio_iter |
|:-------------------|-------------:|-------------:|
| gross_pos|MAR|0.3  |        1.011 |        1.12  |
| gross_pos|MCAR|0.3 |        1.014 |        1.123 |
| gross_pos|MNAR|0.3 |        0.918 |        1.048 |
| gross|MAR|0.1      |        0.999 |        1.138 |
| gross|MAR|0.3      |        1     |        1.105 |
| gross|MCAR|0.1     |        1.001 |        1.132 |
| gross|MCAR|0.3     |        1.001 |        1.141 |
| gross|MNAR|0.1     |        0.999 |        1.062 |
| gross|MNAR|0.3     |        0.997 |        1.076 |
