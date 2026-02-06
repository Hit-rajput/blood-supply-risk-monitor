# Supply Risk Monitor: Predictive Blood Demand & Supply Forecasting  
### *Trauma-driven demand forecasting and supply risk early warning for Canada*

![Status](https://img.shields.io/badge/Current_Phase-Prototype_&_Ingestion-orange?style=for-the-badge&logo=python)

Blood products are highly perishable, making effective stockpile management critical. This project aims to build a "Control Tower" to forecast trauma-driven demand and identify potential supply risks.

---

## ⚠️ Problem Statement

Operational teams need earlier signals for blood shortage risks. The Supply Risk Monitor leverages national collision data and external factors to predict demand spikes caused by trauma events.

---

## 🚀 Current Status

The project is currently in the **Prototyping & Ingestion** phase. The codebase is primarily **Notebook-driven**.

### ✅ Implemented Features
*   **Data Ingestion**: Automated download and standardization of National Collision Database (NCDB) data (1999-2021) from the Open Canada API.
*   **Forecasting Model**: A Baseline **Facebook Prophet** model has been trained and tested to capture trends and seasonality in collision data.
*   **Data Analysis**: Exploratory analysis notebooks for Toronto and NCDB datasets.

### �  Work in Progress / Roadmap
*   **Hybrid Engine**: Integration of XGBoost for residual error correction (currently planned/claimed but not yet implemented in code).
*   **Genetic Algorithm**: Hyperparameter optimization for the hybrid model.
*   **Productionization**: Refactoring notebook logic (`src/models`, `src/transform`) into executable Python scripts (`.py`).

---

## 📂 Project Structure

```
├── data/               # Raw and processed data
├── notebooks/          # Analysis and prototyping notebooks
│   ├── Analyze.ipynb   # Model analysis
│   ├── ingest_ncdb.ipynb # NCDB data ingestion
│   └── ...
├── src/                # Source code (currently undergoing refactoring)
│   ├── ingest/         # Data ingestion scripts/notebooks
│   ├── models/         # Forecasting models (Prophet)
│   └── transform/      # Data cleaning and transformation
└── ...
```

---

## 🛠️ Tech Stack

*   **Ingestion:** Python (Requests, Pandas)
*   **Modeling:** Facebook Prophet
*   **Data Manipulation:** Pandas
*   **Environment:** Jupyter Notebooks

---

## 🔧 Usage

Currently, the workflow is executed via Jupyter Notebooks:

1.  **Ingest Data**: Run `src/ingest/ingest_ncdb.ipynb` to download collision data.
2.  **Train Model**: Run `src/models/prophet_train.ipynb`.
3.  **Test Model**: Run `src/models/Final_Model_test.ipynb`.

---

## 🎯 Objectives (Future)

*   Build a robust trauma-driven **Demand Index**.
*   Forecast short-horizon risk to support proactive collection planning.
*   Operationalize a decision metric: the **Risk Coverage Ratio**.
