# CTE-Net

## Contextualized Transfer Entropy Network for EEG-Based ADHD Classification

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Models-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-To%20be%20defined-lightgrey)](#license)

CTE-Net is an end-to-end deep-learning architecture for classifying
attention-deficit/hyperactivity disorder (ADHD) from pediatric
electroencephalography (EEG). It combines Transformer-based contextualization
with nonlinear temporal filtering, Takens delay-coordinate reconstruction, and
differentiable matrix-based Transfer Entropy (TE).

Unlike pipelines in which connectivity is computed as a fixed preprocessing
step, CTE-Net learns task-oriented representations and directed predictive
information dependencies jointly with the classifier. The resulting TE matrix
provides an explicit representation of nonlinear, time-delayed, and directional
interactions between EEG channels.

> **Research status:** this repository accompanies the manuscript
> *Transformer-Based Modeling of Directed Transfer Entropy Connectivity for
> EEG-Based ADHD Classification in Children*. This README reflects the revised manuscript submitted to Sensors, dated September 9, 2026. Final publication metadata should be added when available.

## Highlights

- End-to-end learning from multichannel EEG windows.
- Global content-based contextualization with a Transformer encoder.
- Channel-wise nonlinear temporal filtering.
- Takens delay-coordinate embeddings for source and target dynamics.
- Differentiable Transfer Entropy based on Rényi's matrix entropy and a
  rational quadratic kernel.
- Explicit directed connectivity features for model inspection.
- Subject-wise evaluation designed to prevent participant leakage.
- Analysis of within-subject variability across the network stages.
- Comparisons with EEGNet, ShallowConvNet, T-GARNet, IMC-BGT, and MultiStream.
- Participant-level bootstrap confidence intervals and exact McNemar comparisons.
- Component ablations and signal-quality, structural, preprocessing, and reference sensitivity analyses.
- Exact published subject partitions and supplementary datasets S1–S4.

## Model overview

The processing stages are:

1. Multichannel EEG input: 19 channels × 512 samples.
2. Transformer contextualization and projection back to 19 channels.
3. Channel-wise nonlinear temporal filtering: 107 temporal samples per channel.
4. Takens reconstruction and differentiable kernel Transfer Entropy: 48 temporal anchors.
5. Flattening of 342 directed off-diagonal connections and binary classification.

For an EEG window \(\mathbf{X}\in\mathbb{R}^{C\times T}\), CTE-Net first
contextualizes the complete multichannel sequence. The filtered signals are
then reconstructed into source-past, target-past, and target-present states.
For every ordered electrode pair, the TE layer estimates the predictive
information transferred from the source to the target beyond the information
already contained in the target's own history.

The estimated values should be interpreted as **directed predictive
dependencies**, not as definitive evidence of causal influence.

## Dataset and preprocessing

The experiments use the public
[EEG Data for ADHD/Control Children](https://ieee-dataport.org/open-access/eeg-data-adhd-control-children)
dataset.

| Property | Experimental setting |
| --- | --- |
| Analyzed cohort | 120 participants: 60 ADHD and 60 controls |
| Age range | 7–12 years |
| EEG montage | 19 channels, international 10–20 system |
| Sampling rate | 128 Hz |
| Task | Visual continuous-performance task |
| Window length | 4 s (512 samples) |
| Window overlap | 50% |
| Primary preprocessing condition | Original A1/A2 reference; no additional artifact rejection, ICA, frequency filtering, or band decomposition |
| Additional sensitivity conditions | Frequency filtering with quality screening; common-average reference |
| Total windows | 8,213 |
| Evaluation split | Five fixed stratified subject-wise folds |
| Repetitions | Ten random seeds; 50 trained models in total |

The original dataset contains 121 children (61 ADHD and 60 controls). One ADHD participant was randomly excluded before windowing, partitioning, optimization, and evaluation to define the balanced cohort used for all models. Participant-linked age and sex metadata and medication status during EEG acquisition were unavailable; group-level information cannot support participant-level adjustment.

The dataset is not redistributed in this repository. Download it from the
original source and place it under `data/raw/` as described in
[Prepare the data](#4-prepare-the-data). Keep every participant exclusively in
one training, validation, or test subset to avoid subject-level information
leakage.

## Architecture configuration

The fixed configuration below follows Table 2 of the revised manuscript.

| Stage | Main configuration |
| --- | --- |
| Input | 19 channels, 512 samples (4 s at 128 Hz) |
| Input projection | Embedding dimension 128 |
| Transformer | 1 layer, 1 attention head, head dimension 128, feed-forward dimension 128, dropout 0.5 |
| Channel projection | 128 → 19 channels |
| Temporal filter | Channel-wise Conv1D, kernel size 83, stride 1, average pooling 4; output length 107 |
| Takens embedding | Source dimension $D_x=6$, target dimension $D_y=1$, delay $\tau=2$, interaction lag $\mu=2$; 48 valid temporal anchors |
| Kernel TE | Rational quadratic kernel with fixed $a=\ell=\alpha_{RQ}=1$; Rényi order $\alpha_R=2$; trainable linear projections before kernel evaluation |
| Kernel matrices | 48 × 48 per channel and reconstructed state |
| Connectivity features | 19 × 19 TE matrix; 342 off-diagonal directed connections |
| Classifier | Dense layer with 64 units, dropout 0.5, one sigmoid output |

## Repository structure

| Location | Contents |
| --- | --- |
| [`Models/`](Models/) | CTE-Net and baseline notebooks: `tdha-CTE-Net.ipynb`, `EEGNet-Pytorch.ipynb`, `Shallow-Pytorch.ipynb`, `T-Garnet.ipynb`, `IM-CBGT.ipynb`, and `MultiStream.ipynb` |
| [`ablation/`](ablation/) | `ablation-without-transformer.ipynb` and `ablation-without-te.ipynb` |
| [`analysis/Interpretability/`](analysis/Interpretability/) | Connectivity inspection and representation characterization |
| [`analysis/Subjects/`](analysis/Subjects/) | Participant-level evaluation notebooks for CTE-Net and each baseline |
| [`folds.pkl`](folds.pkl) | Exact five-fold training, validation, and test assignments, supplied at the repository root |
| [`partitions/`](partitions/) | Partition documentation and an additional copy of the partition file |
| [`tests/`](tests/) | Statistical-analysis notebooks, post hoc sensitivity analyses, confusion-matrix exports, and the notebook smoke-test script |
| [`supplementary_material/`](supplementary_material/) | Supplementary Data S1–S4 and their documentation |
| [`requirements.txt`](requirements.txt) | Declared Python dependencies |

Original EEG recordings and generated model checkpoints are supplied locally.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/alegomezri/CTE-Net.git
cd CTE-Net
```

### 2. Create an isolated environment

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the data and exact partitions

1. Download the [EEG Data for ADHD/Control Children](https://ieee-dataport.org/open-access/eeg-data-adhd-control-children) dataset from IEEE DataPort.
2. Place the participant `.mat` files in `data/raw/ieee/ADHD_group/` and `data/raw/ieee/Control_group/`.
3. Copy `folds.pkl` from the repository root to `data/raw/folds.pkl`, the local path expected by the model notebooks. Run the following commands from the repository root (`CTE-Net/`).

Linux or macOS:

```bash
mkdir -p data/raw
cp folds.pkl data/raw/folds.pkl
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force data/raw
Copy-Item folds.pkl data/raw/folds.pkl
```

The root-level [`folds.pkl`](folds.pkl) contains five tuples of `(train_subjects, validation_subjects, test_subjects)`. Each fold includes 76 training, 20 validation, and 24 test participants. Every participant appears exactly once in a test set across the five folds. Use this file to reproduce the published assignments; generating a new split does not reproduce the same experiment. The `partitions/` directory also contains a copy and documentation; the instructions here use the root-level file as the source.

### 5. Run an experiment

```bash
jupyter lab
```

Open the desired notebook in `Models/` or `ablation/` and execute its cells in order. Reuse the fixed partitions and ten training seeds for all comparisons. Analysis and supplementary notebooks may require predictions, checkpoints, or paths produced by earlier experiments; inspect their input cells before running them.

The S4 notebooks are [`cte-net-filtering.ipynb`](supplementary_material/Supplementary%20Data%20S4/cte-net-filtering.ipynb) and [`cte-net-car.ipynb`](supplementary_material/Supplementary%20Data%20S4/cte-net-car.ipynb).

### 6. Optional execution check

```bash
pytest tests/test_notebooks_smoke.py
```

The script requests reduced settings through `CTE_NET_SMOKE_TEST=1` and requires the local dataset. It tests execution rather than agreement with published numerical results. The current script searches `Models/` and uppercase `Ablation/`; the repository uses lowercase `ablation/`, so ablation notebooks are not discovered on case-sensitive systems unless that path is corrected. This README update does not certify that the notebooks or dependency installation have been executed successfully.

## Evaluation protocol

- Five fixed stratified subject-wise folds, each with 76 training, 20 validation, and 24 test participants; no participant overlap within a fold.
- Ten random training seeds, yielding 50 model fits per architecture.
- Binary cross-entropy training, validation-based early stopping, and checkpoint selection.
- Twenty Optuna trials per architecture, with architecture-specific search spaces and a common validation objective. The selected configuration is fixed across folds and seeds; test metrics do not guide optimization.
- ADHD is the positive class, with a probability threshold of 0.5.
- Window-level metrics are averaged across the five test folds within each seed, then summarized as mean ± sample standard deviation across seeds.
- Participant-level probabilities are obtained by averaging out-of-fold window probabilities within each participant and seed. Point estimates are averaged across seeds. Confidence intervals use 5,000 stratified participant-level bootstrap resamples, applying the same resampled participant indices across all seeds.
- Primary between-model comparisons use one consensus decision per participant, obtained by averaging participant probabilities across seeds and thresholding at 0.5. Exact McNemar tests use Holm correction across the five baseline comparisons.
- Paired two-sided Wilcoxon signed-rank tests with Holm correction characterize seed-level optimization variability. Seeds are repeated model fits, not independent clinical observations.
- Ablation comparisons use Holm correction across two participant-level McNemar tests and six exploratory seed-level tests.

## Main results

### Window-level classification

Values are percentages, reported as mean ± sample standard deviation across ten seeds after averaging folds within each seed (manuscript Table 3).

| Model | Accuracy | Balanced accuracy | Sensitivity | Specificity | Precision | F1 | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CTE-Net | 80.9 ± 1.7 | 80.6 ± 1.8 | 84.2 ± 2.3 | 77.0 ± 3.2 | 82.7 ± 2.1 | 82.9 ± 1.5 | 87.9 ± 1.5 |
| EEGNet | 81.5 ± 2.1 | 81.4 ± 2.1 | 83.5 ± 3.6 | 79.3 ± 4.0 | 84.3 ± 2.2 | 83.1 ± 2.2 | 88.8 ± 2.5 |
| ShallowConvNet | 83.5 ± 1.7 | 83.7 ± 1.8 | 80.6 ± 2.4 | 86.9 ± 3.4 | 88.1 ± 2.9 | 83.2 ± 2.0 | 90.4 ± 1.7 |
| T-GARNet | 77.6 ± 0.5 | 76.7 ± 0.6 | 85.6 ± 1.1 | 67.8 ± 1.9 | 77.3 ± 0.8 | 80.8 ± 0.4 | 84.0 ± 0.4 |
| IMC-BGT | 66.3 ± 1.2 | 65.3 ± 1.4 | 74.7 ± 2.7 | 55.8 ± 4.5 | 68.2 ± 1.6 | 70.8 ± 1.0 | 71.2 ± 1.0 |
| MultiStream | 58.6 ± 0.3 | 55.2 ± 0.4 | 86.1 ± 0.9 | 24.4 ± 1.4 | 58.7 ± 0.3 | 69.8 ± 0.3 | 55.3 ± 0.4 |

### Participant-level classification

Values are percentages. Accuracy and ROC-AUC include 95% participant-bootstrap confidence intervals; full intervals for all metrics are reported in manuscript Table 5.

| Model | Accuracy (95% CI) | Sensitivity | Specificity | Precision | F1 | ROC-AUC (95% CI) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CTE-Net | 83.4 (78.2–88.2) | 86.0 | 80.8 | 81.8 | 83.8 | 90.2 (85.1–94.6) |
| EEGNet | 82.7 (77.7–87.3) | 87.2 | 78.2 | 80.1 | 83.4 | 89.2 (83.5–93.9) |
| ShallowConvNet | 84.7 (79.2–89.8) | 82.5 | 87.0 | 86.5 | 84.4 | 91.6 (86.6–95.7) |
| T-GARNet | 79.4 (72.5–85.8) | 90.3 | 68.5 | 74.2 | 81.4 | 85.8 (78.2–92.5) |
| IMC-BGT | 72.7 (66.3–78.8) | 85.3 | 60.0 | 68.3 | 75.8 | 78.6 (70.2–86.2) |
| MultiStream | 56.2 (51.2–61.4) | 93.7 | 18.8 | 53.6 | 68.2 | 60.3 (50.9–69.6) |

Exact participant-level McNemar tests with Holm correction found a significant advantage for CTE-Net only over MultiStream ($p_{Holm}=1.29\times10^{-6}$). Corrected p-values were 1.0000 for EEGNet, 1.0000 for ShallowConvNet, 0.1055 for T-GARNet, and 0.0502 for IMC-BGT. Nonsignificant differences do not establish equivalence. CTE-Net combines competitive classification with an explicit directed predictive connectivity representation.

### Ablation analysis

Window-level values are percentages (mean ± sample standard deviation). The last column reports the participant-level exact McNemar comparison with the complete model, corrected across the two ablations (Table 7).

| Variant | Accuracy | Sensitivity | Precision | Participant-level Holm p-value |
| --- | ---: | ---: | ---: | ---: |
| Without Transformer | 73.4 ± 2.2 | 78.0 ± 2.8 | 75.7 ± 2.5 | 0.0338 |
| TE replaced by temporal mean pooling | 78.7 ± 0.8 | 82.3 ± 2.8 | 80.8 ± 1.6 | 0.2891 |
| Complete CTE-Net | 80.9 ± 1.7 | 84.2 ± 2.3 | 82.7 ± 2.1 | — |

Removing the Transformer produced the largest performance reduction. Replacing TE with pooling reduced the point estimates, but the participant-level difference was not significant after correction; its exploratory seed-level difference was significant only for accuracy ($p_{Holm}=0.0410$). The TE module additionally supplies the explicit directed-connectivity representation.

### Representation-space organization

| Representation | Window silhouette ↑ | Participant-centroid silhouette ↑ | Same/different-class distance ratio ↓ |
| --- | ---: | ---: | ---: |
| Raw EEG | 0.0558 | 0.0210 | 0.9887 |
| Transformer output | 0.0712 | 0.2640 | 0.7056 |
| Temporal filter | 0.1326 | 0.3316 | 0.6326 |
| **Transfer Entropy** | **0.2148** | **0.3557** | **0.6031** |

The directed TE representation yielded the lowest within-subject dispersion,
with a median reduction of **38.35%** relative to raw EEG. The result remained
consistent across alternative PCA dimensionalities and distance definitions.

## Sensitivity analyses and supplementary data

| Dataset | Contents and main observations |
| --- | --- |
| [S1](supplementary_material/Supplementary%20Data%20S1/) | Row-normalized window-level confusion matrices for CTE-Net and all baselines. |
| [S2](supplementary_material/Supplementary%20Data%20S2/) | Post hoc signal-quality assessment without retraining. The primary robust threshold flagged 358/8,213 windows (4.36%); excluding them changed window-level metrics by at most 0.51 percentage points and participant-level metrics by at most 0.17 percentage points. Alternative thresholds were also examined. |
| [S3](supplementary_material/Supplementary%20Data%20S3/) | Joint structural sensitivity for $D_x$, $D_y$, $\tau$, and $\mu$. Mean validation accuracy across 11 configurations ranged from 81.63% to 89.78% (median 86.20%). Alternatives were not evaluated under the repeated test protocol, so these results do not establish superior generalization or individual parameter effects. |
| [S4](supplementary_material/Supplementary%20Data%20S4/) | Filtering/quality-screening and CAR notebooks, prediction and metric exports, paired bootstrap comparisons, exact McNemar tests, and connectivity concordance analyses. |

In the manuscript, retraining after frequency filtering and quality screening reduced participant-level accuracy from 83.5% to 73.9% and ROC-AUC from 90.1% to 81.9%, while retaining all participants. This combined procedure changes both signal content and window selection; its effects should not be attributed to one component alone.

CAR preserved classification performance but yielded low concordance of detailed learned connectivity (mean Spearman correlation 0.070; strongest-connection Jaccard overlap 0.067). Predictive stability therefore does not imply reference-invariant connectivity.

**Current S4 export coverage:** both notebooks are present, but the checked performance, paired-difference, agreement, and connectivity-summary CSV exports identify CAR and the original A1/A2 condition. Separate Filtering performance exports are not identified in the current directory. The filtering results summarized above are reported in the manuscript; the public CSV inventory should not be treated as a complete export of both experiments. See the [supplementary README](supplementary_material/README.md) for file descriptions.

## Reproducibility notes

- Use the root-level `folds.pkl`, copied to `data/raw/folds.pkl`, to preserve the exact published subject assignments. Never randomly distribute windows from one participant across training, validation, and test subsets.
- Record condition, random seed, fold, checkpoint, and preprocessing settings for each run.
- Fit predictive preprocessing and quality-screening thresholds using training participants only. Validation data guide model selection; test data are reserved for evaluation.
- The representation-space analysis is a separate post hoc descriptive analysis: stage-specific standardization and PCA were fitted on out-of-fold test representations within each seed–fold. These transformations did not train the classifier or select its hyperparameters. The cosine-distance control omits PCA but still uses standardized features, so it does not establish independence from normalization.
- Distinguish window-level metrics, mean participant-level metrics across seeds, and consensus decisions used for McNemar tests.
- Keep the S2 post hoc exclusion analysis separate from S4 retraining experiments.
- The study uses one pediatric task-EEG cohort and does not establish external clinical validity or interventional causality.
- Source EEG data and trained checkpoints are not distributed with the supplementary CSV files.

## Citation

If this code contributes to your research, please cite the accompanying
manuscript. The bibliographic information below should be updated when the
article receives its final journal, volume, pages, and DOI.

```bibtex
@article{gomezrivera2026ctenet,
  title   = {Transformer-Based Modeling of Directed Transfer Entropy
             Connectivity for EEG-Based ADHD Classification in Children},
  author  = {Gomez-Rivera, A. and Pastrana-Cortes, J. D. and
             Alvarez-Meza, Andres M. and Gil-Gonzalez, J. and
             Cardenas-Pena, D.},
  year    = {2026},
  note    = {Manuscript under review}
}
```

## Repository provenance

This repository brings together the model, ablation, participant-level, interpretability, statistical, and supplementary workflows accompanying CTE-Net. Folder-specific README files describe the corresponding analyses.

## Authors

- **A. Gomez-Rivera** — Signal Processing and Recognition Group, Universidad Nacional de Colombia
- **J. D. Pastrana-Cortés** — Automatics Research Group, Universidad Tecnológica de Pereira
- **Andrés M. Álvarez-Meza** — Signal Processing and Recognition Group, Universidad Nacional de Colombia
- **J. Gil-Gonzalez** — Automatics Research Group, Universidad Tecnológica de Pereira
- **D. Cárdenas-Peña** — Automatics Research Group, Universidad Tecnológica de Pereira

## Funding

This work was supported by the research program *Alianza Científica con Enfoque
Comunitario para Mitigar Brechas de Atención y Manejo de Trastornos Mentales
Relacionados con Impulsividad en Colombia - ACEMATE*, grant 111091991908.

## Responsible use

CTE-Net is intended for research purposes. It is not a medical device and must
not be used as a stand-alone diagnostic system. ADHD assessment requires
qualified clinical evaluation and information from multiple sources.

## License

No `LICENSE` file is currently included in the repository. The accompanying article’s license does not automatically license the source code.

## Contact

For questions about the repository or the manuscript, please contact
[A. Gomez-Rivera](mailto:yeagomezri@unal.edu.co).
