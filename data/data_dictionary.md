This reference documents the committed `street_conditions_2025_labeled.csv` snapshot: **70,322 requests and 38 columns**. Each row is one NYC Department of Transportation (DOT) Street Condition request created during 2025. It is a request-level binary classification dataset, not an aggregated time series. Rows need not be in chronological order; identifiers must not be used as predictors.

Validated on 2026-10-22 against repository commit `d4a15bc501564ad6b53e7780ea5cc6976411bb29`. Counts describe that saved snapshot, not a new API download. CSV files do not preserve pandas dtypes; types below describe how the fields should be interpreted. No predictor is an ordered severity category. Dates have no timezone offset in the saved file; the notebook subtracts timezone-naive timestamps. Confirm timezone and daylight-saving behavior before making precise elapsed-time claims.

## Source and collection

- Publisher: NYC Open Data / NYC 311, dataset ID `erm2-nwe9`, *311 Service Requests from 2020 to Present*.
- [Dataset and field descriptions](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data).
- [JSON API endpoint](https://data.cityofnewyork.us/resource/erm2-nwe9.json).
- Filters: `agency = 'DOT'`, `complaint_type = 'Street Condition'`, and a half-open creation-date window for each month: start inclusive, next month exclusive. Together the windows cover `2025-01-01T00:00:00 <= created_date < 2026-01-01T00:00:00`.
- Collection uses Python `requests` and Socrata query parameters. The `collect_month(start_date, end_date)` helper returns a list of JSON records; it requests pages of 5,000 with `$offset`, ordered by `created_date ASC, unique_key ASC`. The original January collection used a single limit of 6,000, enough for its 5,474 rows.
- `process_month(year, month)` calls the collector, saves raw records, checks duplicate IDs, parses dates, calculates hours, removes negative durations, and saves monthly CSVs and summary counts. January through March were checked during development; the loop processes April through December.
- The source is updated over time. The notebook does not log an exact retrieval timestamp for every request or preserve an environment lock from the original run. Retain the saved raw JSON and CSVs to reproduce this snapshot rather than assume a later API call will return identical records.

## Cleaning and target definition

The saved collection contains 70,330 records before excluding six negative durations (February: 1; March: 2; July: 1; December: 2). Concatenating the cleaned monthly CSVs produced 70,324 rows with no duplicated `unique_key`. Two records with missing closure dates and `Unspecified` status could not be labeled and were excluded, leaving 70,322 rows.

`closure_hours = (closed_date - created_date).total_seconds() / 3600`.

| Condition | `closed_48h` | Rows |
|---|---:|---:|
| Recorded duration from 0 through 48 hours, inclusive | 1 | 44,355 |
| Recorded duration greater than 48 hours | 0 | 22,492 |
| Missing closure date and status Pending or Open | 0 | 3,475 |
| Missing closure date and Unspecified status | Excluded | 2 |

Thus the final target contains 44,355 ones (63.1%) and 25,967 zeros (36.9%), with no missing labels. The 48-hour cutoff is a team-selected operational threshold, not a verified NYC service standard or a measure of task difficulty. Administrative closure does not necessarily mean physical repair.

**Follow-up assumption:** labeling a request with no recorded closure as 0 requires observing it for at least 48 hours after creation and treating the missing closure record as evidence of no administrative closure by then. The 2025 requests were collected during the team's 2026 work, giving ample elapsed calendar time, but record completeness is still an assumption. This is not the same as deleting all Pending/Open requests. Six rows have Pending status and a recorded closure date; the notebook uses recorded duration for those rows. The final file has 66,847 recorded durations and 3,475 missing durations. It also retains 3,276 zero-hour durations; these require interpretation as administrative records, not instantaneous repair.

## All 38 saved columns

Roles describe an initial modeling proposal, not a fitted or finalized feature matrix. **Candidate** means assess at submission time before including in X; mutable geovalidated fields may have been updated later. **Derive** means use calendar features. **Leakage** means outcome-related information excluded from X. **Audit**, **Constant**, **Empty**, **Sparse**, and **Redundant** mean retain in the saved data if useful, but exclude initially from X. **Target** is y, never a predictor. Continuous units are given in the descriptions; state-plane units remain unverified rather than guessed.

| Column | Interpretation | Missing | Initial role | Description |
|---|---|---:|---|---|
| `unique_key` | Identifier | 0 | Audit | Unique service-request identifier. Keep as text for duplicate checks and traceability; exclude from predictors. |
| `created_date` | Timestamp | 0 | Derive | Request creation date and time. Parse as a datetime; derive calendar features rather than use the raw timestamp. |
| `closed_date` | Timestamp | 3,475 | Leakage | Date and time the responding agency recorded closure. Used to calculate the outcome; exclude from predictors. |
| `agency` | Nominal | 0 | Constant | Responding agency acronym. DOT means Department of Transportation; constant after filtering. |
| `agency_name` | Nominal | 0 | Constant | Full responding agency name; Department of Transportation in every row. |
| `complaint_type` | Nominal | 0 | Constant | Broad problem category. Street Condition in every row; descriptor provides the varying problem detail. |
| `descriptor` | Nominal | 0 | Candidate | Specific street-condition problem, with 21 observed categories defined below. These labels are not an ordered severity scale. |
| `incident_zip` | Nominal code | 749 | Candidate | Geovalidated incident ZIP code. Preserve as text; numerical magnitude has no predictive interpretation. Codes are listed in the category inventory. |
| `intersection_street_1` | Text | 24,352 | Audit | First intersecting street from the geovalidated incident location. High-cardinality location text. |
| `intersection_street_2` | Text | 24,331 | Audit | Second intersecting street from the geovalidated incident location. High-cardinality location text. |
| `address_type` | Nominal | 0 | Candidate | Type of incident-location information, such as an address, intersection, or street segment. Six observed labels are defined below. |
| `city` | Nominal | 10,900 | Audit | City or locality name returned by geovalidation. Values are not necessarily borough names; partly redundant with other geography. |
| `facility_type` | Nominal | 70,322 | Empty | City facility type associated with a request, if available. Entirely blank in this snapshot. |
| `status` | Nominal | 0 | Leakage | Request status at collection, not necessarily status at submission. Closed, Pending, and Open are defined below. Used for labeling only. |
| `resolution_description` | Text | 15 | Leakage | Last action described by the responding agency, sometimes including next steps. Exclude because it can reveal post-submission handling. |
| `resolution_action_updated_date` | Timestamp | 12 | Leakage | Date and time the responding agency last updated the request. Post-submission information; exclude from predictors. |
| `community_board` | Nominal code | 0 | Candidate | Geovalidated community-board label, typically a board number plus borough. Exceptional labels are retained as source values and need validation. |
| `council_district` | Nominal code | 19,796 | Candidate | City Council district containing the request. Values 1 through 51 identify districts, not a ranking; saved CSV uses decimal-looking codes. |
| `police_precinct` | Nominal code | 0 | Candidate | NYPD precinct containing the request. Precinct numbers identify jurisdictions, not a ranking; Unspecified means not identified. |
| `borough` | Nominal | 0 | Candidate | Incident borough, submitted and confirmed by geovalidation. Five NYC boroughs plus Unspecified. |
| `x_coordinate_state_plane` | Continuous | 19,598 | Audit | Geovalidated horizontal coordinate in the source state-plane system. The source field description does not specify units or CRS; verify before interpreting distances. Redundant with latitude/longitude. |
| `y_coordinate_state_plane` | Continuous | 19,591 | Audit | Geovalidated vertical coordinate in the source state-plane system. The source field description does not specify units or CRS; verify before interpreting distances. Redundant with latitude/longitude. |
| `open_data_channel_type` | Nominal | 0 | Candidate | How the request was submitted: PHONE, ONLINE, OTHER, or UNKNOWN in this snapshot. |
| `park_facility_name` | Text | 0 | Constant | Name of a Parks Department facility, if applicable. Every saved value is the placeholder Unspecified. |
| `park_borough` | Nominal | 0 | Redundant | Source park-related borough field. In this snapshot its values match borough row for row, so retain only borough for initial modeling. |
| `latitude` | Continuous | 19,601 | Candidate | Incident latitude in decimal degrees. Missing values must be handled within the training pipeline. |
| `longitude` | Continuous | 19,601 | Candidate | Incident longitude in decimal degrees. Missing values must be handled within the training pipeline. |
| `location` | Structured text | 19,601 | Redundant | Serialized geographic point containing longitude then latitude. Duplicates the separate coordinate fields; do not treat as a third independent location measurement. |
| `incident_address` | Text | 14,092 | Audit | Incident-address text supplied for the location. High-cardinality location field; retain for audit rather than the initial predictor matrix. |
| `street_name` | Text | 14,092 | Audit | Street name of the incident address supplied by the submitter. High-cardinality location text. |
| `cross_street_1` | Text | 14,511 | Audit | First cross street associated with the geovalidated incident location. High-cardinality location text. |
| `cross_street_2` | Text | 14,494 | Audit | Second cross street associated with the geovalidated incident location. High-cardinality location text. |
| `descriptor_2` | Nominal | 70,302 | Sparse | Third level of problem detail. Only Other appears, in 20 rows; the remaining 70,302 rows are blank. Exclude initially because it is nearly empty. |
| `location_type` | Nominal | 38,771 | Candidate | Type of location associated with the request, with six observed labels defined below. Frequently missing; optional candidate requiring missing-value handling. |
| `landmark` | Text | 48,935 | Audit | Landmark name associated with the incident location when available. High-cardinality location text. |
| `bbl` | Identifier | 43,894 | Audit | Borough-Block-Lot parcel identifier from geovalidation. Preserve as an identifier, not a continuous measurement; decimal suffixes are serialization artifacts. |
| `closure_hours` | Continuous | 3,475 | Leakage | Derived recorded duration in hours: (closed_date - created_date).total_seconds() / 3600. Missing when closure is unavailable; excludes negative durations. Never include in predictors. |
| `closed_48h` | Binary target | 0 | Target | 1 means recorded administrative closure within 48 hours inclusive. 0 means closure after 48 hours, or missing closure with Pending/Open status at collection. See target rules and follow-up assumption below. |

## Observed categories and their meanings

Definitions below are plain-language interpretations of source labels, not official engineering severity definitions. The [category inventory](category_inventory.csv) gives **every observed value, count, and meaning for each categorical column**, including all geographic codes, locality names, placeholder values, and blanks. Category counts are snapshot-specific. High-cardinality address strings, free-form resolution text, IDs, and numeric measurements are not enumerated as categories.

### `descriptor`

| Value | Rows | Meaning |
|---|---:|---|
| Blocked - Construction | 4,245 | Reported street obstruction associated with construction. |
| Cave-in | 9,647 | Reported collapse or sinking of the street surface. |
| Crash Cushion Defect | 225 | Reported defect in a crash cushion, an impact-absorbing road safety device. |
| Defacement | 20 | Reported defacement of a street-related surface or feature. |
| Defective Hardware | 5,490 | Reported defective street hardware; the label does not identify a specific component. |
| Depression Maintenance | 31 | Reported maintenance issue involving a depression in the street surface. |
| Dumpster - Construction Waste | 584 | Reported street condition involving a construction-waste dumpster. |
| Failed Street Repair | 3,487 | Reported problem with a previous street repair. |
| Guard Rail - Street | 106 | Reported street guard-rail condition. |
| Hummock | 18 | Reported raised bump or mound in the street surface. |
| Line/Marking - After Repaving | 507 | Reported road line or marking issue after repaving. |
| Line/Marking - Faded | 386 | Reported faded road line or marking. |
| Plate Condition - Anti-Skid | 53 | Reported issue with a street plate anti-skid surface. |
| Plate Condition - Noisy | 2,927 | Reported noise from a street plate. |
| Plate Condition - Open | 65 | Reported open street-plate condition; no engineering severity is inferred. |
| Plate Condition - Shifted | 622 | Reported street plate that has moved out of position. |
| Pothole | 38,430 | Reported hole in the street surface. |
| Rough, Pitted or Cracked Roads | 3,121 | Reported roughness, pitting, or cracking of the road surface. |
| Strip Paving | 1 | Reported condition classified by DOT as Strip Paving; the source label supplies no further detail. |
| Unsafe Worksite | 66 | Reported unsafe condition at a worksite. |
| Wear & Tear | 291 | Reported deterioration through wear and tear. |

### `address_type`

| Value | Rows | Meaning |
|---|---:|---|
| ADDRESS | 27,748 | Street address. |
| BLOCKFACE | 19,639 | Street segment or block face. |
| INTERSECTION | 22,779 | Intersection of streets. |
| PLACE | 72 | Source place-based label; exact distinction from PLACENAME is not documented in the schema. |
| PLACENAME | 26 | Source place-name label; exact distinction from PLACE is not documented in the schema. |
| UNRECOGNIZED | 58 | Location type not recognized by the source. |

### `status`

| Value | Rows | Meaning |
|---|---:|---|
| Closed | 66,841 | Agency-recorded closed status. |
| Open | 8 | Agency-recorded open status. |
| Pending | 3,473 | Agency-recorded pending status. |

### `borough`

| Value | Rows | Meaning |
|---|---:|---|
| BRONX | 6,955 | NYC borough: Bronx. |
| BROOKLYN | 18,375 | NYC borough: Brooklyn. |
| MANHATTAN | 12,386 | NYC borough: Manhattan. |
| QUEENS | 25,980 | NYC borough: Queens. |
| STATEN ISLAND | 6,494 | NYC borough: Staten Island. |
| Unspecified | 132 | Borough not identified. |

### `open_data_channel_type`

| Value | Rows | Meaning |
|---|---:|---|
| ONLINE | 15,842 | Submitted through an online channel. |
| OTHER | 1 | Other submission channel. |
| PHONE | 13,191 | Submitted by telephone. |
| UNKNOWN | 41,288 | Submission channel not known or not recorded. |

### `location_type`

| Value | Rows | Meaning |
|---|---:|---|
| Bike Lane | 39 | Bicycle lane. |
| Crosswalk | 337 | Pedestrian crossing. |
| School Safety Zone | 14 | School safety zone. |
| Speed Reducer | 48 | Traffic-calming speed reducer. |
| Street | 31,006 | Street location. |
| Vehicle Lane | 107 | Vehicle traffic lane. |

### `agency`

| Value | Rows | Meaning |
|---|---:|---|
| DOT | 70,322 | Department of Transportation. |

### `agency_name`

| Value | Rows | Meaning |
|---|---:|---|
| Department of Transportation | 70,322 | Full name of the responding agency. |

### `complaint_type`

| Value | Rows | Meaning |
|---|---:|---|
| Street Condition | 70,322 | Broad category of street-condition requests. |

### `descriptor_2`

| Value | Rows | Meaning |
|---|---:|---|
| Other | 20 | Additional problem detail recorded as Other; no more specific detail provided. |

### `closed_48h`

| Value | Rows | Meaning |
|---|---:|---|
| 0 | 25,967 | Not recorded as closed within 48 hours under the labeling rules. |
| 1 | 44,355 | Recorded as closed within 48 hours inclusive. |

### `park_facility_name`

| Value | Rows | Meaning |
|---|---:|---|
| Unspecified | 70,322 | No specific park facility identified. |

## Geographic code conventions

ZIP codes, community boards, council districts, and precincts are nominal identifiers. Their numerical values do not express a smaller-to-larger ranking. Council district values such as `1.0` are serialized codes, not measured quantities. `city` contains source locality names, which should not be silently treated as boroughs. Literal `Unspecified` and `UNKNOWN` values are distinct from blank cells. The EDA notebook converts `borough == "Unspecified"` to missing in its working copy. Coordinates are missing for 19,601 rows (27.9%); availability of coordinates may itself be informative.

## Features created outside the saved CSV

The committed `src/eda_1.ipynb` creates these fields in memory; they are **not additional columns in the saved 38-column CSV**:

| Feature | Meaning / values | Units / interpretation |
|---|---|---|
| `hour` | Creation hour, 0 through 23 | Hours on a daily cycle |
| `month` | Creation month, 1 through 12 | January through December; annual cycle |
| `day_of_week` | Monday through Sunday | Nominal calendar labels, weekly cycle |
| `location_missing` | Whether latitude is missing | Boolean: True means absent, False means present |

Weekend status and historical complaint-volume counts discussed in the report are **planned features**, not implemented in the committed EDA notebook. If added, weekend means Saturday/Sunday. Historical counts must use requests created strictly before the current request, with clearly defined time windows and grouping (for example, borough or descriptor). The first window needs earlier data or an explicit insufficient-history rule. Do not include future requests, use the constant `complaint_type` as if it varied, or claim these features already exist.

## Predictor exclusions and limitations

- Always exclude `closed_date`, `closure_hours`, `status`, `resolution_description`, and `resolution_action_updated_date` from X: they can reveal the eventual outcome. Use `closed_48h` only as y.
- Exclude `unique_key` and `bbl` initially as identifiers; retain them for traceability. Exclude constant, empty, sparse, redundant, and high-cardinality text fields as specified in the table unless a later modeling decision justifies a change.
- Evaluate candidate predictors using only information available when a new request is submitted. The latest open-data snapshot cannot by itself establish that every geovalidated value was available unchanged at that moment.
- Requests may be related in location, time, or underlying incident. Unique IDs do not establish independent observations. Choose and justify a validation split later; no model or validation result is documented here.
- Use [schema_profile.csv](schema_profile.csv) for a machine-readable description, null counts, and distinct-value counts. No missing-value imputation, encoding, or final predictor selection has yet been established by this documentation.
