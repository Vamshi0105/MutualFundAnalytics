# Bluestock Mutual Fund Analytics Capstone

## Overview
End-to-end mutual fund analytics pipeline with ETL, SQLite storage, EDA, performance analytics, risk metrics, and an interactive dashboard.

## Project structure
- data/
- scripts/
- notebooks/
- outputs/
- dashboard/
- reports/

## Setup
```bash
pip install -r requirements.txt
```

## Run the pipeline
```bash
python scripts/run_ETL.py
```

## Launch the dashboard
Tableau: open dashboard/bluestock_mf_dashboard.twbx
Streamlit:
```bash
streamlit run app.py
```

## Outputs
- fund_scorecard.csv
- cagr_comparison.csv
- sharpe_ratio.csv
- drawdown.csv
- var_cvar.csv
