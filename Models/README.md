# Model training and repeated evaluation

This directory contains the PyTorch notebooks used to train CTE-Net and the five baseline models evaluated in the manuscript *Transformer-Based Modeling of Directed Transfer Entropy Connectivity for EEG-Based ADHD Classification in Children*.

## Notebooks

| Notebook | Model | Main implementation |
| --- | --- | --- |
| `tdha-CTE-Net.ipynb` | CTE-Net | Transformer contextualization, projection to channel-indexed coordinates, nonlinear temporal filtering, Takens reconstruction, kernel-based differentiable directed Transfer Entropy, and classification. |
| `T-Garnet.ipynb` | T-GARNet | Transformer encoder, Gaussian-kernel representation, Rényi-entropy regularization, convolutional processing, and classification. |
| `Shallow-Pytorch.ipynb` | ShallowConvNet | Temporal and spatial convolutions followed by nonlinear activation, average pooling, dropout, and a linear classifier. |
| `MultiStream.ipynb` | MultiStream | Separate Transformer encoders for spectral, temporal, and spatial EEG representations, followed by feature fusion and classification. |
| `IM-CBGT.ipynb` | IMC-BGT | Handcrafted EEG feature extraction, fold-specific feature preprocessing, and fusion of CNN, CNN–BiLSTM, and GRU–self-attention branches. |
| `EEGNet-Pytorch.ipynb` | EEGNet | Temporal convolution, depthwise spatial convolution, separable convolution, average pooling, and classification. |

The filenames above are the recommended repository names after removing upload-copy suffixes.

## Shared data preparation

The notebooks load the ADHD and control EEG recordings from MATLAB files and divide each recording into windows of 512 samples with 50% overlap. The resulting standard neural-network input has shape:

```text
(windows, 19 channels, 512 samples)
```

At the dataset sampling rate of 128 Hz, each window corresponds to 4 seconds. MultiStream derives three representations from every window:

* A spectral stream based on Welch power estimates in 20 log-spaced frequency bands.
* A temporal stream based on ten consecutive time blocks.
* A spatial stream containing the root-mean-square value of each channel.

IMC-BGT instead extracts statistical, Hjorth, and spectral features. Its standardization, PCA, and univariate feature-selection steps are fitted exclusively on the training portion of each fold and then applied to the corresponding validation and test data.

## Experimental protocol

All models use the predefined participant-wise partitions stored in `folds.pkl`. Each fold contains separate training, validation, and test participant lists; windows from one participant are therefore not divided among these subsets.

The final repeated evaluation uses:

* Five fixed participant-wise folds.
* Ten base random seeds (`0`–`9`).
* One model trained and tested for every seed–fold combination, giving 50 held-out test evaluations per architecture.
* A maximum of 100 epochs and a batch size of 16.
* Validation-loss checkpoint selection and early stopping.
* Automatic CUDA use when a compatible GPU is available.
* Deterministic random-seed controls where supported by PyTorch.

The notebooks save fold checkpoints and intermediate results so that completed work can be inspected or reused. The `force_retrain` variable controls whether existing fold outputs are replaced.

## Hyperparameter selection

CTE-Net and T-GARNet include an Optuna study with a target of 20 completed trials. The objective is the mean validation accuracy across the predefined training/validation partitions. The selected configuration is then fixed and used for the ten-seed repeated evaluation.

The Optuna search is performed once and is not repeated as an independently nested search inside every outer test fold. The ShallowConvNet, MultiStream, IMC-BGT, and EEGNet notebooks use the fixed configurations encoded in their evaluation sections and do not perform a new Optuna search.

## Model-specific notes

### `tdha-CTE-Net.ipynb`

This notebook defines the complete proposed architecture. A Transformer first contextualizes the EEG window across its channel coordinates. The representation is projected back to 19 channel-indexed coordinates and passed through a nonlinear temporal filter, Takens delay-coordinate reconstruction, learned projections, and kernel layers. The differentiable TE layer produces a directed `19 × 19` matrix; after removal of the diagonal, the 342 directed coefficients are supplied to the classifier.

The notebook contains both the Optuna model-selection stage and the repeated evaluation with the selected hyperparameters. Study journals, resumable trial caches, best-fold weights, repeated fold metrics, and aggregate summaries are written under `../results/`.

### `T-Garnet.ipynb`

This notebook implements T-GARNet with Transformer contextualization, a Gaussian-kernel channel matrix, Rényi-entropy regularization, and a convolutional classification head. It contains a 20-trial Optuna stage followed by the ten-seed, five-fold evaluation with the selected configuration.

### `Shallow-Pytorch.ipynb`

This notebook implements the ShallowConvNet baseline in PyTorch, including its temporal and spatial convolutions and max-norm constraints. It runs a fixed-seed check and the complete repeated evaluation using a fixed configuration.

### `MultiStream.ipynb`

This notebook constructs the spectral, temporal, and spatial input streams before training three parallel Transformer encoders. Their encoded vectors are concatenated and passed to the final classifier. The notebook includes a fixed-seed run and the complete repeated evaluation.

### `IM-CBGT.ipynb`

This notebook extracts EEG features and applies fold-specific standardization, PCA, and chi-square feature selection. The selected feature sequence is processed by three parallel branches—CNN, CNN–BiLSTM, and GRU with self-attention—whose outputs are fused for classification. The notebook includes a fixed-seed run and the complete repeated evaluation.

### `EEGNet-Pytorch.ipynb`

This notebook implements EEGNet in PyTorch with same-padded temporal convolution, depthwise spatial convolution, separable convolution, max-norm constraints, and a two-class output layer. It includes a fixed-seed run and the complete repeated evaluation.

## Expected repository structure

The default relative paths assume the following layout:

```text
project_root/
├── MODELS/
│   ├── tdha-CTE-Net.ipynb
│   ├── T-Garnet.ipynb
│   ├── Shallow-Pytorch.ipynb
│   ├── MultiStream.ipynb
│   ├── IM-CBGT.ipynb
│   └── EEGNet-Pytorch.ipynb
├── data/
│   └── raw/
│       ├── folds.pkl
│       └── ieee/
│           ├── ADHD_group/*.mat
│           └── Control_group/*.mat
└── results/
```

Update the path variables in the corresponding notebook if the data or output directories are stored elsewhere.

## Main outputs

The exact output directory is model-specific, but all repeated-evaluation sections generate:

| Output | Description |
| --- | --- |
| `repeated_test_results.csv` | One row of held-out window-level metrics for each seed and fold. |
| `repeated_test_summary.json` | Experimental configuration and global, fold-specific, and seed-specific summaries. |
| `repeat_seed_<n>/` or equivalent | Fold checkpoints, training histories, cached results, and model weights for a single base seed. |

The fixed-seed sections of EEGNet, ShallowConvNet, MultiStream, and IMC-BGT additionally save `summary_results.json` and `summary_results.pkl`. The CTE-Net and T-GARNet model-selection sections also save the Optuna journal, trial-resumption cache, and weights associated with the selected trial.

Depending on the model, the reported window-level measures include accuracy, balanced accuracy, sensitivity/recall, precision, Cohen's kappa, and ROC-AUC. Aggregate values are summarized across the 50 seed–fold evaluations and also grouped by fold and seed.

## Requirements

The notebooks were developed with Python 3.10 and collectively require:

* NumPy
* pandas
* SciPy
* scikit-learn
* PyTorch
* Optuna
* torchinfo

GPU execution is strongly recommended, particularly for the Optuna studies and the complete ten-seed repeated evaluations.

## Downstream analyses

The outputs generated here are consumed by the notebooks in `SUBJECTS/`, `TEST/`, `ABLATION/`, and `INTERPRETABILITY/` for participant-level evaluation, paired statistical comparisons, ablation testing, Transfer Entropy stability assessment, and qualitative model interpretation.
