Supply Risk Monitor: Predictive Blood Demand & Supply Forecasting
The Supply Risk Monitor is a predictive analytics platform designed to forecast trauma-driven blood demand and identify periods where donor supply capacity in Canada is likely to fall short.

This project aims to shift from descriptive reporting (what happened) to prescriptive risk modeling (what is likely to happen) by combining collision data, donor/donation signals, and external drivers like weather and holidays to provide a “Control Tower” for early warning and scenario planning.

Problem Statement
Blood products are highly perishable, which makes stockpiling difficult:

Red Blood Cells: 
≈
42
≈42 days

Platelets: 
≈
5
≈5–
7
7 days

At the same time:

Volatile demand: trauma events spike seasonally (travel seasons, long weekends, extreme weather)

Supply constraints: donor turnout is sensitive to external factors

The gap: teams often react to shortages after they emerge

This project introduces a forward-looking metric that supports proactive collection campaigns and inventory redistribution.

Core Metric: Risk Coverage Ratio
The dashboard centers on the Risk Coverage Ratio:

Risk Coverage Ratio
=
Supply Proxy
Demand Index
Risk Coverage Ratio= 
Demand Index
Supply Proxy
 
Supply Proxy: leading indicators of donor capacity (planned integration)

Demand Index: trauma-driven demand proxy (initially derived from NCDB collisions)

The dashboard will classify future periods into Stable, Warning, and Critical thresholds (to be finalized during dashboard design and calibration).

Technical Solution (ELT Architecture)
This system follows an ELT (Extract, Load, Transform) approach:

Ingestion (Bronze): automated fetching of public datasets (NCDB now; weather next)

Transformation (Silver/Gold): cleaning, standardization, and modeling into BI-ready structures (star schema planned)

Forecasting engine (planned hybrid approach):

Prophet: baseline seasonality + holiday effects

XGBoost: exogenous drivers (weather severity, trauma proxies, event indicators)

Operationalization: Power BI “Control Tower” dashboard to monitor Risk Coverage Ratio and support scenario planning

Repository Structure
text
data/
  bronze/
    ncdb/                 # Raw National Collision Database CSVs (1999–2021)
  silver/
    ncdb/                 # Cleaned/merged dataset outputs

src/
  ingest/                 # Notebooks/scripts for automated data retrieval (e.g., CKAN)

notebooks/                # EDA + processing (Polars; large-scale handling)
Current Progress: NCDB Pipeline (Trauma Proxy)
Phase 1 focuses on building a high-fidelity trauma proxy using the National Collision Database:

Dataset size: 
>
7.7
>7.7 million collision events processed

Optimization: Polars LazyFrames to merge and clean 20+ years efficiently

Filtering: injury and fatal collisions prioritized for demand-signal quality

EDA: seasonality patterns, severity mapping, and victim demographic distributions

Getting Started
Prerequisites
Python 3.10+

Polars: https://pola.rs/

Jupyter Notebook/Lab

Install
bash
git clone https://github.com/hit-rajput/blood-supply-risk-monitor.git
cd blood-supply-risk-monitor
pip install polars pandas matplotlib seaborn
Run (current workflow)
Run ingestion notebooks/scripts in src/ingest/ to download raw files into data/bronze/

Run processing/EDA notebooks in notebooks/ to generate cleaned outputs in data/silver/

Roadmap
 Ingest National Collision Database (NCDB)

 Initial EDA and data cleaning

 Integrate external weather data (Environment and Climate Change Canada)

 Build Prophet + XGBoost forecasting model

 Develop Power BI “Control Tower” dashboard (Risk Coverage Ratio + thresholds)

Data & Governance Notes
Public datasets are used for ingestion (NCDB and planned external drivers)

Any donor/donation data integration must follow privacy, security, and governance requirements (aggregation, de-identification, access controls)

Author
Hit Rajput
Focus: Data Science, Machine Learning, and Business Intelligence in Healthcare
