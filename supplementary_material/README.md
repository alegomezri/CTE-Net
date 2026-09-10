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
## Supplementary Data S2

### Signal-quality assessment and post hoc sensitivity analysis

This directory contains the results of the post hoc signal-quality assessment and sensitivity analysis performed for CTE-Net. The analysis included 8,213 physical EEG windows from 120 participants and the corresponding out-of-fold predictions obtained across ten random training seeds.

EEG windows were screened for nonfinite values, flat channels, extreme amplitude, kurtosis, frontal low- and high-frequency activity, and 50-Hz line noise. Participant-balanced median/MAD thresholds were estimated using 30 windows per participant. The primary criterion defined potentially contaminated windows using a robust threshold of \(z>5\), while \(z>4\) and \(z>6\) were examined as alternative sensitivity conditions.

The model was not retrained. Instead, flagged windows were excluded from the previously generated out-of-fold predictions, after which the window- and participant-level metrics were recalculated. Therefore, this analysis evaluates the stability of the reported predictive performance and does not constitute an artifact-removal preprocessing pipeline.

### Included files

| File                                                             | Description                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CTE_Net_signal_quality_robust_thresholds.csv`                   | Median, MAD, and resulting robust thresholds for each signal-quality indicator.                                                                                                                                                                                    |
| `CTE_Net_signal_quality_flag_summary.csv`                        | Number and percentage of windows flagged under the \(z>4\), \(z>5\), and \(z>6\) criteria.                                                                                                                                                                         |
| `CTE_Net_signal_quality_reason_counts.csv`                       | Number of windows associated with each signal-quality indicator, including extreme kurtosis, 50-Hz line noise, peak-to-peak amplitude, absolute amplitude, and high-frequency activity.                                                                            |
| `CTE_Net_artifact_sensitivity_window_metrics_summary.csv`        | Window-level performance metrics before and after excluding flagged windows under the evaluated thresholds.                                                                                                                                                        |
| `CTE_Net_artifact_sensitivity_subject_metrics_95CI.csv`          | Participant-level performance before and after the primary \(z>5\) exclusion, including 95% confidence intervals from 5,000 stratified participant-level bootstrap resamples.                                                                                      |
| `CTE_Net_artifact_sensitivity_subject_metrics_by_seed.csv`       | Participant-level metrics calculated separately for each random training seed and valid signal-quality condition.                                                                                                                                                  |
| `CTE_Net_artifact_sensitivity_subject_coverage_by_condition.csv` | Number of participants retained under each signal-quality condition. The \(z>5\) and \(z>6\) conditions retained all 120 participants, whereas \(z>4\) left one participant without retained windows and was therefore omitted from participant-level comparisons. |
| `CTE_Net_signal_quality_group_summary.csv`                       | Participant-level distribution of potentially contaminated windows for the ADHD and control groups.                                                                                                                                                                |
| `CTE_Net_artifact_prediction_association.csv`                    | Spearman associations between the participant-level proportion of flagged windows and the consensus ADHD probability.                                                                                                                                              |

### Main findings

Under the primary \(z>5\) threshold, 358 of 8,213 EEG windows (4.36%) were identified as potentially contaminated. Excluding these windows changed the window-level performance metrics by no more than 0.51 percentage points and the participant-level metrics by no more than 0.17 percentage points. The participant-level accuracy changed from 83.42% to 83.50%, while ROC-AUC changed from 90.24% to 90.15%.

Across the complete cohort, the proportion of flagged windows was not significantly associated with the consensus ADHD probability (\(\rho=0.062\), \(p=0.503\)). These results indicate that the principal classification findings remained stable after excluding windows with extreme signal-quality indicators.

The flagged windows should be interpreted as potentially contaminated rather than confirmed artifacts. This post hoc analysis does not demonstrate that the retained signals or learned connectivity patterns are artifact-free.

The code used to generate these supplementary files is provided in:

```text
tests/analysis-sensibility.ipynb
```
## Supplementary Data S3

### Structural sensitivity analysis of the Transfer Entropy parameters

These files report an additional structural sensitivity analysis of the Transfer Entropy module in CTE-Net. The analysis examined the Takens embedding dimensions \(D_x\) and \(D_y\), the reconstruction delay \(\tau\), and the interaction lag \(\mu\). It includes the selected reference configuration, \(D_x=6\), \(D_y=1\), \(\tau=2\), and \(\mu=2\), together with ten alternative completed configurations.

The reported objective corresponds to the mean validation accuracy across the five fixed subject-wise folds. These results characterize the sensitivity of the validation objective to the structural parameters of the Transfer Entropy module; they do not constitute an independent test-set or external-validation comparison.

### Included files

| File                                                                  | Description                                                                                                                                                                                                                                                  |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Supplementary_Data_S3_TE_structural_sensitivity_trials(1).csv`       | Trial-level results for the 11 completed configurations, including the trial identifiers and state, execution timestamps, objective value, \(D_x\), \(D_y\), \(\tau\), \(\mu\), reference-configuration indicator, objective percentage, difference from the reference in percentage points, configuration label, rank, and configuration type. |
| `Supplementary_Data_S3_TE_structural_sensitivity_summary(1).csv`      | Study-level summary containing the number of completed and alternative configurations, the reference parameters and objective, the rank of the reference configuration, and the minimum, maximum, mean, sample standard deviation, median, and range of the validation objective.                                      |

### Main findings

## Supplementary Data S4

### Preprocessing and reference sensitivity analyses

The [Supplementary Data S4](https://github.com/alegomezri/CTE-Net/tree/main/supplementary_material/Supplementary%20Data%20S4) directory provides analysis code for two complementary sensitivity experiments: frequency filtering with signal-quality screening and common-average referencing (CAR).

The filtering experiment retrains CTE-Net using frequency-filtered EEG after fold-specific exclusion of windows with extreme signal-quality indicators. Thresholds are estimated using only the corresponding training participants, and the original A1/A2 condition is evaluated using the same retained test windows. Unlike the post hoc analysis in S2, this experiment includes model retraining.

The CAR experiment retrains CTE-Net after common-average referencing and compares its predictions and learned connectivity with those obtained under the original A1/A2 reference. Both experiments use the five fixed subject-wise folds, ten random training seeds, and the fixed CTE-Net configuration without additional hyperparameter optimization.

### Analysis notebooks

| File | Description |
| --- | --- |
| `cte-net-filtering.ipynb` | Frequency-filtered and quality-screened EEG sensitivity workflow, including training and the corresponding analyses. |
| `cte-net-car.ipynb` | Common-average-reference sensitivity workflow, including training and the corresponding analyses. |

### Included CSV files

| File | Description |
| --- | --- |
| `condition_training_summary.csv` | Training summary by condition, seed, and fold, including the selected epoch, validation accuracy, and number of epochs executed. |
| `paired_fold_metrics.csv` | Fold-level classification metrics for the paired conditions. |
| `window_metrics_mean_across_folds_by_seed.csv` | Window-level classification metrics averaged across folds within each random seed. |
| `paired_window_predictions.csv` | Window-level predictions used in the paired comparison. |
| `paired_subject_predictions_by_seed.csv` | Participant-level predictions for each random seed and condition. |
| `participant_metrics_by_seed.csv` | Participant-level classification metrics for each random seed. |
| `participant_metrics_95CI.csv` | Participant-level performance estimates and 95% confidence intervals, with participant, seed, and bootstrap counts. |
| `participant_metric_differences_95CI.csv` | Paired differences in participant-level metrics with 95% bootstrap confidence intervals. The comparison column specifies the subtraction order. |
| `participant_bootstrap_distribution.csv` | Bootstrap results underlying the participant-level statistical summaries. |
| `participant_consensus_predictions.csv` | Participant-level consensus predictions across random seeds. |
| `prediction_agreement_and_mcnemar.csv` | Correlation of participant probabilities, classification agreement, discordant classification counts, and exact McNemar p-values. |
| `connectivity_stability_95CI.csv` | Connectivity concordance summaries with 95% confidence intervals, including Spearman correlation across 342 directed connections and Jaccard overlap for the strongest 10% of connections. |
| `connectivity_stability_by_class.csv` | Connectivity concordance summarized by diagnostic class. |
| `connectivity_stability_by_participant.csv` | Participant-level connectivity concordance results. |
| `quality_features_all_windows.csv` | Window-level signal-quality indicators, including amplitude, kurtosis, spectral ratios, nonfinite values, and flat-channel indicators. |
| `quality_thresholds_by_fold.csv` | Fold-specific robust signal-quality thresholds, reference medians and scales, threshold direction, and flag counts. |
| `quality_summary_by_fold_and_split.csv` | Participant and window coverage by fold and split, including retained and flagged window counts. |

### Scope of the currently supplied results

The supplied performance summary, paired metric-difference, prediction-agreement, and connectivity-summary CSV files report `common_average_reference` versus `original_A1A2_same_windows`. The training summary likewise identifies the CAR condition. The current quality-coverage summary reports no excluded windows. These exports should therefore not be interpreted as the performance results or retained-window counts of the filtered and quality-screened experiment. The filtering notebook and quality-indicator/threshold files are provided, but separate filtering performance exports are not identified in the current directory.

For CAR, the participant-level accuracy is 83.08% (95% CI: 77.67–88.08%), compared with 83.42% (95% CI: 78.25–88.25%) under the original reference on the same windows. The paired accuracy difference is −0.33 percentage points (95% CI: −2.33 to 1.75). Participant-level classification agreement is 94.17%, with an exact McNemar p-value of 1.0. Similar predictive performance should not be interpreted as unchanged connectivity: the mean participant-level Spearman correlation across directed connections is 0.0696, and the mean Jaccard overlap for the strongest 10% is 0.0674.

### Reproducibility

The CSV results can be inspected without retraining. To rerun the workflows, obtain the source EEG data separately, install the dependencies imported by the notebooks, and configure their input and output paths. Model checkpoints and intermediate binary TE arrays are not included in this directory and must be regenerated or supplied separately for notebook steps that require them. Metric values in the participant-level performance and difference tables are expressed as proportions; multiply by 100 to obtain percentages or percentage-point differences, respectively.


Across the 11 completed configurations, the mean validation accuracy ranged from 81.63% to 89.78%, with a mean of 86.00%, a sample standard deviation of 2.45 percentage points, and a median of 86.20%. The total range was 8.15 percentage points. The selected reference configuration achieved 81.63%, whereas the highest validation objective, 89.78%, was obtained with \(D_x=6\), \(D_y=1\), \(\tau=4\), and \(\mu=1\).

Because the configurations were compared using the same internal validation objective employed during hyperparameter analysis, the results should be interpreted as a structural sensitivity assessment rather than as evidence of improved held-out or externally validated performance.
