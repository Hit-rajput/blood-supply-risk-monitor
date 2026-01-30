# Supply Risk Monitor: Predictive Blood Demand & Supply Forecasting  
### *Trauma-driven demand forecasting and supply risk early warning for Canada*

![Status](https://img.shields.io/badge/Current_Phase-Data gathering-blue?style=for-the-badge&logo=python)

Blood products are highly perishable (RBC ≈ 42 days; platelets ≈ 5–7 days), which makes stockpiling difficult[web:2][web:4]. Meanwhile, trauma demand can spike seasonally (long weekends, travel peaks, severe weather), and donor turnout is sensitive to external conditions. This project builds a forward-looking "Control Tower" that forecasts trauma-driven demand and highlights periods when donor supply capacity is likely to fall short.

---

## ⚠️ Problem Statement

Operational teams often detect risk after shortages emerge. The Supply Risk Monitor aims to provide earlier signals by combining:

- Trauma proxies from collisions (NCDB)
- External demand/supply drivers (weather, holidays, event signals)
- Forecasting models built for both seasonality and exogenous effects

---

## 🎯 Objectives

- Build a robust trauma-driven **Demand Index** using NCDB (injury/fatal collisions)
- Integrate exogenous drivers (weather severity, holidays, travel periods)
- Forecast short-horizon risk to support proactive collection planning
- Operationalize a single decision metric: the **Risk Coverage Ratio**

---

## 📉 Core Metric: Risk Coverage Ratio

The dashboard centers on:

```
Risk Coverage Ratio = Supply Proxy ÷ Demand Index
```

- **Supply Proxy**: leading indicators of donor capacity (planned integration)
- **Demand Index**: trauma-driven proxy from collisions (current focus)

Threshold bands will classify future periods as **Stable**, **Warning**, or **Critical** during dashboard calibration.

---

## 🛠️ Technical Solution (ELT + Forecasting)

The system follows an **ELT** approach:

1. **Extract**: automated fetching of public datasets (NCDB now; weather next)
2. **Load**: Bronze layer (raw files preserved)
3. **Transform**: Silver layer (cleaned, merged, analytics-ready outputs); Gold layer planned (star schema for BI)
4. **Forecasting engine** (planned hybrid):
   - **Prophet** for baseline seasonality and holiday effects
   - **XGBoost** for exogenous features (weather severity, trauma proxies, event indicators)
5. **Operationalization**: Power BI "Control Tower" monitoring Risk Coverage Ratio and risk periods

---

## 📂 Repository Structure

```
data/
  bronze/
    ncdb/                 # Raw NCDB CSVs (1999–2021)
  silver/
    ncdb/                 # Cleaned/merged outputs (e.g., ncdb_merged_filtered.csv)

src/
  ingest/                 # Ingestion notebooks/scripts (Open Canada CKAN)

notebooks/                # EDA + processing (Polars; large-scale handling)
```

---

## 📊 Current Progress: NCDB Trauma Proxy Pipeline

**Phase 1** focuses on NCDB to build the trauma proxy:

- **Scale**: > 7.7 million collision events processed
- **Performance**: Polars LazyFrames used to merge and filter 20+ years efficiently
- **Filtering**: injury + fatal collisions prioritized for higher-fidelity demand signal
- **EDA**: seasonality, severity mapping, and demographic distributions

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Jupyter Notebook/Lab
- [Polars](https://pola.rs/)

### Installation

```bash
git clone https://github.com/hit-rajput/blood-supply-risk-monitor.git
cd blood-supply-risk-monitor
pip install polars pandas matplotlib seaborn
```

### Run (current workflow)

1. Run ingestion in `src/ingest/` to download raw data into `data/bronze/`
2. Run notebooks in `notebooks/` to generate cleaned outputs into `data/silver/`

---

## 🗺️ Roadmap

- [x] Ingest National Collision Database (NCDB)
- [x] Initial EDA and cleaning
- [ ] Integrate weather data (Environment and Climate Change Canada)
- [ ] Build Prophet + XGBoost forecasting model
- [ ] Create Power BI "Control Tower" dashboard (Risk Coverage Ratio + thresholds + scenarios)

---

## 📚 Data Sources (Current + Planned)

- **[National Collision Database (NCDB)](https://open.canada.ca/)** (Open Canada)
- **Weather** (planned): Environment and Climate Change Canada
- **Holidays/calendar effects** (planned): federal/provincial holiday calendar features

---

## 🔐 Data & Governance Notes

- This repo uses public datasets for ingestion (NCDB and planned external drivers)
- Any donor/donation data integration must follow privacy and governance requirements (aggregation, de-identification, access controls)

---

## 👤 Author

**Hit Rajput**  
*Focus: Data Science, Machine Learning, and Business Intelligence in Healthcare*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
