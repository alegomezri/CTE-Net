# CTE-Net ablation experiments

This directory contains the two component-wise ablation experiments used to examine the predictive contribution of the Transformer and Transfer Entropy (TE) branches in CTE-Net. Both variants retain the original subject-wise experimental protocol and generate out-of-fold predictions for subsequent paired statistical comparisons.

## Notebooks

| Notebook | Removed component | Retained processing flow |
| --- | --- | --- |
| `ablation-without-transformer.ipynb` | Transformer contextualization block | `EEG → nonlinear temporal filter → Takens reconstruction → kernels → Transfer Entropy → classifier` |
| `ablation-without-te.ipynb` | Complete Transfer Entropy branch | `EEG → Transformer → channel projection → deterministic temporal pooling → classifier` |

## Shared experimental protocol

Both ablation experiments use:

* The same participants and predefined subject-wise partitions stored in `folds.pkl`.
* Five mutually exclusive subject-wise test folds.
* Ten base seeds (`0`–`9`), producing 50 trained models per ablation.
* Fixed model hyperparameters applicable to the components retained in each architecture.
* No additional Optuna search.
* No weights transferred from the complete CTE-Net model.
* Model-weight initialization with seed 42 in every fold, matching the effective protocol of the presented CTE-Net experiments.
* Training DataLoader shuffling with `base_seed + fold_id`.
* Adam optimization and a `ReduceLROnPlateau` scheduler.
* A maximum of 100 epochs, batch size 16, and early stopping after 25 epochs without sufficient validation-loss improvement.
* Selection and restoration of the best checkpoint using validation loss only.
* A probability threshold of 0.5, with ADHD treated as the positive class.
* Direct window-level evaluation without majority voting.

For each seed, the test metrics are first averaged across the five folds. The final results are reported as the mean and sample standard deviation across the ten seed-level averages.

## Ablation without the Transformer

### `ablation-without-transformer.ipynb`

This experiment removes only the Transformer contextualization block. The nonlinear temporal filter, Takens reconstruction, learned Takens-state projections, kernel layers, differentiable TE estimator, diagonal removal, matrix vectorization, and classifier are retained.

The temporal filter is applied directly to the original channel-indexed EEG window before the Takens and TE operations. No multi-head attention, Transformer feedforward layer, Transformer residual normalization, or Transformer-to-channel projection is instantiated.

### Output directory

On Kaggle, results are saved to:

```text
/kaggle/working/ablation_without_transformer_repeated_10seeds/
```

Outside Kaggle, the default output directory is:

```text
../results/ablation_without_transformer_repeated_10seeds/
```

### Main aggregate outputs

| File | Description |
| --- | --- |
| `WithoutTransformer_window_level_metrics_by_fold.csv` | Window-level metrics for every seed and test fold. |
| `WithoutTransformer_window_level_metrics_by_seed.csv` | Five-fold mean metrics within each seed. |
| `WithoutTransformer_window_level_metrics_mean_std.csv` | Mean and sample standard deviation across ten seeds. |
| `WithoutTransformer_all_window_predictions.csv` | Complete out-of-fold window probabilities and predictions. |
| `WithoutTransformer_repeated_protocol_summary.json` | Experimental configuration and execution summary. |
| `WithoutTransformer_subject_level_predictions_by_seed.csv` | Participant probabilities obtained by averaging windows within each seed. |
| `WithoutTransformer_subject_level_metrics_by_seed.csv` | Participant-level metrics calculated separately for each seed. |
| `WithoutTransformer_subject_level_consensus_predictions.csv` | One consensus probability and prediction per participant after averaging across seeds. |

Each `seed_<n>/` subdirectory also stores the fold-specific checkpoints, learning history, validation predictions, test predictions, and fold metrics required for safe resumption and inspection.

## Ablation without the Transfer Entropy module

### `ablation-without-te.ipynb`

This experiment retains the Transformer and removes the entire branch designed to estimate directed TE. The removed components are:

* Nonlinear temporal filter \(\phi\).
* Takens delay-coordinate reconstruction.
* Learned Takens-state projections.
* Rational Quadratic or Gaussian kernel layers.
* Differentiable Transfer Entropy layer.
* Diagonal removal and TE-matrix vectorization.

After Transformer contextualization and projection back to the 19 channel coordinates, a deterministic temporal mean-pooling layer divides each 512-sample representation into 18 contiguous blocks of 28 samples. The final eight samples are discarded, and the mean of each block is retained. This produces `19 × 18 = 342` classifier input features without introducing trainable replacement parameters, matching the dimensionality of the off-diagonal TE vector used by the complete model.

### Output directory

On Kaggle, results are saved to:

```text
/kaggle/working/ablation_without_te_repeated_10seeds/
```

Outside Kaggle, the default output directory is:

```text
../results/ablation_without_te_repeated_10seeds/
```

### Main aggregate outputs

| File | Description |
| --- | --- |
| `WithoutTE_window_level_metrics_by_fold.csv` | Window-level metrics for every seed and test fold. |
| `WithoutTE_window_level_metrics_by_seed.csv` | Five-fold mean metrics within each seed. |
| `WithoutTE_window_level_metrics_mean_std.csv` | Mean and sample standard deviation across ten seeds. |
| `WithoutTE_all_window_predictions.csv` | Complete out-of-fold window probabilities and predictions. |
| `WithoutTE_repeated_protocol_summary.json` | Experimental configuration and execution summary. |
| `WithoutTE_subject_level_predictions_by_seed.csv` | Participant probabilities obtained by averaging windows within each seed. |
| `WithoutTE_subject_level_metrics_by_seed.csv` | Participant-level metrics calculated separately for each seed. |
| `WithoutTE_subject_level_consensus_predictions.csv` | One consensus probability and prediction per participant after averaging across seeds. |

Each `seed_<n>/` subdirectory also contains the fold-specific checkpoints, learning history, validation predictions, test predictions, and fold metrics.

## Data structure

The notebooks expect the dataset root to contain:

```text
<dataset_root>/
├── folds.pkl
└── ieee/
    ├── ADHD_group/*.mat
    └── Control_group/*.mat
```

The EEG recordings are segmented into windows of 512 samples with 50% overlap. Participant membership is determined exclusively from `folds.pkl`; participants are not manually added to or removed from the experimental cohort.

The notebooks search for the data in the following order:

1. The path provided through `CTE_NET_DATA_ROOT`.
2. The configured Kaggle dataset path.
3. The local fallback `../data/raw/`.

## Execution controls

* Set `CTE_NET_DATA_ROOT` to run with a custom dataset location.
* Set `CTE_NET_SMOKE_TEST=1` to run only base seed 0 as a quick execution check.
* Keep `FORCE_RETRAIN=False` to reuse completed folds and train only missing folds.
* Set `FORCE_RETRAIN=True` only when all stored fold results must be replaced.

## Requirements

The notebooks were developed for a Kaggle Python environment and use:

* NumPy
* pandas
* SciPy
* scikit-learn
* PyTorch

GPU execution is recommended because each complete experiment trains 50 models.

## Subsequent statistical analysis

The aggregate window-prediction files generated by these notebooks are used by `TEST/ablation-test.ipynb`. That notebook verifies that the complete and ablated models contain identical participants and test partitions, reconstructs the evaluation metrics, performs paired Wilcoxon tests across matched seeds, and performs exact McNemar tests using participant-level consensus decisions.

Random seeds represent computational repetitions rather than independent clinical observations. Therefore, the seed-level Wilcoxon analysis evaluates consistency across model initializations, while the participant-level McNemar analysis is the primary paired inferential comparison.
