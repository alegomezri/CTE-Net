# Fixed Subject Partitions

This directory contains the exact subject-level partitions used in all experiments reported in the manuscript.

## File

* `folds.pkl`: fixed training, validation, and test partitions for the five-fold subject-wise evaluation.

The file contains a Python list with five elements. Each element is a tuple with the following structure:

```python
(train_subjects, validation_subjects, test_subjects)
```

Each fold contains:

* 76 training participants
* 20 validation participants
* 24 test participants

The training, validation, and test subsets are mutually exclusive within each fold and jointly contain all 120 participants. Across the five folds, every participant appears exactly once in the test set.

The same fixed partitions were used for CTE-Net, all baseline models, all ablation experiments, and all ten random seeds. This subject-wise design prevents EEG windows from the same participant from appearing in more than one subset within a given fold.

## Using the partitions

The experiment notebooks load the partition file from:

```text
data/raw/folds.pkl
```

After cloning the repository, copy the provided file to the expected local path:

```bash
mkdir -p data/raw
cp partitions/folds.pkl data/raw/folds.pkl
```

On Windows PowerShell, use:

```powershell
New-Item -ItemType Directory -Force data/raw
Copy-Item partitions/folds.pkl data/raw/folds.pkl
```

No modification of the experiment notebooks is required.

## Data availability

The `folds.pkl` file contains only participant identifiers and their assigned experimental subsets. It does not contain or redistribute any EEG recordings.

The original EEG recordings are publicly available from the [EEG Data for ADHD/Control Children](https://ieee-dataport.org/open-access/eeg-data-adhd-control-children) dataset. Download and organization instructions are provided in the main repository README.

