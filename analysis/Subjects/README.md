# Participant-level evaluation

This directory contains the notebooks used to reconstruct and evaluate participant-level out-of-fold predictions for CTE-Net and the five baseline models accompanying the manuscript *Transformer-Based Modeling of Directed Transfer Entropy Connectivity for EEG-Based ADHD Classification in Children*.

## Notebooks

| Notebook | Model | Execution type | Default output directory |
| --- | --- | --- | --- |
| `cte-net-ic-95.ipynb` | CTE-Net | Reinference of 50 saved checkpoints with automatic architecture reconstruction | `/kaggle/working/HybridTransformerTEKTE_reinference_complete/` |
| `eeg-net-ic-95.ipynb` | EEGNet | Reinference of 50 saved checkpoints | `/kaggle/working/EEGNet_reinference_complete/` |
| `shallow-net-ic-95.ipynb` | ShallowConvNet | Reinference of 50 saved checkpoints, including the custom loss required for deserialization | `/kaggle/working/ShallowConvNet_reinference_complete/` |
| `t-garnet-ic-95.ipynb` | T-GARNet | Reinference of 50 saved checkpoints | `/kaggle/working/TGARNet_reinference_complete/` |
| `im-cbgt-ic-95.ipynb` | IMC-BGT | Complete repeated training and evaluation using ten seeds and five folds | `/kaggle/working/resultados_imcbgt_tdah_ARTICULO_120subjects/` |
| `multistream-ic-95.ipynb` | MultiStream | Analysis of previously generated outputs without training or loading a model | `/kaggle/working/MultiStream_analysis_only/` |

## Shared participant-level procedure

The notebooks implement the same participant-level evaluation protocol:

1. Only out-of-fold test-window probabilities are used.
2. Within each seed, the ADHD probabilities of all windows belonging to the same participant are averaged arithmetically.
3. A threshold of 0.5 is applied to the participant probability, with ADHD treated as the positive class.
4. Accuracy, sensitivity, specificity, precision, F1-score, and ROC-AUC are calculated separately for each seed.
5. The reported point estimate is the mean of the ten seed-specific participant-level metrics.
6. The 95% confidence intervals are estimated using 5,000 stratified percentile-bootstrap resamples with the participant as the sampling unit.

Within each bootstrap replicate, Control and ADHD participants are sampled separately with replacement. The same sampled participants are then applied to all ten seed-specific predictions, the metric is calculated within each seed, and the ten values are averaged. Consequently, random seeds quantify model-initialization variability and are not treated as independent clinical observations.

## Consensus predictions

In addition to the seed-specific evaluation, every notebook generates one consensus prediction per participant. The participant probabilities are averaged across the ten seeds and thresholded at 0.5.

The consensus exports are intended for paired participant-level analyses, particularly the exact McNemar comparisons performed in `TEST/mcnemar-tests-cte-net.ipynb`. The consensus metrics and the bootstrap point estimates serve different purposes: confidence intervals summarize the mean performance across seeds, whereas consensus predictions provide one paired decision per participant and model.

## Standard participant-level outputs

Each notebook produces the same set of participant-level files using its corresponding prefix:

| File pattern | Description |
| --- | --- |
| `<PREFIX>_subject_level_predictions_by_seed.csv` | One participant probability and prediction for every participant and seed. |
| `<PREFIX>_subject_level_metrics_by_seed.csv` | Descriptive participant-level metrics calculated separately for each seed. |
| `<PREFIX>_subject_level_metrics_95CI.csv` | Mean performance across seeds and stratified participant-level bootstrap 95% confidence intervals. |
| `<PREFIX>_subject_level_bootstrap_distribution.csv` | Complete bootstrap distributions for the six participant-level metrics. |
| `<PREFIX>_subject_level_point_metrics_by_seed.csv` | Seed-specific metrics used to calculate the reported point estimates. |
| `<PREFIX>_subject_level_consensus_predictions.csv` | One seed-averaged probability and decision per participant. |
| `<PREFIX>_subject_level_table_for_manuscript.csv` | Compact manuscript-ready participant-level results table. |
| `<PREFIX>_subject_level_table_for_manuscript.tex` | LaTeX version of the participant-level results table. |

The filename prefixes are:

| Model | Prefix |
| --- | --- |
| CTE-Net | `CTE_Net` |
| EEGNet | `EEGNet` |
| ShallowConvNet | `ShallowConvNet` |
| T-GARNet | `TGARNet` |
| IMC-BGT | `IMCBGT` |
| MultiStream | `MultiStream` |

## CTE-Net

### `cte-net-ic-95.ipynb`

This notebook reconstructs the architecture of each CTE-Net checkpoint directly from its saved state dictionary. It also resolves the compatible number of attention heads by comparing the recomputed fold metrics with the stored values.

The notebook loads the complete cohort and five subject-wise folds, discovers the 50 checkpoints, performs out-of-fold reinference, and exports window-, fold-, seed-, and participant-level results. It additionally generates subject-performance heatmaps and data files for TikZ-based figures.

## EEGNet

### `eeg-net-ic-95.ipynb`

This notebook loads the 120-participant cohort and reinfers the ten-seed, five-fold EEGNet checkpoints. It reconstructs the window probabilities, compares recomputed and stored fold metrics, summarizes performance across folds and seeds, and generates participant-level outputs and visualizations.

## ShallowConvNet

### `shallow-net-ic-95.ipynb`

This notebook reinfers the ShallowConvNet checkpoints. It includes `ShallowClassificationLoss`, which is required to deserialize the `fold_result.pkl` files produced by the original training notebook. The remaining reinference, aggregation, bootstrap, consensus, and export procedures follow the common participant-level protocol.

## T-GARNet

### `t-garnet-ic-95.ipynb`

This notebook reconstructs the T-GARNet architecture, discovers the 50 stored checkpoints, and performs complete out-of-fold reinference. It exports window and participant results, saved-versus-recomputed metric comparisons, subject-level heatmaps, and TikZ-compatible data in addition to the standardized participant-level files.

## IMC-BGT

### `im-cbgt-ic-95.ipynb`

This notebook performs complete repeated IMC-BGT training rather than checkpoint-only reinference. It uses exclusively the 120 participants defined in `folds.pkl`, with ten seeds and five subject-wise folds.

Feature standardization, PCA, and univariate feature selection are fitted using only the training participants within each fold. Checkpoints, window predictions, participant summaries, and metrics are saved as each fold is completed, allowing interrupted executions to resume without repeating finished folds.

## MultiStream

### `multistream-ic-95.ipynb`

This notebook does not train or load a neural network. It reads previously generated MultiStream exports from:

```text
/kaggle/input/notebooks/alejandragomezr/multistream/
```

If consolidated exports are unavailable, it searches for and combines the fold-level `subject_summary.csv` and `test_window_predictions.csv` files. Window-level metrics are calculated when the window predictions are available. The participant-level bootstrap and consensus exports follow the same protocol used for the other models.

## Data and model inputs

The reinference and training notebooks expect the EEG dataset to contain:

```text
<dataset_root>/
├── folds.pkl
└── ieee/
    ├── ADHD_group/*.mat
    └── Control_group/*.mat
```

CTE-Net, EEGNet, ShallowConvNet, and T-GARNet additionally require their saved checkpoint directories. IMC-BGT requires only the EEG data and fold definitions because it performs repeated training. MultiStream requires only its previously generated prediction and participant-summary exports.

All paths are configured for Kaggle and must be updated at the beginning of each notebook when running in another environment.

## Requirements

The notebooks collectively use:

* NumPy
* pandas
* SciPy
* scikit-learn
* Matplotlib
* PyTorch

GPU execution is recommended for checkpoint reinference and is strongly recommended for the repeated IMC-BGT training.

## Statistical interpretation

The bootstrap intervals quantify uncertainty at the participant level while preserving the dependence among the ten predictions available for each participant. They should not be interpreted as intervals obtained from 1,200 independent observations.

The model-specific notebooks include an exact McNemar helper for checking two consensus-prediction files. The final multiple-model inference is performed separately in `TEST/mcnemar-tests-cte-net.ipynb`, where Holm correction is applied across the five CTE-Net-versus-baseline comparisons.
