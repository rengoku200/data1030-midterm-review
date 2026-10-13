# DATA1030 Midterm Project

Brown University | DATA1030 | Fall 2026

## Overview
//TBD

## Repository structure

| Directory | Contents |
| --- | --- |
| `data/` | Raw and preprocessed data, plus data documentation |
| `figures/` | Generated exploratory and explanatory figures |
| `results/` | Predictions, saved models, and evaluation results |
| `report/` | Team-authored midterm PDF and final presentation slides |
| `src/` | Python scripts and Jupyter notebooks |

Root files include `.gitignore`, `LICENSE`, `README.md`, and `environment.yml`.

## Setup
//TBD

```bash
conda env create -f environment.yml
conda activate data1030-midterm
jupyter lab
```

Imports and Versions: Python 3.11.10, NumPy 1.26.4, pandas 2.2.3, Matplotlib 3.9.2, seaborn 0.13.2, scikit-learn 1.5.2, requests 2.32.3, JupyterLab 4.2.5.

## Workflow
1. Agree on a research question, data source, and supervised prediction target.
2. Collect data through an API, website scraping, PDF extraction, or another method requiring coding effort. Ready-made downloadable datasets are not accepted by the rubric.
3. Preserve collection code, query parameters, timestamps, and raw data.
4. Complete `data/data_dictionary.md`, including feature types, units, categorical values, and ordinal ordering.
5. Validate records, handle missing values, and create explanatory visualizations.
6. Define a prediction task with features available at deployment time.
7. Review and cite related research and data sources.
8. Develop and evaluate course models for the final presentation.

If data is too large for GitHub, document the source link and exact download command or notebook instead. Do not commit credentials or confidential data.

## Midterm requirements
- Public repository with all team members added as collaborators.
- Title, team names, affiliation, and GitHub link at the beginning of the report.
- Required sections: Introduction; Data; Exploratory Data Analysis; Problem description and potential impact; References.
- Maximum 1,500 words excluding references and appendix.
- At least three explanatory figures, with captions, labeled axes, and clear messages.
- No code in the submitted report.
- The team writes the report; the rubric permits LLM help for grammatical errors and typos only.
- Submit the report PDF in `report/` and push all work before submission.

## Team
- 
- Other team members: Jason Uranta, Jack Fei , Baidy Mbaye 

