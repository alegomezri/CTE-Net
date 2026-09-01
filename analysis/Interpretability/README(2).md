# Interpretability

This directory contains the post hoc analyses used to characterize the directed Transfer Entropy (TE) representations learned by CTE-Net and to generate the connectivity visualizations accompanying the manuscript *Transformer-Based Modeling of Directed Transfer Entropy Connectivity for EEG-Based ADHD Classification in Children*.

## Notebooks

| Notebook | Purpose |
| --- | --- |
| `cte-net-characterization-of-transfer-entropy.ipynb` | Characterizes the distribution, range, negative values, and numerical validity of the off-diagonal TE coefficients obtained from the out-of-fold test representations. |
| `conectividades-cte-net.ipynb` | Computes participant- and group-level mean TE matrices and generates heatmaps and qualitative connectivity maps for selected correctly and incorrectly classified participants. |

## Characterization of Transfer Entropy values

### `cte-net-characterization-of-transfer-entropy.ipynb`

This notebook analyzes only the TE matrices from the held-out test partition of each of the five fixed subject-wise folds. Therefore, the analyzed representations are out-of-fold and correspond to data not used to train the model associated with each fold.

The diagonal is excluded because it was set to zero by construction. Nonfinite values are counted before the statistical analysis and are excluded only from the corresponding numerical summaries; the stored matrices are not modified.

### Analyses performed

* Automatic detection of the directory containing `fold_1` through `fold_5`.
* Verification that each TE array has shape `(n_windows, 19, 19)`.
* Extraction of all directed off-diagonal coefficients.
* Global characterization of the minimum, maximum, mean, standard deviation, median, and selected percentiles.
* Quantification of negative, zero, and nonfinite coefficients.
* Examination of the negative tail at thresholds ranging from `TE < 0` to `TE < -0.01`.
* Summaries by fold and by participant.
* Visualization of the complete distribution and its central 99%.

### Input data

The notebook expects one `.npz` file per participant inside the following structure:

```text
TE_matrices_all_folds_train_validation_test_diag_zero/
├── fold_1/test/<class>/*.npz
├── fold_2/test/<class>/*.npz
├── fold_3/test/<class>/*.npz
├── fold_4/test/<class>/*.npz
└── fold_5/test/<class>/*.npz
```

Each file must contain `TE_matrices`. The `subject_id` and `class_name` fields are used when available; otherwise, they are inferred from the filename and parent directory.

### Generated files

Results are saved to `/kaggle/working/te_value_characterization/`:

| File | Description |
| --- | --- |
| `TE_global_summary.csv` | Global descriptive statistics for all finite off-diagonal TE coefficients. |
| `TE_summary_by_fold.csv` | Descriptive statistics and negative-value counts for each test fold. |
| `TE_summary_by_subject.csv` | Participant-level TE summaries, including the number of windows and coefficients. |
| `TE_negative_tail.csv` | Number and percentage of coefficients below the evaluated negative thresholds. |
| `reviewer_numbers.txt` | Compact text summary containing the TE range, negative-value count, nonfinite-value count, median, and 1st–99th percentile interval. |

### Results from the saved execution

The saved execution processed 2,772,594 finite off-diagonal coefficients from 119 participant files. The coefficients ranged from `-0.08005744` to `0.51560783`; 278,901 coefficients (10.0592%) were negative, and no nonfinite values were observed. Negative coefficients were present in every analyzed participant file.

## Connectivity visualization

### `conectividades-cte-net.ipynb`

This notebook analyzes the TE matrices and classification outputs stored for the `fold_3/test` directory. It loads the Control and `TDAH` directories separately, verifies the channel order, and averages all window-level TE matrices belonging to the same participant.

Participant-level ADHD probabilities are calculated by averaging the window-level probabilities. A threshold of 0.5 is then used to obtain the participant-level prediction.

### Analyses performed

* Construction of participant-level mean TE matrices.
* Computation of the Control and ADHD group means after giving each participant equal weight.
* Visualization of the Control mean, ADHD mean, and ADHD-minus-Control difference matrices.
* Identification of correctly and incorrectly classified participants using only their mean classification probabilities.
* Visualization of four representative participant-level TE matrices.
* Generation of circular directed-connectivity diagrams after shared-range normalization.

### Participant-selection procedure

The connectivity matrices are not used to select the displayed participants. Selection is based exclusively on the mean predicted ADHD probability:

| Case | Selection rule | Participant in the saved execution |
| --- | --- | --- |
| Best Control | Lowest mean ADHD probability among Control participants | `v306` |
| Best ADHD | Highest mean ADHD probability among ADHD participants | `v284` |
| Misclassified Control | Highest mean ADHD probability among Control participants | `v297` |
| Misclassified ADHD | Lowest mean ADHD probability among ADHD participants | `v27p` |

The saved execution analyzed 24 participants from the selected test fold: 12 Control participants and 12 participants with ADHD.

### Input data

The notebook expects the following directories:

```text
TE_matrices_all_folds_train_validation_test_diag_zero/
└── fold_3/test/
    ├── Control/*.npz
    └── TDAH/*.npz
```

Each `.npz` file is expected to contain:

* `TE_matrices`
* `subject_id`
* `class_name`
* `label`
* `split`
* `fold`
* `channel_names`
* `y_window`
* `y_prob`
* `y_pred`
* `window_ids`
* `diagonal_zero`
* `diagonal_removed`

### Generated figures

The heatmaps and participant summaries are displayed within the notebook. The circular connectivity diagrams are saved as:

| File | Description |
| --- | --- |
| `best_control_v306_normalized.pdf` | Correctly classified Control participant with the lowest mean ADHD probability. |
| `best_tdah_v284_normalized.pdf` | Correctly classified ADHD participant with the highest mean ADHD probability. |
| `misclassified_control_v297_normalized.pdf` | Control participant with the highest mean ADHD probability. |
| `misclassified_tdah_v27p_normalized.pdf` | ADHD participant with the lowest mean ADHD probability. |

For each correctly classified or misclassified pair, the matrices are normalized using a shared minimum and maximum. The diagonal is reset to zero, and the circular plots use the 95th–100th percentile interval with a threshold of 0.1.

## Requirements

The notebooks were developed for a Kaggle Python environment and use:

* NumPy
* pandas
* Matplotlib
* `dunderlab.visualizations`
* `python-circos`, installed as a dependency of `dunderlab.visualizations`

The visualization package is installed in the connectivity notebook with:

```bash
pip install -U git+https://github.com/dunderlab/python-dunderlab.visualizations.git
```

Update the `ROOT` and `BASE_DIR` variables if the TE matrices are stored outside the Kaggle paths used in the notebooks. Before running the circular-plot cells, ensure that the base plotting-options dictionary named `arguments` is defined, because those cells create participant-specific settings with `arguments.copy()`.

## Interpretation scope

The TE coefficients are computed after Transformer contextualization and projection back to a channel-indexed representation. Consequently, a labeled coefficient such as F8→C4 represents a directed predictive dependency between channel-indexed coordinates of the learned contextualized representation. It should not be interpreted as conventional Transfer Entropy calculated directly between the original F8 and C4 electrode signals or as a source-level cortical interaction.

The participant-level connectivity maps are qualitative illustrations of model behavior. They are not intended to establish group-level neurophysiological differences, and their displayed channel labels should be interpreted within the learned representation rather than as direct evidence of anatomically localized information transfer.
