# Supply Risk Monitor: Predictive Blood Demand & Supply Forecasting  
### *Trauma-driven demand forecasting and supply risk early warning for Canada*

![Status](https://img.shields.io/badge/Current_Phase-Modeling_&_Optimization-blue?style=for-the-badge&logo=python)

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

## 📉 Core Metric: Risk Coverage Ratio (RCR)

The system calculates a daily/weekly **Risk Coverage Ratio**:

$$RCR_t = \frac{\text{Predicted Supply Capacity}_t}{\text{Predicted Trauma Demand Index}_t}$$

- **RCR > 1.2 (Green):** Safe buffer.
- **1.0 < RCR < 1.2 (Yellow):** Warning zone.
- **RCR < 1.0 (Red):** Projected deficit (Code Red).

---

## 🏗️ Architecture: Hybrid Residual Learning

We utilize a two-stage **Hybrid Forecasting Engine** to capture both stable trends and sudden shocks:

1.  **Baseline Model (Facebook Prophet):** Captures long-term trend and annual seasonality (e.g., Summer peaks, December dips).
2.  **Residual Corrector (XGBoost):** Predicts the *error* of the baseline model by analyzing exogenous shocks:
    * **Weather:** Snow depth, precipitation, and freezing rain conditions.
    * **Calendar:** "Double Jeopardy" long weekends (high demand + low supply).
    * **National Signal:** Transfer learning from the 22-year National Collision Database.

*Optimization Note:* The XGBoost hyperparameters are fine-tuned using a **Genetic Algorithm** to prevent overfitting on the limited recent data.

---

## 🛠️ Tech Stack

- **Ingestion:** Python (Pandas, Meteostat API)
- **Processing:** Polars / Pandas
- **Modeling:** Prophet, XGBoost, Scikit-Learn (Genetic Opt)
- **Visualization:** Matplotlib, Seaborn
- **Orchestration:** Jupyter Notebooks

### Installation

```bash
pip install polars pandas matplotlib seaborn prophet xgboost meteostat sklearn-genetic-opt
