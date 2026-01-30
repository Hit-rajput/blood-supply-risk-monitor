# Supply Risk Monitor: Predictive Blood Demand & Supply Forecasting  
### *Trauma-driven demand forecasting and supply risk early warning for Canada*

![Status](https://img.shields.io/badge/Current_Phase-Data_Gathering_&_Algorithm_Selection-orange?style=for-the-badge&logo=python)

Blood products are highly perishable (RBC ≈ 42 days; platelets ≈ 5–7 days), which makes stockpiling difficult. Meanwhile, trauma demand can spike seasonally (long weekends, travel peaks, severe weather), and donor turnout is sensitive to external conditions. This project builds a forward-looking "Control Tower" that forecasts trauma-driven demand and highlights periods when donor supply capacity is likely to fall short.

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
- Evaluate forecasting algorithms (Prophet, XGBoost, SARIMA, LSTM) for optimal performance
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
4. **Algorithm evaluation** (current phase):
   - **Prophet**: baseline seasonality and holiday effects
   - **XGBoost**: exogenous features (weather severity, trauma proxies, event indicators)
   - **SARIMA**: classical time series with seasonal components
   - **LSTM/GRU**: deep learning approaches for sequential patterns
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

**Phase 1** focuses on data gathering and algorithm evaluation:

- **Scale**: > 7.7 million collision events processed
- **Performance**: Polars LazyFrames used to merge and filter 20+ years efficiently
- **Filtering**: injury + fatal collisions prioritized for higher-fidelity demand signal
- **EDA**: seasonality patterns, severity mapping, and demographic distributions
- **Algorithm research**: evaluating Prophet, XGBoost, SARIMA, and LSTM for trauma demand forecasting

<details>
<summary><b>📋 View Detailed NCDB Exploratory Analysis Findings</b></summary>

<br>

### Executive Summary

The data reveals a critical misalignment between typical blood donation patterns and trauma demand:

- **The Problem**: Trauma demand peaks in Summer and Late Autumn—precisely when donor attendance typically drops ("Summer Slump")
- **The Risk Zone**: The highest volume of potential trauma patients occurs on Friday afternoons (3 PM – 6 PM), creating a weekly pressure point for hospital inventory entering the weekend
- **The Patient Profile**: The primary demographic driver is Males aged 18–30. This group is statistically more likely to be involved in severe crashes and, due to average body size, may require higher volumes of blood products per transfusion than other demographics

---

### Temporal Dynamics: When is the System Stressed?

#### Long-Term Trend: The "COVID Shock"

**Observation**: There is a steady, structural decline in collision injuries from 1999–2019, likely due to improved vehicle safety standards.

**Critical Anomaly**: The massive drop in 2020 represents the COVID-19 lockdowns and reduced traffic volume.

**Forecasting Implication**: Predictive models cannot treat 2020–2021 as "normal." This period must either be treated as an anomaly in time series forecasting or adjusted using control features like "vehicle kilometers traveled."

#### Seasonality: The "Summer Peak"

**Observation**: Injuries rise starting in May, peak in July–August, and remain elevated through October.

**Blood Supply Context**: Canadian Blood Services often faces low donor turnout in summer due to vacations. The simultaneous peak in trauma demand creates a perfect storm for supply risk.

**Recommended Action**: Implement targeted donor campaigns in April–May to build inventory buffer before the summer surge.

#### Weekly Risk Pattern: Friday Afternoon Pressure

**Observation**: Fridays are the most dangerous day of the week, specifically between 15:00 and 18:00.

**Supply Chain Impact**: Hospitals need to be fully stocked by Friday morning. If a mass casualty event occurs on Friday afternoon, the supply chain has minimal buffer time before the weekend when staffing and logistics are reduced.

---

### Demographic Drivers: Estimating Volume Requirements

#### The "Young Male" Factor

**Observation**: A massive spike in victims aged 20–30, with Males significantly outnumbering Females.

**Modeling Insight**: "Trauma Volume" is not just *Count of People*—it is *Count × Body Surface Area*. A 25-year-old male typically has a larger blood volume (approximately 5-6 liters) than a child or elderly patient.

**Forecasting Enhancement**: Weight collisions involving this demographic as "High Demand Potential" in predictive models.

---

### Strategic Recommendations

#### For Blood Inventory Management

1. **Pre-Summer Stockpiling**: Launch intensive donor recruitment campaigns in April–May
2. **Friday Load Balancing**: Increase Thursday night/Friday morning deliveries to trauma centers by 15-20%
3. **Demographic-Weighted Forecasting**: Implement collision forecasts that account for victim demographics, not just incident counts

#### For Predictive Modeling

1. **COVID Period Handling**: Use external regressors or dummy variables for 2020–2021
2. **Seasonal Decomposition**: Apply multiplicative seasonal models given the consistent summer peak pattern
3. **Age-Gender Weighting**: Incorporate demographic multipliers based on average blood volume requirements

---

**📄 Full Analysis**: See [NCDB_FINDINGS.md](docs/NCDB_findings.md) for complete findings with visualizations

</details>

---
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
- [ ] Evaluate and select optimal forecasting algorithm (Prophet vs XGBoost vs SARIMA vs LSTM)
- [ ] Build production forecasting pipeline
- [ ] Create Power BI "Control Tower" dashboard (Risk Coverage Ratio + thresholds + scenarios)

---

## 📚 Data Sources (Current + Planned)

- **[National Collision Database (NCDB)](https://open.canada.ca/)** (Open Canada)
- **Weather** (planned): Environment and Climate Change Canada
- **Holidays/calendar effects** (planned): federal/provincial holiday calendar features
- **Donor/donation signals** (planned): internal Canadian Blood Services data (subject to governance)

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
