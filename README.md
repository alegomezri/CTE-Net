CTE-Net

Contextualized Transfer Entropy Network for EEG-Based ADHD Classification



CTE-Net is an end-to-end deep-learning architecture for classifyingattention-deficit/hyperactivity disorder (ADHD) from pediatricelectroencephalography (EEG). It combines Transformer-based contextualizationwith nonlinear temporal filtering, Takens delay-coordinate reconstruction, anddifferentiable matrix-based Transfer Entropy (TE).

Unlike pipelines in which connectivity is computed as a fixed preprocessingstep, CTE-Net learns task-oriented representations and directed predictiveinformation dependencies jointly with the classifier. The resulting TE matrixprovides an explicit representation of nonlinear, time-delayed, and directionalinteractions between EEG channels.

Research status: this repository accompanies the manuscriptTransformer-Based Modeling of Directed Transfer Entropy Connectivity forEEG-Based ADHD Classification in Children. The code and documentation maychange while the manuscript is under review.

Highlights

End-to-end learning from multichannel EEG windows.

Global content-based contextualization with a Transformer encoder.

Channel-wise nonlinear temporal filtering.

Takens delay-coordinate embeddings for source and target dynamics.

Differentiable Transfer Entropy based on Rényi's matrix entropy and arational quadratic kernel.

Explicit directed connectivity features for model inspection.

Subject-wise evaluation designed to prevent participant leakage.

Analysis of within-subject variability across the network stages.

Comparisons with EEGNet, ShallowConvNet, T-GARNet, IMC-BGT, and MultiStream.

Model overview

flowchart TD
    A["EEG window<br/>19 × 512"] --> B["Transformer<br/>contextualization"]
    B --> C["Channel-wise nonlinear<br/>temporal filtering"]
    C --> D["Takens delay-coordinate<br/>reconstruction"]
    D --> E["Differentiable directed<br/>Transfer Entropy"]
    E --> F["Connectivity matrix<br/>19 × 19"]
    F --> G["Binary classifier<br/>ADHD vs. control"]

For an EEG window (\mathbf{X}\in\mathbb{R}^{C\times T}), CTE-Net firstcontextualizes the complete multichannel sequence. The filtered signals arethen reconstructed into source-past, target-past, and target-present states.For every ordered electrode pair, the TE layer estimates the predictiveinformation transferred from the source to the target beyond the informationalready contained in the target's own history.

The estimated values should be interpreted as directed predictivedependencies, not as definitive evidence of causal influence.

Dataset and preprocessing

The experiments use the publicEEG Data for ADHD/Control Childrendataset.

Property

Experimental setting

Analyzed cohort

120 participants: 60 ADHD and 60 controls

Age range

7–12 years

EEG montage

19 channels, international 10–20 system

Sampling rate

128 Hz

Task

Visual continuous-performance task

Window length

4 s (512 samples)

Window overlap

50%

Additional preprocessing

No artifact rejection, ICA, frequency filtering, or band decomposition

Evaluation split

Five fixed stratified subject-wise folds

Repetitions

Ten random seeds; 50 trained models in total

The dataset is not redistributed in this repository. Download it from theoriginal source and update the dataset paths in the corresponding notebooks.Keep every participant exclusively in one training, validation, or test subsetto avoid subject-level information leakage.

Architecture configuration

Stage

Main configuration

Input

(C=19), (T=512)

Transformer

2 layers, 2 attention heads, embedding size 32, feed-forward size 256, dropout 0.4

Temporal filter

Depthwise Conv1D, kernel size 99, stride 1, average pooling 4

Takens embedding

(D_x=4), (D_y=2), delay (\tau=5), prediction horizon (\mu=5)

Kernel TE

Rational quadratic kernel, (\alpha_{\mathrm{RQ}}=1), Rényi order (\alpha_R=2)

Classifier

Dense layer with 128 units, dropout 0.1, one sigmoid output

Repository structure

CTE-Net/
├── Models/
│   ├── EEGNet-Pytorch.ipynb
│   ├── IM-CBGT.ipynb
│   ├── MultiStream.ipynb
│   ├── Shallow-Pytorch.ipynb
│   ├── T-Garnet.ipynb
│   ├── tdha-t-tekt...ipynb
│   └── tdha-t-tektnet-2.ipynb
└── README.md

The Models/ directory contains the proposed model experiments and thebaseline implementations used in the comparative evaluation. Some notebookfilenames retain their original experimental names; consult the first Markdowncell of each notebook for its model and purpose.

Getting started

1. Clone the repository

git clone https://github.com/alegomezri/CTE-Net.git
cd CTE-Net

2. Create an isolated environment

python -m venv .venv

Activate it on Linux or macOS:

source .venv/bin/activate

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

3. Install the dependencies

The notebooks use deep-learning, scientific-computing, optimization, and EEGanalysis libraries. Install the packages required by the notebook you intendto run. A typical environment includes:

pip install jupyter numpy pandas scipy scikit-learn matplotlib seaborn \
    torch optuna

If a notebook uses TensorFlow/Keras or additional EEG utilities, install thosedependencies as indicated by its import cells. A pinned requirements.txt isrecommended for exact reproduction.

4. Prepare the data

Download the dataset from IEEE DataPort.

Store it outside version control.

Update the input and output paths in the selected notebook.

Verify that subject identifiers are retained before generating the folds.

Suggested local layout:

CTE-Net/
├── data/                 # ignored by Git
│   └── raw/
├── Models/
└── results/

5. Run an experiment

jupyter lab

Open the desired notebook under Models/ and execute its cells in order. For afair comparison, reuse the same subject-wise partitions, preprocessing,validation protocol, and random seeds for every model.

Evaluation protocol

Five-fold stratified group cross-validation.

Twenty-four participants held out for testing in each fold.

Subject-independent training, validation, and test subsets.

Binary cross-entropy optimization with early stopping.

Validation-based checkpoint selection.

Hyperparameter optimization with 20 Optuna trials and pruning.

ADHD treated as the positive class.

Window-level decision threshold of 0.5.

Metrics averaged across the five folds for each seed and summarized acrossten seeds.

Paired two-sided Wilcoxon signed-rank tests with Holm correction for modelcomparisons.

Main results

Window-level classification

Model

Accuracy (%)

Precision (%)

Recall (%)

EEGNet

81.5 ± 2.1

84.3 ± 2.2

83.5 ± 3.6

ShallowConvNet

84.1 ± 1.7

88.0 ± 2.9

81.7 ± 2.4

T-GARNet

77.4 ± 0.5

76.9 ± 0.8

85.5 ± 1.1

IMC-BGT

66.1 ± 1.2

68.2 ± 1.4

74.4 ± 3.4

MultiStream

58.6 ± 0.6

58.7 ± 0.3

86.5 ± 2.2

CTE-Net

80.7 ± 1.7

82.2 ± 2.1

84.0 ± 2.3

CTE-Net was statistically comparable to EEGNet across accuracy, precision, andrecall. ShallowConvNet achieved higher accuracy and precision, whereas CTE-Netoutperformed T-GARNet, IMC-BGT, and MultiStream in accuracy and precision underthe reported corrected comparisons. The principal contribution of CTE-Net istherefore not a claim of uniform predictive superiority, but the combination ofcompetitive classification with an explicit nonlinear and directedconnectivity representation.

Representation-space organization

Representation

Window silhouette ↑

Participant-centroid silhouette ↑

Same/different-class distance ratio ↓

Raw EEG

0.0558

0.0210

0.9887

Transformer output

0.0712

0.2640

0.7056

Temporal filter

0.1326

0.3316

0.6326

Transfer Entropy

0.2148

0.3557

0.6031

The directed TE representation yielded the lowest within-subject dispersion,with a median reduction of 38.35% relative to raw EEG. The result remainedconsistent across alternative PCA dimensionalities and distance definitions.

Reproducibility notes

Do not randomly split individual EEG windows across subsets.

Record the random seed, fold, checkpoint, and preprocessing configuration foreach run.

Fit transformations used for evaluation, including standardization and PCA,without access to held-out participant information.

Keep dataset files, checkpoints, and generated results out of Git unless theirredistribution is permitted.

Report whether results correspond to window-level or participant-leveldecisions.

Citation

If this code contributes to your research, please cite the accompanyingmanuscript. The bibliographic information below should be updated when thearticle receives its final journal, volume, pages, and DOI.

@article{gomezrivera2026ctenet,
  title   = {Transformer-Based Modeling of Directed Transfer Entropy
             Connectivity for EEG-Based ADHD Classification in Children},
  author  = {Gomez-Rivera, A. and Alvarez-Meza, Andres M. and
             Cardenas-Pena, D.},
  year    = {2026},
  note    = {Manuscript under review}
}

Authors

A. Gomez-Rivera — Signal Processing and Recognition Group, UniversidadNacional de Colombia

Andrés M. Álvarez-Meza — Signal Processing and Recognition Group,Universidad Nacional de Colombia

D. Cárdenas-Peña — Automatics Research Group, Universidad Tecnológica dePereira

Funding

This work was supported by the research program Alianza Científica con EnfoqueComunitario para Mitigar Brechas de Atención y Manejo de Trastornos MentalesRelacionados con Impulsividad en Colombia - ACEMATE, grant 111091991908.

Responsible use

CTE-Net is intended for research purposes. It is not a medical device and mustnot be used as a stand-alone diagnostic system. ADHD assessment requiresqualified clinical evaluation and information from multiple sources.

License

No software license has yet been specified. Add a LICENSE file beforeredistributing or accepting external contributions. The license of theaccompanying article does not automatically define the license of this sourcecode.

Contact

For questions about the repository or the manuscript, please contactA. Gomez-Rivera.
