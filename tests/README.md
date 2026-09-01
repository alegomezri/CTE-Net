# Tests and statistical analyses

This directory contains the notebooks used to evaluate CTE-Net, compare it with the baseline and ablation models, assess the stability of its Transfer Entropy (TE) representations, and perform the post hoc signal-quality sensitivity analysis accompanying the manuscript *Transformer-Based Modeling of Directed Transfer Entropy Connectivity for EEG-Based ADHD Classification in Children*.

## Notebooks

| Notebook | Main purpose | Analysis unit |
| --- | --- | --- |
| `all-window-predictions.ipynb` | Reconstructs window-level metrics, performs paired Wilcoxon tests across ten training seeds, and generates the supplementary normalized confusion matrices. | Window and random seed |
| `mcnemar-tests-cte-net.ipynb` | Performs exact paired comparisons between CTE-Net and the five baseline models using one consensus decision per participant. | Participant |
| `ablation-test.ipynb` | Compares the complete CTE-Net model with variants without the TE module and without the Transformer. | Window, random seed, and participant |
| `cte-net-te-stability-10-seeds.ipynb` | Reinfers the 50 trained CTE-Net models, reconstructs out-of-fold predictions, calculates participant-level performance, and assesses TE stability across windows and seeds. | Window, fold, random seed, and participant |
| `analysis-sensibility.ipynb` | Evaluates the sensitivity of the reported performance to the post hoc exclusion of windows with extreme signal-quality indicators. | Window and participant |

## Window-level metrics and seed-level comparisons

### `all-window-predictions.ipynb`

This notebook reconstructs the window-level results for:

* CTE-Net
* EEGNet
* ShallowConvNet
* T-GARNet
* IMC-BGT
* MultiStream

ADHD is treated as the positive class, and window-level probabilities are converted into predictions using a threshold of 0.5. For each model and seed, metrics are first computed within each of the five fixed subject-wise test folds and then averaged across folds. The reported mean and sample standard deviation are calculated across the ten matched training seeds.

The notebook also performs paired two-sided Wilcoxon signed-rank tests between CTE-Net and each baseline for accuracy, precision, and sensitivity. Holm correction is applied across the complete family of 15 prespecified comparisons: three metrics multiplied by five baselines. These seed-level tests evaluate whether differences were consistently reproduced across training initializations; seeds are not interpreted as independent clinical observations.

Finally, the notebook generates row-normalized window-level confusion matrices. Within each seed, sensitivity and specificity correspond to the mean across the five folds. The four matrix cells are subsequently summarized using the mean and sample standard deviation across ten seeds.

### Main outputs

| Output directory | Generated files |
| --- | --- |
| `/kaggle/working/comment_12_window_metrics/` | `window_metrics_by_fold.csv`, `window_metrics_by_seed.csv`, `window_metrics_mean_std.csv`, and `window_metrics_table_for_manuscript.csv` |
| `/kaggle/working/comment_12_wilcoxon_holm/` | `CTE_Net_vs_baselines_Wilcoxon_Holm_updated.csv` and `CTE_Net_vs_baselines_Wilcoxon_Holm_manuscript.csv` |
| `/kaggle/working/comment_12_supplementary/` | `Supplementary_Data_S1_window_level_normalized_confusion_matrices.csv` |

## Participant-level baseline comparisons

### `mcnemar-tests-cte-net.ipynb`

This notebook reads one consensus prediction per participant for CTE-Net and the five baseline models. It verifies that all models contain the same 120 participants, labels, and subject-wise test assignments before carrying out the comparisons.

The analysis includes:

* Exact two-sided McNemar tests for CTE-Net versus each baseline.
* Holm correction across the five paired model comparisons.
* Discordant counts \(n_{10}\) and \(n_{01}\).
* Paired differences in accuracy, sensitivity, specificity, precision, F1-score, and ROC-AUC.
* Stratified participant-level bootstrap 95% confidence intervals using 5,000 resamples.
* Descriptive consensus and fold-level metrics for all six models.
* A manuscript-ready LaTeX table.

The participant is the paired statistical unit. The ten training seeds are combined into the consensus probability and are not treated as independent observations.

### Main outputs

Results are saved to `/kaggle/working/CTE_Net_participant_level_pairwise_tests/`:

| File | Description |
| --- | --- |
| `CTE_Net_vs_baselines_McNemar_Holm.csv` | Exact McNemar results and Holm-adjusted p-values. |
| `CTE_Net_vs_baselines_paired_metric_differences_95CI.csv` | Paired metric differences and participant-level 95% confidence intervals. |
| `CTE_Net_vs_baselines_paired_bootstrap_distributions.csv` | Bootstrap distributions for all paired metric differences. |
| `CTE_Net_vs_baselines_paired_subject_details.csv` | Participant-level predictions, correctness indicators, and discordance status. |
| `all_models_consensus_performance.csv` | Descriptive performance of the consensus predictions. |
| `all_models_fold_level_consensus_metrics.csv` | Descriptive participant-level metrics within each test fold. |
| `participant_level_mcnemar_holm_table.tex` | LaTeX table for manuscript preparation. |

## Ablation analysis

### `ablation-test.ipynb`

This notebook compares:

* Complete CTE-Net
* CTE-Net without the TE module
* CTE-Net without the Transformer

It reconstructs all metrics from the saved out-of-fold window probabilities and audits the experimental protocol. The audit verifies the presence of ten seeds, five folds per seed, 120 participants per seed, consistent labels, and identical subject-wise test partitions across the three architectures.

Two complementary statistical analyses are performed:

1. Paired two-sided Wilcoxon signed-rank tests across the ten matched seeds for accuracy, sensitivity, and precision. Holm correction is applied across six comparisons: three metrics multiplied by two ablations.
2. Exact paired McNemar tests using one consensus decision per participant and architecture. Holm correction is applied across the two ablation comparisons.

The Wilcoxon analysis describes consistency across computational repetitions. The participant-level McNemar analysis is the primary paired inferential comparison.

### Main outputs

Results are saved to `/kaggle/working/ablation_statistical_tests/`. The principal files are:

* `Ablation_input_protocol_audit.csv`
* `Ablation_window_metrics_by_fold_recomputed.csv`
* `Ablation_window_metrics_by_seed_recomputed.csv`
* `Ablation_window_metrics_mean_std.csv`
* `Ablation_Wilcoxon_Holm_primary_metrics.csv`
* `Ablation_participant_predictions_by_seed.csv`
* `Ablation_participant_consensus_predictions.csv`
* `Ablation_participant_metrics_by_seed.csv`
* `Ablation_participant_metrics_mean_std.csv`
* `Ablation_McNemar_exact_Holm.csv`
* `Ablation_seed_comparisons_for_manuscript.csv`
* `Ablation_participant_comparisons_for_manuscript.csv`

## CTE-Net reinference and Transfer Entropy stability

### `cte-net-te-stability-10-seeds.ipynb`

This notebook loads the raw EEG data, the five predefined subject-wise folds, and the 50 CTE-Net checkpoints obtained from ten seeds and five folds. The architecture of each model is inferred from its checkpoint state dictionary before out-of-fold reinference.

The notebook performs three connected analyses:

1. **Complete reinference:** reconstructs window-level probabilities, fold metrics, seed-level summaries, participant summaries, and saved-versus-recomputed metric comparisons.
2. **Participant-level evaluation:** averages window probabilities within each participant and seed, applies a threshold of 0.5, and estimates 95% confidence intervals using 5,000 stratified participant-level bootstrap resamples.
3. **TE stability:** compares the 342 directed off-diagonal TE coefficients of each window with the mean of the remaining windows from the same participant. Stability is summarized using Spearman correlation and Jaccard similarity for the strongest 10% of directed connections. Values are averaged first across windows and then across ten seeds, producing one observation per participant. Confidence intervals are estimated using 5,000 participant-level bootstrap resamples.

### Main outputs

Results are saved to `/kaggle/working/HybridTransformerTEKTE_reinference_complete/`. The principal outputs include:

| Analysis | Main files |
| --- | --- |
| Reinference | `CTE_Net_all_window_predictions.csv`, `CTE_Net_subject_summary_by_seed.csv`, `CTE_Net_fold_metrics_recomputed.csv`, `CTE_Net_saved_vs_recomputed_metrics.csv`, and `CTE_Net_seed_metrics_mean_of_folds.csv` |
| Participant-level evaluation | `CTE_Net_subject_level_predictions_by_seed.csv`, `CTE_Net_subject_level_metrics_95CI.csv`, `CTE_Net_subject_level_consensus_predictions.csv`, and `CTE_Net_subject_level_table_for_manuscript.tex` |
| TE stability | `CTE_Net_TE_stability_by_window_seed.csv`, `CTE_Net_TE_stability_by_subject_seed.csv`, `CTE_Net_TE_stability_by_subject_consensus.csv`, `CTE_Net_TE_stability_summary_95CI.csv`, `CTE_Net_TE_stability_bootstrap_distribution.csv`, and `CTE_Net_TE_stability_table_for_manuscript.tex` |

## Post hoc signal-quality sensitivity analysis

### `analysis-sensibility.ipynb`

This notebook performs a post hoc sensitivity analysis without loading model checkpoints or retraining CTE-Net. It reconstructs the original EEG windows and links them to the previously saved out-of-fold predictions.

Each physical EEG window is screened using:

* Nonfinite values.
* Practically flat channels.
* Maximum absolute amplitude.
* Maximum peak-to-peak amplitude.
* Maximum channel kurtosis.
* Frontal 0.5–4 Hz power ratio.
* 30–45 Hz high-frequency power ratio.
* 48–52 Hz line-noise ratio.

Participant-balanced reference thresholds are constructed using the same number of uniformly selected windows from each participant. The primary rule uses a robust threshold of \(z>5\), while \(z>4\) and \(z>6\) are evaluated as alternative sensitivity conditions.

Flagged windows are excluded only from the previously generated test predictions, after which window- and participant-level metrics are recalculated. The participant-level comparison between all windows and the primary \(z>5\) condition uses 5,000 stratified bootstrap resamples. This analysis does not constitute an artifact-removal preprocessing pipeline, and flagged windows must be interpreted as potentially contaminated rather than confirmed artifacts.

### Main outputs

Results are saved to `/kaggle/working/CTE_Net_artifact_quality_sensitivity/`. The main supplementary outputs are:

* `CTE_Net_signal_quality_robust_thresholds.csv`
* `CTE_Net_signal_quality_flag_summary.csv`
* `CTE_Net_signal_quality_reason_counts.csv`
* `CTE_Net_signal_quality_group_summary.csv`
* `CTE_Net_artifact_sensitivity_window_metrics_summary.csv`
* `CTE_Net_artifact_sensitivity_subject_metrics_by_seed.csv`
* `CTE_Net_artifact_sensitivity_subject_metrics_95CI.csv`
* `CTE_Net_artifact_sensitivity_subject_coverage_by_condition.csv`
* `CTE_Net_artifact_prediction_association.csv`
* `CTE_Net_artifact_sensitivity_analysis_summary.json`
* `artifact_rate_by_diagnostic_group.png`
* `participant_performance_before_after_qc.png`

## Requirements

The notebooks were developed for a Kaggle Python environment and use:

* NumPy
* pandas
* SciPy
* scikit-learn
* statsmodels
* Matplotlib
* PyTorch

The sensitivity analysis additionally reads MATLAB `.mat` EEG files. The reinference and TE-stability notebook requires the trained PyTorch checkpoints and benefits substantially from GPU execution.

## Data and path configuration

The notebooks use Kaggle-specific input and output paths. Update the path variables at the beginning of each notebook when running them in another environment.

The signal-quality notebook also supports the following environment variables:

* `CTE_NET_DATASET_ROOT`
* `CTE_NET_RESULTS_ROOT`
* `CTE_NET_QC_OUTPUT_ROOT`
* `CTE_NET_QC_SMOKE_TEST=1` for a reduced 100-resample bootstrap test

## Statistical interpretation

The seed-level and participant-level analyses provide complementary evidence. Paired Wilcoxon tests determine whether performance differences are consistently reproduced across matched random training initializations, whereas exact McNemar tests determine whether those differences translate into different numbers of correctly classified participants.

Random seeds quantify optimization variability and are not independent clinical observations. Participant-level inference therefore uses the participant as the paired or bootstrap sampling unit. All classification analyses rely on out-of-fold predictions, ADHD is treated as the positive class, and the default decision threshold is 0.5.
