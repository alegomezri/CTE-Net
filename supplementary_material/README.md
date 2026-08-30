# Supplementary Material

This directory contains the supplementary data accompanying the manuscript *Transformer-Based Modeling of Directed Transfer Entropy Connectivity for EEG-Based ADHD Classification in Children*.

## Supplementary Data S1

### `Supplementary_Data_S1_window_level_normalized_confusion_matrices.csv`

This file reports the window-level row-normalized confusion matrices for the following models:

* CTE-Net
* EEGNet
* ShallowConvNet
* T-GARNet
* IMC-BGT
* MultiStream

For each model, the file contains the four confusion-matrix cells:

* `TN`: Control windows correctly classified as Control
* `FP`: Control windows incorrectly classified as ADHD
* `FN`: ADHD windows incorrectly classified as Control
* `TP`: ADHD windows correctly classified as ADHD

The matrices are normalized by true class. Therefore, the values corresponding to each true-class row sum to 1. ADHD is treated as the positive class, and window-level predictions use a decision threshold of 0.5.

For each random seed, the normalized values were first averaged across the five fixed subject-wise folds. The reported values correspond to the mean and sample standard deviation across the ten random seeds.

## Column description

| Column               | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| `model`              | Classification model                                                      |
| `true_class`         | True class of the EEG windows                                             |
| `predicted_class`    | Class predicted by the model                                              |
| `matrix_cell`        | Confusion-matrix cell: TN, FP, FN, or TP                                  |
| `mean`               | Mean normalized value across the ten seeds, expressed as a proportion     |
| `std`                | Sample standard deviation across the ten seeds, expressed as a proportion |
| `n_seeds`            | Number of random seeds used in the summary                                |
| `mean_percent`       | Mean normalized value expressed as a percentage                           |
| `std_percent`        | Sample standard deviation expressed as a percentage                       |
| `normalization`      | Normalization procedure applied to the confusion matrix                   |
| `aggregation`        | Procedure used to aggregate folds and random seeds                        |
| `positive_class`     | Class treated as positive                                                 |
| `decision_threshold` | Probability threshold used for window-level classification                |

The code used to generate this supplementary file is provided in:

```text
tests/all-window-predictions.ipynb
```

