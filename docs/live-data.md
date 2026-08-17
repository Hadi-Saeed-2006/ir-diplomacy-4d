# Live data layer

DIPLOMATIQ 4D uses the bundled dataset as its stable demo source. A lightweight optional ingestion script can fetch recent diplomacy-related article signals from the public GDELT DOC 2.0 API.

## Run

```bash
python scripts/fetch_gdelt_news.py
```

The script writes `data/gdelt_news.csv` and does not modify the core event dataset.

## Why this design?

The GDELT DOC 2.0 API supports article search and JSON/CSV output. citeturn1search0 The raw GDELT Event Database is also publicly distributed as daily files, but those files are much larger and have a more complex schema. citeturn1search10turn1search12

Keeping the live news layer optional means the dashboard remains demoable even when the network or external service is unavailable.

## Provenance

Each exported record stores the source label `GDELT DOC 2.0`. For a production deployment, add retrieval timestamps, query parameters, raw-response snapshots and source licensing/usage notes.
