# 🌐 DIPLOMATIQ 4D

### Global Relations & Diplomacy Intelligence Platform

**DIPLOMATIQ 4D** is a lightweight geopolitical analytics platform built to explore how international-relations signals evolve across **geography, time, actors, counterparties, severity and impact**.

> **4D = 3D geographic space + time.**

[![CI](https://github.com/Hadi-Saeed-2006/ir-diplomacy-4d/actions/workflows/quality.yml/badge.svg)](https://github.com/Hadi-Saeed-2006/ir-diplomacy-4d/actions/workflows/quality.yml)

---

## 🎯 What problem does it solve?

International-relations data is multidimensional. A conventional chart can show *what happened*, but analysts also need to understand **where signals concentrate, who is interacting, how activity changes over time, and which signals deserve further investigation**.

DIPLOMATIQ 4D turns those dimensions into an interactive analyst workflow:

**Detect → Connect → Quantify → Profile → Validate**

This is a **decision-support portfolio prototype**, not an intelligence product or official geopolitical-risk rating.

---

## 🛰️ Core capabilities

| Module | Purpose | Demonstrates |
|---|---|---|
| 🌍 **4D Globe** | Explore events geographically and temporally | Geospatial analytics + visualization |
| 🤝 **Diplomatic Network** | Explore actor/counterparty relationships | Network analysis |
| 📈 **Risk & Trends** | Compare event volume, impact and pressure | Analytical modeling |
| 🌍 **Country Profile** | Drill into one country's signals and partners | Interactive analytics |
| 🧠 **Analyst Brief** | Convert filtered data into an executive summary | Product thinking |
| 📰 **Live News Layer** | Optional external news signals | API/data ingestion |
| ⬇️ **CSV Export** | Export the current analytical slice | Practical workflow |

---

## 🧠 Analytical model

The project represents the event system as:

`Actor × Counterparty × Location × Time × Event Type × Severity × Impact`

The current **relative pressure score** is deliberately transparent rather than a black-box ML model. It combines:

- severity — **45%**
- aggregate impact — **35%**
- event frequency — **20%**

The score is normalized within the selected sample. It is **not** a country credit rating, intelligence assessment, or official foreign-policy indicator.

---

## 🏗️ Architecture

```text
                    DIPLOMATIQ 4D
                         │
          ┌──────────────┴──────────────┐
          │                             │
   Bundled event data             Optional live news
          │                             │
          └──────────────┬──────────────┘
                         ↓
                 Validation layer
                         ↓
                 Pandas data model
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
        Analytical layer       Profile layer
              │                     │
       ┌──────┼──────┐              │
       ↓      ↓      ↓              ↓
     Globe  Network Trends      Country Profile
       │      │      │              │
       └──────┴──────┴──────┬───────┘
                             ↓
                    Streamlit interface
```

### Why the architecture is intentionally simple

The project prioritizes **fast startup, low failure surface and explainability**. The core dashboard does not require a database, cloud service, API key, Docker stack or ML model.

External/live data is an enhancement rather than a single point of failure.

---

## 🛠️ Technology stack

- **Python** — application and analytical logic
- **Pandas** — data transformation
- **NumPy** — numerical calculations
- **Plotly** — interactive visual analytics
- **Streamlit** — dashboard application
- **GitHub Actions** — automated quality checks

---

## 📁 Repository structure

```text
ir-diplomacy-4d/
├── app.py
├── data/
│   └── diplomatic_events.csv
├── scripts/
│   └── data ingestion utilities
├── docs/
│   └── methodology and live-data notes
├── .github/workflows/
│   └── quality.yml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## ▶️ Run locally

```bash
git clone https://github.com/Hadi-Saeed-2006/ir-diplomacy-4d.git
cd ir-diplomacy-4d
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

---

## 🔬 Data integrity & provenance

The bundled dataset is **synthetic demonstration data** designed to keep the project immediately runnable and reproducible.

The optional live-news layer is treated separately from the event dataset because **news coverage is a signal, not automatically a verified diplomatic event**.

For future production ingestion, each record should retain:

- source
- source URL
- retrieval timestamp
- publisher/domain
- transformation history
- data type
- confidence/provenance metadata

See [`docs/live-data.md`](docs/live-data.md) for the live-data design.

---

## 🧪 Reliability

GitHub Actions automatically checks the repository's Python compilation and CSV structure.

The project intentionally uses a small dependency surface so it is easier to reproduce on another machine and easier to debug during a live portfolio demonstration.

---

## 🔐 Security principles

- Never commit API keys or credentials.
- Keep secrets in environment variables or GitHub Secrets.
- Do not present synthetic analytics as real-world intelligence.
- Treat external news signals as unverified until validated against authoritative sources.

GitHub recommends enabling repository security features such as Dependabot alerts, secret scanning and push protection for public repositories.

---

## 🚀 Roadmap

### Completed

- [x] 4D global visualization foundation
- [x] Diplomatic network analysis
- [x] Explainable pressure indicator
- [x] Country intelligence profile
- [x] Analyst brief
- [x] Filtered CSV export
- [x] Data validation
- [x] GitHub Actions quality checks
- [x] Optional live-news architecture

### Next versions

- [ ] Source/provenance panel inside the dashboard
- [ ] Additional authoritative public datasets
- [ ] NLP-based event extraction
- [ ] Entity recognition for countries and institutions
- [ ] Anomaly detection
- [ ] Optional forecasting experiment

Advanced AI features will only be added if they improve the analytical outcome without making the application fragile.

---

## 💼 Portfolio / CV positioning

**DIPLOMATIQ 4D — Global Relations & Diplomacy Intelligence Platform**

> Built a geopolitical analytics platform using Python, Pandas, NumPy, Plotly and Streamlit to model international-relations events across geography and time; implemented diplomatic network analysis, an explainable pressure indicator, country-level intelligence profiles, optional live-news ingestion, data validation and automated GitHub Actions quality checks.

### Skills demonstrated

**Python • Data Analysis • Data Visualization • Geospatial Analytics • Network Analysis • Statistical Scoring • Streamlit • API/Data Ingestion • Git/GitHub • CI/CD • International Relations Analytics**

---

## ⚠️ Responsible-use note

DIPLOMATIQ 4D is an educational and portfolio decision-support prototype. It does not provide military, intelligence, legal or foreign-policy advice. Analytical scores are project-defined indicators and should not be interpreted as official country assessments.

---

## 👤 Author

**Hadi Shaikh**  
Data Science student | Geopolitical Analytics | International Relations & Diplomacy

[GitHub](https://github.com/Hadi-Saeed-2006) · [DIPLOMATIQ 4D](https://github.com/Hadi-Saeed-2006/ir-diplomacy-4d)
