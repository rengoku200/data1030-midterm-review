# AI assistance and authorship

This project used OpenAI ChatGPT / Codex for the contributions listed below. The distinction between the original collection work and the later rerunnable implementation is intentional.

## Contributions

| Portion | Authorship and assistance |
|---|---|
| Original collection workflow and `collect_month` | Baidy Mbaye developed the original workflow and primarily implemented `collect_month` by adapting the API requests and monthly filtering he had already written. ChatGPT provided guidance. This is not attributed as entirely AI-authored. |
| Original `process_month` automation | ChatGPT assisted with implementing `process_month`, including calling the collector, parsing dates, calculating closure hours, checking duplicate IDs and missing closure dates, excluding negative durations, and saving the cleaned monthly data and summary checks. This automation was used for April–December after the January–March development and checks. |
| Column documentation | ChatGPT generated the column descriptions and supporting documentation in `data/data_dictionary.md`, `data/category_inventory.csv`, and `data/schema_profile.csv`. Definitions were informed by NYC Open Data field metadata; counts were computed from the saved dataset. The AI tool is credited for the wording and compilation, and NYC Open Data remains the underlying data/metadata source. |
| Rerunnable implementation | ChatGPT / Codex authored the revised `src/data_collection.ipynb`, `src/collection_pipeline.py`, and `src/test_collection_pipeline.py`. This includes adapting the earlier collection logic, explicit monthly input loading, validation, separate rebuilt outputs, and automated checks. The original development notebook is retained under `src/archive/`. |
| Repository documentation | ChatGPT / Codex generated and revised the README and setup/reproduction guidance. It also generated the optional documentation appendix reference files in `report/`; these are separate reference materials and are not required in the submitted report. |

The revised implementation was checked by the AI tool against the saved raw JSONs and labeled CSV, using sequential execution in fresh Python processes and five offline tests. This statement does not claim the team independently performed those checks or that the original execution environment was verified.

## Conversation source

**REQUIRED LINK — NOT YET ADDED:** Baidy must insert the actual shared URL for this ChatGPT conversation here. The assistant does not have access to that URL and has not invented a link. The syllabus's chat-history-link requirement remains incomplete until the real link is added.

## Data and metadata source

[NYC Open Data: 311 Service Requests from 2020 to Present](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data), dataset `erm2-nwe9`. [Official field metadata](https://data.cityofnewyork.us/api/views/erm2-nwe9.json).

This note documents the collection code and repository documentation listed above. Attribution for any assistance retained in the report or EDA must be documented separately by the relevant contributors.
