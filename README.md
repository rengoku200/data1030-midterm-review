# NYC Street Conditions: Predicting Closure Within 48 Hours

DATA1030 midterm project, Brown University, Fall 2026.  
Team: Jack Fei, Jason Uranta, and Baidy Mbaye.

We study whether a NYC Department of Transportation (DOT) Street Condition service request will receive a recorded administrative closure within 48 hours of submission. The project uses request-level records created in 2025, collected programmatically from NYC Open Data. The midterm work covers data collection, cleaning, labeling, and exploratory analysis. Model training and evaluation are later steps.

The saved labeled dataset contains **70,322 rows and 38 columns**. The binary target `closed_48h` is 1 for closure within 48 hours inclusive and 0 for later closure or a qualifying unresolved request. There are **44,355 positive** and **25,967 negative** labels. The threshold is a team choice; it is not an established city service guarantee. Administrative closure should not be interpreted as confirmed repair.

## Start here

- [Full data dictionary](data/data_dictionary.md): definitions and modeling roles for all 38 columns, units, cleaning decisions, target rules, missing values, and limitations.
- [Category inventory](data/category_inventory.csv): all observed categorical values, their counts, and meanings, including geographic codes.
- [Schema profile](data/schema_profile.csv): one row per column with semantic type and missingness.
- [Report with completed documentation appendix](report/Data_Midterm_Report_documented.pdf).
- [Appendix LaTeX source](report/appendix_data_documentation.tex) and [instructions](report/README.md).

## Repository structure

```text
data/       Raw monthly JSON, cleaned monthly CSVs, combined/labeled CSVs, documentation
figures/    EDA figures by day of week, borough, and month
results/    Reserved for future models, predictions, and evaluation outputs
report/     Midterm PDF and editable appendix LaTeX
src/        Collection/cleaning notebook and EDA notebook
.gitignore
environment.yml
LICENSE
README.md
```

`src/data_collection.ipynb` contains the API exploration, monthly collection helpers, cleaning checks, concatenation, and target creation. `src/eda_1.ipynb` reads the saved labeled CSV, derives calendar fields and a location-missing indicator, and creates exploratory plots. Historical-volume features and weekend status mentioned in the report remain planned; the committed EDA notebook does not create them.

## Data source and collection

- [NYC Open Data: 311 Service Requests from 2020 to Present](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data), dataset ID `erm2-nwe9`.
- API: `https://data.cityofnewyork.us/resource/erm2-nwe9.json`.
- Filters: `agency = 'DOT'`, `complaint_type = 'Street Condition'`, and creation dates from January 1, 2025 inclusive through January 1, 2026 exclusive.
- The collector requests monthly JSON records through `requests`, with ordered pages of 5,000 records in the automated helper. Raw JSONs and cleaned monthly CSVs are retained under `data/`.
- Six negative closure durations were excluded. Two records without enough information to assign an outcome were excluded. Pending/Open requests with missing closure dates were retained and labeled 0 under the follow-up assumption explained in the dictionary.

Monthly CSV filenames reflect the original workflow: January has no `_clean` suffix, February through November use `_clean`, and December uses `_clean_clean`. These are twelve separate monthly inputs, not an indication that December should be cleaned twice. `street_conditions_2025_combined.csv` has 70,324 rows before the two unlabelable records are removed; `street_conditions_2025_labeled.csv` has the final 70,322 rows. The monthly-checks CSV summarizes April through December only.

The API is updated over time. Use the committed snapshot to reproduce its counts. A later download can differ, and creation during 2025 does not require closure during 2025.

## Local setup and current reproducibility limits

Clone the repository, then create the supplied Conda environment:

```bash
git clone https://github.com/rengoku200/data1030-midterm-review.git
cd data1030-midterm-review
conda env create -f environment.yml
conda activate data1030-midterm
cd src
jupyter lab
```

Open `eda_1.ipynb` from `src/` so its `../data/` and `../figures/` paths resolve. The saved CSV can also be inspected directly:

```python
import pandas as pd

df = pd.read_csv(
    "../data/street_conditions_2025_labeled.csv",
    dtype={"unique_key": str, "incident_zip": str},
    parse_dates=["created_date", "closed_date", "resolution_action_updated_date"],
)
print(df.shape)  # Saved snapshot: (70322, 38)
print(df["closed_48h"].value_counts())
```

### Environment versions

The repository includes a pinned **starter environment**, listed below. The committed collection notebook records Python **3.14.6** in its metadata, which differs from that starter. Exact package versions from the original execution were not captured. Accordingly, the YAML is a setup starting point; these are **not verified versions of the original run**, and a clean end-to-end execution has not been established.

| Component | Starter `environment.yml` |
|---|---|
| Python | 3.11.10 |
| NumPy | 1.26.4 |
| pandas | 2.2.3 |
| Matplotlib | 3.9.2 |
| seaborn | 0.13.2 |
| scikit-learn | 1.5.2 |
| requests | 2.32.3 |
| JupyterLab | 4.2.5 |

To record the team's actual working environment, run this in that notebook kernel and use the output to update the YAML after verification:

```python
import sys
from importlib.metadata import version, PackageNotFoundError

print(sys.version)
for package in ["numpy", "pandas", "matplotlib", "seaborn", "scikit-learn", "requests", "jupyterlab"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed in this kernel")
```

### Collection notebook reruns

The collection notebook records an interactive development process and should be reviewed before using **Run All**. It uses `Path` before a later import, and its broad monthly-file glob can also match the already-created combined and labeled CSVs on a rerun. The automated collector writes numeric month filenames, whereas the saved monthly inputs have month names. Rerunning unchanged can therefore mix old and new inputs or count generated files twice. These code issues have been documented, not repaired in this documentation step. Work from the saved labeled snapshot for current EDA.

## Modeling boundary

Use only predictors that would be available when a new request is submitted. Exclude closure timestamps, closure duration, status, resolution text, and resolution-update time from predictors because they contain outcome information. Use the request ID for audit only. Candidate predictors and optional calendar features are specified in the dictionary; no final matrix, trained model, or predictive performance is claimed yet.

## License and attribution

Code is covered by the repository's [LICENSE](LICENSE). NYC Open Data is the source of the underlying records; the repository's code license does not change the city's data-use terms. Cite the dataset and retain its attribution when sharing results.
