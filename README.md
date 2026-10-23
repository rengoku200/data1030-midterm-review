# NYC Street Conditions: Predicting Closure Within 48 Hours

DATA1030 midterm project, Brown University, Fall 2026.  
Team: Jack Fei, Jason Uranta, and Baidy Mbaye.

We study whether a NYC Department of Transportation (DOT) Street Condition service request will receive a recorded administrative closure within 48 hours of submission. The project uses request-level records created in 2025, collected programmatically from NYC Open Data. The midterm work covers data collection, cleaning, labeling, and exploratory analysis. Model training and evaluation are later steps.

The saved labeled dataset contains **70,322 rows and 38 columns**. The binary target `closed_48h` is 1 for closure within 48 hours inclusive and 0 for later closure or a qualifying unresolved request. There are **44,355 positive** and **25,967 negative** labels. The threshold is a team choice; it is not an established city service guarantee. Administrative closure should not be interpreted as confirmed repair.

## Start here

- [Full data dictionary](data/data_dictionary.md): definitions and modeling roles for all 38 columns, units, cleaning decisions, target rules, missing values, and limitations.
- [Category inventory](data/category_inventory.csv): all observed categorical values, their counts, and meanings, including geographic codes.
- [Schema profile](data/schema_profile.csv): one row per column with semantic type and missingness.
- [Optional reference copy with documentation appendix](report/Data_Midterm_Report_documented.pdf); documentation can remain in GitHub rather than be included in the submitted report.
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

`src/data_collection.ipynb` is the rerunnable entry point for rebuilding the saved snapshot. It calls `src/collection_pipeline.py` to load raw monthly JSONs, validate and clean them, concatenate the months, and construct the target. The original interactive notebook is preserved under `src/archive/` as a historical reference. `src/eda_row.ipynb` reads the saved labeled CSV, derives calendar fields and a location-missing indicator, and creates exploratory plots. The current EDA notebook creates weekend status (`is_weekend`). Historical-volume features mentioned in the report remain planned; they are not implemented in the committed EDA notebook.

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

Open `eda_row.ipynb` from `src/` so its `../data/` and `../figures/` paths resolve. The saved CSV can also be inspected directly:

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

The repository includes a pinned **starter environment**, listed below. The archived original collection notebook records Python **3.14.6** in its metadata, which differs from that starter. Exact package versions from the original execution were not captured. These are **not verified versions of the original collection run**. The updated saved-snapshot pipeline has been checked against all twelve committed raw JSON inputs with pandas 2.2.3; that verifies reconstruction, not the original environment or a fresh live API collection.

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

### Safely rebuild the saved dataset

Open `src/data_collection.ipynb` and run the cells from top to bottom. Launch Jupyter from the repository root or `src/`.

- The default run reads the twelve committed raw JSON files. It makes no network requests.
- Every import and path is initialized before use; each month is selected explicitly, including February's existing unpadded filename.
- Duplicate IDs, unexpected schema fields, and incorrect date/agency/problem filters stop processing rather than silently changing the sample.
- Outputs go to **`data/rebuilt/`**: twelve cleaned monthly CSVs, a twelve-month checks table, and combined/labeled CSVs. The original CSVs and the EDA notebook's input remain untouched. Output filenames use month names consistently.
- Rebuilt rows are sorted by creation time and request ID. The original snapshot has 70,324 combined rows and 70,322 labeled rows, with the same 44,355 positive and 25,967 negative labels. Timestamp formatting, numeric-code formatting, and last-digit floating-point representation may differ from the original CSV, without changing the underlying values.
- `collect_month(start_date, end_date)` is still available in the helper module for an intentional live API download. It is not called by the default notebook. Preserve live downloads separately: the source is mutable, so a later download need not reproduce the saved snapshot.

Validation included rebuilding all twelve saved months, comparing all 38 columns by request ID with the original labeled CSV (normalizing timestamp/numeric formatting), and checking five offline safety/boundary tests. Notebook code cells were also checked sequentially in fresh Python processes; this environment does not permit starting a Jupyter kernel, so the Jupyter frontend itself was not tested.

The original development notebook is retained as `src/archive/data_collection_original.ipynb` for reference. It is not the supported Run All entry point. The updated workflow does not implement or alter the EDA.

Run the offline boundary and safety checks from `src/`:

```bash
python -m unittest test_collection_pipeline -v
```

## Modeling boundary

Use only predictors that would be available when a new request is submitted. Exclude closure timestamps, closure duration, status, resolution text, and resolution-update time from predictors because they contain outcome information. Use the request ID for audit only. Candidate predictors and optional calendar features are specified in the dictionary; no final matrix, trained model, or predictive performance is claimed yet.

## License and attribution

Code is covered by the repository's [LICENSE](LICENSE). NYC Open Data is the source of the underlying records; the repository's code license does not change the city's data-use terms. Cite the dataset and retain its attribution when sharing results.

## AI assistance

OpenAI ChatGPT / Codex assisted with the column documentation and `process_month`, authored the later rerunnable implementation and tests, and generated/revised repository documentation. Baidy primarily developed the original `collect_month` from his existing collection code, with ChatGPT guidance. See [AI_USAGE.md](AI_USAGE.md) for file-level authorship and the conversation-source requirement. **The actual shared chat URL still needs to be added.**
