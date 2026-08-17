"""Fetch a small, reproducible set of recent diplomacy-related articles from GDELT DOC 2.0.

This is intentionally optional: the dashboard keeps working from the bundled dataset
if the network is unavailable. GDELT DOC 2.0 exposes JSON/CSV article-search output.
"""
from pathlib import Path
from urllib.parse import urlencode
import sys

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "gdelt_news.csv"
API = "https://api.gdeltproject.org/api/v2/doc/doc"

QUERY = '(diplomacy OR "foreign relations" OR "strategic dialogue" OR "bilateral relations" OR "international summit")'


def fetch(limit: int = 50) -> pd.DataFrame:
    params = {
        "query": QUERY,
        "mode": "artlist",
        "maxrecords": min(max(limit, 1), 250),
        "timespan": "7d",
        "sort": "datedesc",
        "format": "json",
    }
    response = requests.get(API, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    articles = payload.get("articles", [])
    if not articles:
        return pd.DataFrame(columns=["date", "title", "url", "domain", "language", "source"])

    rows = []
    for article in articles:
        rows.append({
            "date": article.get("seendate"),
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "domain": article.get("domain", ""),
            "language": article.get("language", ""),
            "source": "GDELT DOC 2.0",
        })
    return pd.DataFrame(rows)


def main() -> int:
    try:
        df = fetch()
        OUT.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT, index=False)
        print(f"Saved {len(df)} GDELT article signals to {OUT}")
        return 0
    except (requests.RequestException, ValueError) as exc:
        print(f"GDELT fetch failed: {exc}", file=sys.stderr)
        print("The core dashboard remains usable with its bundled dataset.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
