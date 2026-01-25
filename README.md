# blood-supply-risk-monitor

# Ingest scripts
touch src/ingest/ingest_ncdb.py
touch src/ingest/ingest_weather.py
touch src/ingest/ingest_toronto_collisions.py
touch src/ingest/ingest_demographics.py
touch src/ingest/ingest_holidays.py

# Transform + models + utils
touch src/transform/cleaners.py
touch src/models/forecast.py
touch src/utils/db_connector.py
touch src/utils/helpers.py

# Data layers
mkdir -p data/{bronze,silver,gold}

# SQL

# Notebooks
mkdir notebooks
touch notebooks/exploratory_analysis.ipynb

# Tests
mkdir tests
touch tests/__init__.py

# Docs
mkdir docs
touch docs/data_dictionary.md
