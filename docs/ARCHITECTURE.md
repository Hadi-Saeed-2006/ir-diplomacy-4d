# DIPLOMATIQ 4D Architecture

## Design goal

The system is deliberately small: a reproducible event dataset, a validation layer, an analytical layer, and a Streamlit presentation layer.

## Data flow

```text
CSV / optional external signal
          ↓
     data validation
          ↓
      pandas DataFrame
          ↓
 ┌────────┼─────────┐
 ↓        ↓         ↓
Geo     Network   Trends
 ↓        ↓         ↓
 └────────┼─────────┘
          ↓
 Country intelligence profile
          ↓
     Streamlit dashboard
```

## Reliability boundaries

1. The bundled dataset is the fallback path.
2. External/live news is optional.
3. No database is required for the portfolio version.
4. The pressure score is deterministic and explainable.
5. CI validates basic code and data integrity before changes are considered stable.

## Extension points

Future modules can be added behind the same data contract:

- authoritative country indicators
- diplomatic documents
- NLP event extraction
- anomaly detection
- forecasting experiments

The goal is to add analytical capability without turning the application into a fragile distributed system.
