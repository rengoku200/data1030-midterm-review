# AI assistance and authorship


## Contributions

Authorship and assistance |
|---|---|
| Original collection workflow and collect month |I was the primary author of collect month and the original checks with ChatGpt providing guidance but not code. Utilizing the previous manual processes for January-February I created collect months.
| Original process_month automation | ChatGPT assisted with implementing process_month, which included using my collector, parsing dates, calculating closure hours, checking duplicate IDs and missing closure dates, excluding negative durations, and saving the cleaned monthly data and summary checks. This automation was used for April–December after the January–March development and checks. |
| Column documentation | ChatGPT generated the column descriptions and supporting documentation in `data/data_dictionary.md`, `data/category_inventory.csv`, and `data/schema_profile.csv`. Definitions were informed by NYC Open Data field metadata; counts were computed from the saved dataset. The AI tool is credited for the wording and compilation, and NYC Open Data remains the underlying data/metadata source. |
| Rerunnable implementation | ChatGPT authored the revised `src/data_collection.ipynb`, `src/collection_pipeline.py`, and `src/test_collection_pipeline.py`. This includes adapting the earlier collection logic, explicit monthly input loading, validation, separate rebuilt outputs, and automated checks. The original development notebook is in the original notebook folder
| Repository documentation | ChatGPT / Codex generated and revised the README and setup/reproduction guidance. It also generated the optional documentation appendix reference files in `report/`; these are separate reference materials and are not required in the submitted report. |

The revised implementation was checked by the AI tool against the saved raw JSONs and labeled CSV, using sequential execution in fresh Python processes and five offline tests. We verified that it ran afterwards and passed tests

## Conversation source



