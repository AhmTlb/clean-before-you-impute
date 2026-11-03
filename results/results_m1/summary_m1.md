# Paper 2, Stage 1: outliers in incomplete data (exploratory)

Datasets: 20 | seeds: 3 | conditions: 16

Condition = outliers | missingness mechanism | missing rate.

## A1. Propagation: imputation error on clean test cells (robust-SD units)

contaminated_fit = imputer fitted on all training rows; clean_fit = on rows without outliers. ratio > 1 means the outliers degrade the imputation of clean cells.

| condition         |   imp_rmse_mean_contaminated_fit |   imp_rmse_mean_clean_fit |   imp_rmse_iter_contaminated_fit |   imp_rmse_iter_clean_fit |   ratio_mean |   ratio_iter |
|:------------------|---------------------------------:|--------------------------:|---------------------------------:|--------------------------:|-------------:|-------------:|
| gross|MCAR|0.1    |                            5.389 |                     4.577 |                            5.343 |                     4.343 |        1.177 |        1.23  |
| gross|MCAR|0.3    |                           12.786 |                    12.735 |                           12.715 |                    15.04  |        1.004 |        0.845 |
| gross|MAR|0.1     |                            2.741 |                     2.766 |                            2.521 |                     5.474 |        0.991 |        0.461 |
| gross|MAR|0.3     |                            5.533 |                     5.455 |                            5.405 |                     7.134 |        1.014 |        0.758 |
| gross|MNAR|0.1    |                           85.312 |                    85.454 |                           85.094 |                    85.032 |        0.998 |        1.001 |
| gross|MNAR|0.3    |                           52.845 |                    53.219 |                           52.669 |                    52.992 |        0.993 |        0.994 |
| gross|MNARobs|0.3 |                           52.984 |                    52.984 |                           52.746 |                    52.746 |        1     |        1     |

## A2. Masking: Isolation Forest recall of the outlier rows (top k = number of outlier rows)

| condition         |   recall_IF_complete |   recall_IF_medianfill |   recall_IF_mean_imputed |   recall_IF_iter_imputed |
|:------------------|---------------------:|-----------------------:|-------------------------:|-------------------------:|
| gross|complete|0  |                0.984 |                  0.984 |                    0.984 |                    0.984 |
| gross|MCAR|0.1    |                0.985 |                  0.952 |                    0.954 |                    0.963 |
| gross|MCAR|0.3    |                0.984 |                  0.864 |                    0.869 |                    0.918 |
| gross|MAR|0.1     |                0.982 |                  0.975 |                    0.974 |                    0.977 |
| gross|MAR|0.3     |                0.984 |                  0.928 |                    0.93  |                    0.948 |
| gross|MNAR|0.1    |                0.985 |                  0.978 |                    0.979 |                    0.983 |
| gross|MNAR|0.3    |                0.984 |                  0.914 |                    0.918 |                    0.941 |
| gross|MNARobs|0.3 |                0.982 |                  0.033 |                    0.041 |                    0.065 |

## A3. Outlier cells hidden by missingness; cell rule (|modified z| > 3.5)

cell_recall is over outlier cells that are still observed.

| condition         |   outlier_cells_hidden_by_missing |   cell_flagged_share |   cell_precision |   cell_recall |
|:------------------|----------------------------------:|---------------------:|-----------------:|--------------:|
| gross|complete|0  |                             0     |                0.033 |            0.762 |         0.957 |
| gross|MCAR|0.1    |                             0.097 |                0.032 |            0.762 |         0.957 |
| gross|MCAR|0.3    |                             0.297 |                0.032 |            0.752 |         0.953 |
| gross|MAR|0.1     |                             0.061 |                0.031 |            0.773 |         0.959 |
| gross|MAR|0.3     |                             0.201 |                0.032 |            0.772 |         0.958 |
| gross|MNAR|0.1    |                             0.099 |                0.027 |            0.866 |         0.967 |
| gross|MNAR|0.3    |                             0.301 |                0.03  |            0.848 |         0.963 |
| gross|MNARobs|0.3 |                             0.999 |                0.014 |            0.005 |         0.05  |

Share of cells the cell rule flags on outlier-free data (false alarms):

| condition        |   cell_flagged_share |
|:-----------------|---------------------:|
| none|complete|0  |                0.012 |
| none|MCAR|0.1    |                0.012 |
| none|MCAR|0.3    |                0.013 |
| none|MAR|0.1     |                0.012 |
| none|MAR|0.3     |                0.013 |
| none|MNAR|0.1    |                0.008 |
| none|MNAR|0.3    |                0.01  |
| none|MNARobs|0.3 |                0.013 |

## B. Baselines (arm none): iterative / native minus mean imputation, points

### iter - mean

| family       |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:-------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| HistGB       |                  0 |            -0.03 |            -0.56 |            0.14 |           -0.26 |            -0.29 |            -0.67 |                0.47 |                 0 |            0.3  |            0.78 |           0.2  |          -0.01 |            0.12 |           -0.31 |               0.6  |
| KNN          |                  0 |             0.56 |             1.79 |            0.12 |            0.45 |             0.23 |            -0.12 |                2.42 |                 0 |            0.7  |            2.91 |           0.38 |           0.73 |            0.65 |            0.84 |               2.71 |
| LogReg       |                  0 |             0.46 |             0.3  |            0.37 |           -0.2  |            -0.04 |            -0.59 |                1.67 |                 0 |            0.76 |            1.73 |           0.41 |           0.51 |            0.45 |            0.04 |               1.47 |
| RandomForest |                  0 |             0.15 |             0.01 |            0.1  |           -0.18 |             0.06 |            -0.96 |                1.18 |                 0 |            0.7  |            1.55 |           0.26 |           0.49 |            0.24 |            0    |               1.36 |

### native - mean

| family       |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:-------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| HistGB       |                  0 |            -0.05 |            -0    |           -0.03 |            0.14 |             0.29 |             0.96 |                0.69 |                 0 |           -0.01 |           -0.15 |          -0    |          -0.07 |            0.46 |            0.36 |               0.68 |
| RandomForest |                  0 |             0.52 |             0.64 |            0.33 |            0.45 |             0.96 |             1.29 |                1.44 |                 0 |            0.67 |            1.1  |           0.31 |           0.74 |            0.49 |            1.34 |               1.42 |

## C. Gains vs. arm none (same imputer, same family), points

### LogReg / mean

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |               4.91 |             5.06 |             4.76 |            5.42 |            5.03 |             5.03 |             3.59 |               -0.52 |             -0.76 |           -0.71 |           -0.36 |          -0.47 |          -0.38 |           -0.76 |           -0.45 |              -0.16 |
| dti         |               4.91 |             5.13 |             4.6  |            5.41 |            4.97 |             4.99 |             3.51 |               -0.39 |             -0.76 |           -0.72 |           -0.44 |          -0.54 |          -0.39 |           -0.53 |           -0.3  |              -0.27 |
| cell        |               2.25 |             3.54 |             3.55 |            3.65 |            3.84 |             4.56 |             2.9  |               -1.02 |             -2.82 |           -2.22 |           -1.99 |          -2.07 |          -1.8  |           -0.44 |           -0.68 |              -0.94 |
| oracle_row  |               4.9  |             5.08 |             4.88 |            5.55 |            5.15 |             4.99 |             3.77 |               -0.02 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               5.01 |             5.61 |             5.39 |            5.69 |            5.25 |             5    |             3.67 |                0.03 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### LogReg / iter

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |               4.91 |             5.36 |             4.82 |            5.23 |            5.16 |             4.94 |             3.4  |               -0.47 |             -0.76 |           -0.83 |           -0.31 |          -0.86 |          -0.5  |           -0.78 |           -0.51 |              -0.2  |
| dti         |               4.91 |             5.71 |             5.62 |            5.37 |            5.56 |             5.3  |             4.14 |               -0.21 |             -0.76 |           -0.6  |           -0.27 |          -0.66 |          -0.34 |           -0.65 |           -0.4  |              -0.08 |
| cell        |               2.41 |             4.23 |             5.01 |            4.28 |            4.56 |             5    |             3.74 |               -1.13 |             -2.58 |           -2.07 |           -1.99 |          -2.13 |          -1.62 |           -0.4  |           -0.26 |              -1.01 |
| oracle_row  |               4.9  |             5.89 |             6.22 |            5.42 |            5.75 |             5.29 |             4.16 |                0.12 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               5.13 |             6.17 |             6.56 |            5.96 |            6.01 |             5.47 |             4.3  |                0.03 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### KNN / mean

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |              -0.05 |             7.97 |             8.04 |            4.13 |            4.19 |             4.27 |             3.36 |               -0.34 |             -0.93 |            0.05 |           -0.06 |          -0.37 |          -0.41 |           -0.69 |           -0.49 |              -0.36 |
| dti         |              -0.05 |             8.03 |             8.23 |            4.17 |            4.17 |             4.59 |             3.55 |               -0.52 |             -0.93 |            0.32 |            0.04 |          -0.5  |          -0.29 |           -0.77 |           -0.51 |              -0.39 |
| cell        |              -4.4  |             8.29 |             7.28 |            2.64 |            1.9  |             4.72 |             2.86 |               -0.75 |             -4.04 |           -1.02 |           -0.63 |          -1.79 |          -1.47 |           -0.52 |           -0.47 |              -0.64 |
| oracle_row  |              -0.19 |             7.93 |             8.37 |            4.13 |            4.09 |             4.64 |             3.5  |               -0.05 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |              -0.17 |             9.45 |             8.84 |            5.09 |            4.14 |             5.31 |             3.75 |               -0.02 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### KNN / iter

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |              -0.05 |             7.82 |             7.57 |            4.22 |            4.4  |             4.88 |             3.67 |                0.16 |             -0.93 |            0.39 |            0.28 |          -0.41 |          -0.08 |           -0.63 |           -0.57 |              -0.19 |
| dti         |              -0.05 |             8.31 |             8.49 |            4.24 |            4.42 |             5.18 |             4.81 |               -0.13 |             -0.93 |            0.25 |            0.03 |          -0.58 |          -0.09 |           -0.52 |           -0.15 |              -0.48 |
| cell        |              -3.48 |             9.23 |             8.35 |            3.39 |            2.71 |             5.65 |             4.4  |               -0.62 |             -3.04 |           -0.18 |           -0.52 |          -1.04 |          -1.33 |           -0.03 |           -0.31 |              -0.68 |
| oracle_row  |              -0.19 |             8.32 |             9.03 |            4.2  |            4.6  |             5.2  |             4.64 |                0.33 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |              -0.2  |             9.63 |             9.22 |            5.16 |            4.7  |             5.91 |             5.04 |                0.05 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### RandomForest / mean

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |               0.27 |             0.05 |            -0.43 |           -0.02 |           -0.14 |             0.09 |            -0.16 |               -0.61 |              -0.7 |           -0.6  |           -0.38 |          -0.61 |          -0.55 |            -0.4 |           -0.54 |              -0.73 |
| dti         |               0.27 |             0.03 |            -0.18 |            0.06 |           -0.28 |             0.07 |            -0.39 |               -0.38 |              -0.7 |           -0.57 |           -0.41 |          -0.46 |          -0.52 |            -0.4 |           -0.43 |              -0.68 |
| cell        |              -0.39 |            -0.31 |            -0.59 |            0.01 |           -0.42 |            -0.37 |            -0.39 |               -0.66 |              -0.4 |           -0.59 |           -0.47 |          -0.19 |          -0.28 |            -0.5 |           -0.56 |              -0.49 |
| oracle_row  |               0.18 |            -0.11 |            -0.13 |            0.1  |           -0.11 |             0.02 |            -0.1  |               -0.29 |             nan   |          nan    |          nan    |         nan    |         nan    |           nan   |          nan    |             nan    |
| oracle_cell |               0.19 |            -0.01 |            -0.02 |            0.18 |           -0.13 |             0    |            -0.17 |               -0.05 |             nan   |          nan    |          nan    |         nan    |         nan    |           nan   |          nan    |             nan    |

### RandomForest / iter

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |               0.27 |             0.07 |             0.04 |            0.05 |            0.16 |            -0.07 |             0.06 |               -0.45 |             -0.7  |           -0.59 |           -0.8  |          -0.8  |          -0.71 |           -0.41 |           -0.54 |              -0.6  |
| dti         |               0.27 |             0.38 |             1.12 |            0.2  |            0.44 |             0.34 |             0.99 |               -0.2  |             -0.7  |           -0.31 |           -0.42 |          -0.61 |          -0.52 |           -0.34 |           -0.27 |              -0.57 |
| cell        |              -0.2  |             0.14 |             0.87 |            0.06 |            0.05 |             0    |             0.43 |               -0.4  |             -0.22 |           -0.34 |           -0.56 |          -0.32 |          -0.64 |            0    |           -0.49 |              -0.46 |
| oracle_row  |               0.18 |             0.48 |             0.96 |            0.27 |            0.49 |             0.22 |             0.77 |               -0.02 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               0.12 |             0.7  |             1.33 |            0.31 |            0.76 |             0.2  |             0.73 |               -0.02 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### RandomForest / native

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| dti         |               0.27 |            -0.06 |            -0.17 |            0.04 |            0.16 |             0.04 |            -0.14 |               -0.19 |              -0.7 |           -0.89 |           -0.59 |          -0.49 |          -0.51 |           -0.08 |           -0.29 |              -0.66 |
| cell        |               0.09 |            -0    |            -0.46 |           -0.13 |            0.12 |             0    |            -0.42 |               -0.99 |              -0.1 |           -0.19 |           -0.44 |          -0.08 |          -0.52 |           -0.21 |           -0.73 |              -1.04 |
| oracle_row  |               0.18 |            -0.16 |            -0.06 |           -0.06 |            0.18 |            -0.12 |            -0.29 |                0.04 |             nan   |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               0.29 |             0.06 |             0.16 |            0.22 |            0.33 |             0.17 |            -0.4  |               -0.07 |             nan   |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### HistGB / mean

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |              -0.03 |            -0.04 |            -0.22 |           -0.1  |            0.08 |             0.16 |            -0.01 |               -0.63 |             -0.89 |           -0.48 |           -0.74 |          -0.9  |          -0.75 |           -0.24 |           -0.54 |              -0.54 |
| dti         |              -0.03 |            -0.15 |            -0.29 |            0.14 |            0.14 |             0.07 |            -0.09 |               -0.47 |             -0.89 |           -0.47 |           -1.11 |          -0.76 |          -0.7  |           -0.32 |           -0.81 |              -0.5  |
| cell        |               0    |            -0.35 |            -0.41 |            0.43 |           -0.27 |             0.04 |            -0.03 |               -0.28 |             -0.31 |           -0.44 |           -0.77 |          -0.34 |          -0.69 |           -0.27 |           -0.23 |              -0.09 |
| oracle_row  |               0.13 |             0.04 |            -0.11 |            0.1  |            0.02 |             0.24 |             0.13 |               -0.17 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               0.45 |             0.13 |             0.31 |            0.46 |            0.36 |             0.22 |             0.42 |               -0.11 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### HistGB / iter

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| itd         |              -0.03 |             0.25 |             0.14 |           -0.1  |            0.03 |             0.2  |             0.06 |               -0.63 |             -0.89 |           -0.36 |           -0.76 |          -0.95 |          -0.94 |           -0.78 |           -0.46 |              -0.54 |
| dti         |              -0.03 |             0.66 |             0.84 |            0.19 |            0.17 |             0.57 |             0.4  |               -0.29 |             -0.89 |           -0.28 |           -0.82 |          -0.81 |          -0.55 |           -0.3  |           -0.68 |              -0.32 |
| cell        |               0.01 |             0.44 |             0.52 |            0.22 |           -0.01 |             0.72 |             0.25 |               -0.4  |             -0.56 |           -0.14 |           -0.49 |          -0.63 |          -0.67 |           -0.08 |           -0.26 |              -0.44 |
| oracle_row  |               0.13 |             0.37 |             0.97 |            0.45 |            0.4  |             0.82 |             0.46 |                0.06 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               0.59 |             0.83 |             1.09 |            0.54 |            0.53 |             0.75 |             0.55 |               -0.06 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

### HistGB / native

| arm         |   gross|complete|0 |   gross|MCAR|0.1 |   gross|MCAR|0.3 |   gross|MAR|0.1 |   gross|MAR|0.3 |   gross|MNAR|0.1 |   gross|MNAR|0.3 |   gross|MNARobs|0.3 |   none|complete|0 |   none|MCAR|0.1 |   none|MCAR|0.3 |   none|MAR|0.1 |   none|MAR|0.3 |   none|MNAR|0.1 |   none|MNAR|0.3 |   none|MNARobs|0.3 |
|:------------|-------------------:|-----------------:|-----------------:|----------------:|----------------:|-----------------:|-----------------:|--------------------:|------------------:|----------------:|----------------:|---------------:|---------------:|----------------:|----------------:|-------------------:|
| dti         |              -0.03 |             0.01 |            -0.01 |            0.04 |           -0.1  |             0.18 |            -0.09 |               -0.29 |             -0.89 |           -0.7  |           -0.62 |          -0.91 |          -0.84 |           -0.8  |           -0.1  |              -0.12 |
| cell        |               0.11 |             0.12 |            -0.27 |            0.24 |           -0.08 |             0.06 |            -0.15 |               -0.6  |             -0.33 |           -0.05 |           -0.61 |          -0.11 |          -0.55 |           -0.06 |           -0.25 |               0.14 |
| oracle_row  |               0.13 |             0.09 |            -0.01 |           -0.18 |           -0.23 |             0.11 |            -0.28 |               -0.39 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |
| oracle_cell |               0.4  |             0.33 |             0.48 |            0.12 |            0.33 |             0.16 |            -0.29 |               -0.04 |            nan    |          nan    |          nan    |         nan    |         nan    |          nan    |          nan    |             nan    |

## D. Paired contrasts on outlier conditions (descriptive, no correction)

| contrast                                       | condition         | family       | imputer   |   n |   mean |   share_positive |   p_two_sided |
|:-----------------------------------------------|:------------------|:-------------|:----------|----:|-------:|-----------------:|--------------:|
| cells vs rows: cell - dti                      | gross|complete|0  | HistGB       | iter      |  20 |  0.043 |             0.6  |         0.401 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | HistGB       | iter      |  20 | -0.225 |             0.4  |         0.571 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | HistGB       | iter      |  20 | -0.322 |             0.5  |         0.784 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | HistGB       | iter      |  20 |  0.033 |             0.45 |         0.911 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | HistGB       | iter      |  20 | -0.18  |             0.45 |         0.756 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | HistGB       | iter      |  20 |  0.146 |             0.5  |         0.701 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | HistGB       | iter      |  20 | -0.143 |             0.5  |         0.841 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | HistGB       | iter      |  20 | -0.112 |             0.55 |         0.756 |
| cells vs rows: cell - dti                      | gross|complete|0  | KNN          | iter      |  20 | -3.427 |             0.1  |         0.001 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | KNN          | iter      |  20 |  0.917 |             0.7  |         0.03  |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | KNN          | iter      |  20 | -0.139 |             0.6  |         0.498 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | KNN          | iter      |  20 | -0.851 |             0.65 |         0.231 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | KNN          | iter      |  20 | -1.712 |             0.45 |         0.097 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | KNN          | iter      |  20 |  0.465 |             0.7  |         0.09  |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | KNN          | iter      |  20 | -0.405 |             0.45 |         0.701 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | KNN          | iter      |  20 | -0.495 |             0.55 |         0.701 |
| cells vs rows: cell - dti                      | gross|complete|0  | LogReg       | iter      |  20 | -2.504 |             0.35 |         0.03  |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | LogReg       | iter      |  20 | -1.481 |             0.5  |         0.546 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | LogReg       | iter      |  20 | -0.615 |             0.35 |         0.409 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | LogReg       | iter      |  20 | -1.091 |             0.45 |         0.475 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | LogReg       | iter      |  20 | -1.004 |             0.3  |         0.189 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | LogReg       | iter      |  20 | -0.295 |             0.5  |         0.737 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | LogReg       | iter      |  20 | -0.396 |             0.35 |         0.546 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | LogReg       | iter      |  20 | -0.919 |             0.45 |         0.498 |
| cells vs rows: cell - dti                      | gross|complete|0  | RandomForest | iter      |  20 | -0.464 |             0.35 |         0.097 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | RandomForest | iter      |  20 | -0.233 |             0.45 |         0.596 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | RandomForest | iter      |  20 | -0.246 |             0.55 |         0.794 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | RandomForest | iter      |  20 | -0.136 |             0.45 |         0.475 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | RandomForest | iter      |  20 | -0.39  |             0.35 |         0.165 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | RandomForest | iter      |  20 | -0.339 |             0.35 |         0.126 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | RandomForest | iter      |  20 | -0.557 |             0.5  |         0.277 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | RandomForest | iter      |  20 | -0.201 |             0.55 |         0.812 |
| cells vs rows: cell - dti                      | gross|complete|0  | HistGB       | mean      |  20 |  0.032 |             0.5  |         0.717 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | HistGB       | mean      |  20 | -0.207 |             0.4  |         0.231 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | HistGB       | mean      |  20 | -0.119 |             0.5  |         0.872 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | HistGB       | mean      |  20 |  0.297 |             0.65 |         0.409 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | HistGB       | mean      |  20 | -0.403 |             0.3  |         0.123 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | HistGB       | mean      |  20 | -0.032 |             0.4  |         0.904 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | HistGB       | mean      |  20 |  0.06  |             0.45 |         0.985 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | HistGB       | mean      |  20 |  0.193 |             0.55 |         0.729 |
| cells vs rows: cell - dti                      | gross|complete|0  | KNN          | mean      |  20 | -4.348 |             0.1  |         0.001 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | KNN          | mean      |  20 |  0.262 |             0.7  |         0.143 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | KNN          | mean      |  20 | -0.948 |             0.55 |         1     |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | KNN          | mean      |  20 | -1.532 |             0.55 |         0.812 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | KNN          | mean      |  20 | -2.271 |             0.2  |         0.001 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | KNN          | mean      |  20 |  0.129 |             0.6  |         0.261 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | KNN          | mean      |  20 | -0.689 |             0.45 |         0.43  |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | KNN          | mean      |  20 | -0.226 |             0.7  |         0.216 |
| cells vs rows: cell - dti                      | gross|complete|0  | LogReg       | mean      |  20 | -2.661 |             0.35 |         0.036 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | LogReg       | mean      |  20 | -1.59  |             0.6  |         0.812 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | LogReg       | mean      |  20 | -1.043 |             0.4  |         0.498 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | LogReg       | mean      |  20 | -1.762 |             0.4  |         0.189 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | LogReg       | mean      |  20 | -1.126 |             0.35 |         0.147 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | LogReg       | mean      |  20 | -0.425 |             0.45 |         0.312 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | LogReg       | mean      |  20 | -0.614 |             0.45 |         0.445 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | LogReg       | mean      |  20 | -0.635 |             0.5  |         0.498 |
| cells vs rows: cell - dti                      | gross|complete|0  | RandomForest | mean      |  20 | -0.657 |             0.25 |         0.007 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | RandomForest | mean      |  20 | -0.34  |             0.45 |         0.616 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | RandomForest | mean      |  20 | -0.413 |             0.5  |         0.522 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | RandomForest | mean      |  20 | -0.05  |             0.6  |         0.898 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | RandomForest | mean      |  20 | -0.14  |             0.5  |         0.841 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | RandomForest | mean      |  20 | -0.437 |             0.3  |         0.154 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | RandomForest | mean      |  20 |  0.003 |             0.45 |         1     |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | RandomForest | mean      |  20 | -0.271 |             0.45 |         0.526 |
| cells vs rows: cell - dti                      | gross|complete|0  | HistGB       | native    |  20 |  0.136 |             0.5  |         0.756 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | HistGB       | native    |  20 |  0.107 |             0.5  |         0.622 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | HistGB       | native    |  20 | -0.263 |             0.4  |         0.295 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | HistGB       | native    |  20 |  0.199 |             0.55 |         0.622 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | HistGB       | native    |  20 |  0.024 |             0.35 |         0.784 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | HistGB       | native    |  20 | -0.117 |             0.55 |         0.956 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | HistGB       | native    |  20 | -0.053 |             0.5  |         0.869 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | HistGB       | native    |  20 | -0.307 |             0.45 |         0.475 |
| cells vs rows: cell - dti                      | gross|complete|0  | RandomForest | native    |  20 | -0.176 |             0.4  |         0.421 |
| cells vs rows: cell - dti                      | gross|MCAR|0.1    | RandomForest | native    |  20 |  0.054 |             0.45 |         0.756 |
| cells vs rows: cell - dti                      | gross|MCAR|0.3    | RandomForest | native    |  20 | -0.298 |             0.3  |         0.171 |
| cells vs rows: cell - dti                      | gross|MAR|0.1     | RandomForest | native    |  20 | -0.173 |             0.45 |         0.444 |
| cells vs rows: cell - dti                      | gross|MAR|0.3     | RandomForest | native    |  20 | -0.04  |             0.35 |         0.475 |
| cells vs rows: cell - dti                      | gross|MNAR|0.1    | RandomForest | native    |  20 | -0.039 |             0.45 |         0.779 |
| cells vs rows: cell - dti                      | gross|MNAR|0.3    | RandomForest | native    |  20 | -0.274 |             0.3  |         0.107 |
| cells vs rows: cell - dti                      | gross|MNARobs|0.3 | RandomForest | native    |  20 | -0.8   |             0.45 |         0.756 |
| oracle cells - oracle rows                     | gross|complete|0  | HistGB       | iter      |  20 |  0.461 |             0.7  |         0.003 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | HistGB       | iter      |  20 |  0.461 |             0.8  |         0.014 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | HistGB       | iter      |  20 |  0.128 |             0.6  |         0.409 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | HistGB       | iter      |  20 |  0.088 |             0.55 |         0.388 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | HistGB       | iter      |  20 |  0.128 |             0.5  |         0.841 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | HistGB       | iter      |  20 | -0.064 |             0.55 |         0.841 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | HistGB       | iter      |  20 |  0.091 |             0.45 |         0.756 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | HistGB       | iter      |  20 | -0.12  |             0.5  |         0.784 |
| oracle cells - oracle rows                     | gross|complete|0  | KNN          | iter      |  20 | -0.009 |             0.4  |         0.528 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | KNN          | iter      |  20 |  1.305 |             0.85 |         0.001 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | KNN          | iter      |  20 |  0.198 |             0.65 |         0.202 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | KNN          | iter      |  20 |  0.957 |             0.9  |         0     |
| oracle cells - oracle rows                     | gross|MAR|0.3     | KNN          | iter      |  20 |  0.098 |             0.55 |         0.52  |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | KNN          | iter      |  20 |  0.711 |             0.75 |         0.019 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | KNN          | iter      |  20 |  0.399 |             0.65 |         0.07  |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | KNN          | iter      |  20 | -0.283 |             0.45 |         0.165 |
| oracle cells - oracle rows                     | gross|complete|0  | LogReg       | iter      |  20 |  0.237 |             0.65 |         0.015 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | LogReg       | iter      |  20 |  0.281 |             0.65 |         0.048 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | LogReg       | iter      |  20 |  0.34  |             0.65 |         0.03  |
| oracle cells - oracle rows                     | gross|MAR|0.1     | LogReg       | iter      |  20 |  0.542 |             0.8  |         0.007 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | LogReg       | iter      |  20 |  0.264 |             0.55 |         0.198 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | LogReg       | iter      |  20 |  0.183 |             0.65 |         0.052 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | LogReg       | iter      |  20 |  0.141 |             0.45 |         0.748 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | LogReg       | iter      |  20 | -0.088 |             0.5  |         0.729 |
| oracle cells - oracle rows                     | gross|complete|0  | RandomForest | iter      |  20 | -0.055 |             0.5  |         0.968 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | RandomForest | iter      |  20 |  0.225 |             0.55 |         0.312 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | RandomForest | iter      |  20 |  0.368 |             0.65 |         0.231 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | RandomForest | iter      |  20 |  0.04  |             0.55 |         0.756 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | RandomForest | iter      |  20 |  0.271 |             0.55 |         0.255 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | RandomForest | iter      |  20 | -0.013 |             0.45 |         0.97  |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | RandomForest | iter      |  20 | -0.045 |             0.45 |         0.968 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | RandomForest | iter      |  20 | -0.001 |             0.4  |         0.955 |
| oracle cells - oracle rows                     | gross|complete|0  | HistGB       | mean      |  20 |  0.312 |             0.7  |         0.177 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | HistGB       | mean      |  20 |  0.093 |             0.6  |         0.455 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | HistGB       | mean      |  20 |  0.423 |             0.75 |         0.03  |
| oracle cells - oracle rows                     | gross|MAR|0.1     | HistGB       | mean      |  20 |  0.358 |             0.6  |         0.076 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | HistGB       | mean      |  20 |  0.34  |             0.55 |         0.177 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | HistGB       | mean      |  20 | -0.027 |             0.55 |         0.881 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | HistGB       | mean      |  20 |  0.294 |             0.6  |         0.368 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | HistGB       | mean      |  20 |  0.062 |             0.6  |         0.812 |
| oracle cells - oracle rows                     | gross|complete|0  | KNN          | mean      |  20 |  0.016 |             0.4  |         0.732 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | KNN          | mean      |  20 |  1.523 |             0.85 |         0.001 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | KNN          | mean      |  20 |  0.477 |             0.75 |         0.048 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | KNN          | mean      |  20 |  0.958 |             0.85 |         0     |
| oracle cells - oracle rows                     | gross|MAR|0.3     | KNN          | mean      |  20 |  0.051 |             0.65 |         0.368 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | KNN          | mean      |  20 |  0.674 |             0.8  |         0.006 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | KNN          | mean      |  20 |  0.25  |             0.6  |         0.07  |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | KNN          | mean      |  20 |  0.026 |             0.6  |         0.596 |
| oracle cells - oracle rows                     | gross|complete|0  | LogReg       | mean      |  20 |  0.116 |             0.5  |         0.298 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | LogReg       | mean      |  20 |  0.525 |             0.75 |         0.019 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | LogReg       | mean      |  20 |  0.508 |             0.7  |         0.058 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | LogReg       | mean      |  20 |  0.149 |             0.65 |         0.202 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | LogReg       | mean      |  20 |  0.092 |             0.55 |         0.157 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | LogReg       | mean      |  20 |  0.01  |             0.6  |         0.841 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | LogReg       | mean      |  20 | -0.103 |             0.45 |         0.546 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | LogReg       | mean      |  20 |  0.047 |             0.55 |         0.784 |
| oracle cells - oracle rows                     | gross|complete|0  | RandomForest | mean      |  20 |  0.014 |             0.55 |         0.398 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | RandomForest | mean      |  20 |  0.105 |             0.6  |         0.368 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | RandomForest | mean      |  20 |  0.103 |             0.45 |         0.927 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | RandomForest | mean      |  20 |  0.085 |             0.5  |         0.748 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | RandomForest | mean      |  20 | -0.025 |             0.35 |         0.622 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | RandomForest | mean      |  20 | -0.023 |             0.4  |         0.881 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | RandomForest | mean      |  20 | -0.071 |             0.5  |         0.648 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | RandomForest | mean      |  20 |  0.243 |             0.7  |         0.053 |
| oracle cells - oracle rows                     | gross|complete|0  | HistGB       | native    |  20 |  0.271 |             0.6  |         0.07  |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | HistGB       | native    |  20 |  0.246 |             0.65 |         0.189 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | HistGB       | native    |  20 |  0.495 |             0.65 |         0.133 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | HistGB       | native    |  20 |  0.307 |             0.7  |         0.083 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | HistGB       | native    |  20 |  0.552 |             0.75 |         0.001 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | HistGB       | native    |  20 |  0.055 |             0.65 |         0.571 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | HistGB       | native    |  20 | -0.006 |             0.45 |         0.956 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | HistGB       | native    |  20 |  0.352 |             0.7  |         0.09  |
| oracle cells - oracle rows                     | gross|complete|0  | RandomForest | native    |  20 |  0.108 |             0.7  |         0.245 |
| oracle cells - oracle rows                     | gross|MCAR|0.1    | RandomForest | native    |  20 |  0.221 |             0.6  |         0.294 |
| oracle cells - oracle rows                     | gross|MCAR|0.3    | RandomForest | native    |  20 |  0.226 |             0.6  |         0.231 |
| oracle cells - oracle rows                     | gross|MAR|0.1     | RandomForest | native    |  20 |  0.288 |             0.6  |         0.154 |
| oracle cells - oracle rows                     | gross|MAR|0.3     | RandomForest | native    |  20 |  0.155 |             0.55 |         0.475 |
| oracle cells - oracle rows                     | gross|MNAR|0.1    | RandomForest | native    |  20 |  0.291 |             0.6  |         0.145 |
| oracle cells - oracle rows                     | gross|MNAR|0.3    | RandomForest | native    |  20 | -0.113 |             0.45 |         0.687 |
| oracle cells - oracle rows                     | gross|MNARobs|0.3 | RandomForest | native    |  20 | -0.113 |             0.4  |         0.43  |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | HistGB       | iter      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | HistGB       | iter      |  20 |  0.411 |             0.75 |         0.04  |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | HistGB       | iter      |  20 |  0.703 |             0.65 |         0.024 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | HistGB       | iter      |  20 |  0.292 |             0.65 |         0.133 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | HistGB       | iter      |  20 |  0.146 |             0.6  |         0.204 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | HistGB       | iter      |  20 |  0.372 |             0.6  |         0.165 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | HistGB       | iter      |  20 |  0.335 |             0.8  |         0.076 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | HistGB       | iter      |  20 |  0.343 |             0.75 |         0.189 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | KNN          | iter      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | KNN          | iter      |  20 |  0.488 |             0.75 |         0.009 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | KNN          | iter      |  20 |  0.912 |             0.6  |         0.036 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | KNN          | iter      |  20 |  0.02  |             0.55 |         0.648 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | KNN          | iter      |  20 |  0.021 |             0.45 |         0.956 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | KNN          | iter      |  20 |  0.304 |             0.7  |         0.097 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | KNN          | iter      |  20 |  1.136 |             0.75 |         0.003 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | KNN          | iter      |  20 | -0.287 |             0.4  |         0.165 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | LogReg       | iter      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | LogReg       | iter      |  20 |  0.344 |             0.7  |         0.016 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | LogReg       | iter      |  20 |  0.806 |             0.8  |         0.011 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | LogReg       | iter      |  20 |  0.143 |             0.6  |         0.52  |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | LogReg       | iter      |  20 |  0.406 |             0.65 |         0.136 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | LogReg       | iter      |  20 |  0.352 |             0.7  |         0.025 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | LogReg       | iter      |  20 |  0.737 |             0.65 |         0.076 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | LogReg       | iter      |  20 |  0.257 |             0.6  |         0.251 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | RandomForest | iter      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | RandomForest | iter      |  20 |  0.303 |             0.65 |         0.202 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | RandomForest | iter      |  20 |  1.076 |             0.85 |         0.005 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | RandomForest | iter      |  20 |  0.147 |             0.75 |         0.097 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | RandomForest | iter      |  20 |  0.281 |             0.6  |         0.165 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | RandomForest | iter      |  20 |  0.409 |             0.65 |         0.008 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | RandomForest | iter      |  20 |  0.921 |             0.75 |         0.015 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | RandomForest | iter      |  20 |  0.247 |             0.65 |         0.312 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | HistGB       | mean      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | HistGB       | mean      |  20 | -0.102 |             0.4  |         0.641 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | HistGB       | mean      |  20 | -0.071 |             0.45 |         0.368 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | HistGB       | mean      |  20 |  0.241 |             0.6  |         0.083 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | HistGB       | mean      |  20 |  0.059 |             0.6  |         0.33  |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | HistGB       | mean      |  20 | -0.091 |             0.45 |         0.33  |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | HistGB       | mean      |  20 | -0.079 |             0.6  |         0.812 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | HistGB       | mean      |  20 |  0.16  |             0.55 |         0.648 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | KNN          | mean      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | KNN          | mean      |  20 |  0.059 |             0.45 |         0.653 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | KNN          | mean      |  20 |  0.189 |             0.5  |         0.313 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | KNN          | mean      |  20 |  0.039 |             0.45 |         0.653 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | KNN          | mean      |  20 | -0.017 |             0.45 |         0.784 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | KNN          | mean      |  20 |  0.328 |             0.45 |         0.642 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | KNN          | mean      |  20 |  0.191 |             0.45 |         0.409 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | KNN          | mean      |  20 | -0.18  |             0.3  |         0.261 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | LogReg       | mean      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | LogReg       | mean      |  20 |  0.063 |             0.5  |         0.307 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | LogReg       | mean      |  20 | -0.159 |             0.45 |         0.368 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | LogReg       | mean      |  20 | -0.006 |             0.35 |         0.679 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | LogReg       | mean      |  20 | -0.058 |             0.5  |         0.643 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | LogReg       | mean      |  20 | -0.046 |             0.3  |         0.78  |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | LogReg       | mean      |  20 | -0.084 |             0.4  |         0.472 |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | LogReg       | mean      |  20 |  0.128 |             0.7  |         0.112 |
| order: detect-then-impute - impute-then-detect | gross|complete|0  | RandomForest | mean      |  20 |  0     |             0    |       nan     |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.1    | RandomForest | mean      |  20 | -0.019 |             0.4  |         0.627 |
| order: detect-then-impute - impute-then-detect | gross|MCAR|0.3    | RandomForest | mean      |  20 |  0.257 |             0.7  |         0.053 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.1     | RandomForest | mean      |  20 |  0.085 |             0.5  |         0.571 |
| order: detect-then-impute - impute-then-detect | gross|MAR|0.3     | RandomForest | mean      |  20 | -0.139 |             0.35 |         0.277 |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.1    | RandomForest | mean      |  20 | -0.023 |             0.35 |         0.39  |
| order: detect-then-impute - impute-then-detect | gross|MNAR|0.3    | RandomForest | mean      |  20 | -0.23  |             0.3  |         0.07  |
| order: detect-then-impute - impute-then-detect | gross|MNARobs|0.3 | RandomForest | mean      |  20 |  0.23  |             0.5  |         0.295 |

## E. Removals that deleted a whole class (%)

| arm         |   % wiped |
|:------------|----------:|
| cell        |         0 |
| dti         |         0 |
| itd         |         0 |
| oracle_cell |         0 |
| oracle_row  |         0 |
