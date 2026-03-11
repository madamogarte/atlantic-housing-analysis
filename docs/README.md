\# Atlantic Canada Housing Market Analysis



\## Overview

This project analyzes housing starts across Atlantic Canada (Nova Scotia, New Brunswick, Prince Edward Island, Newfoundland and Labrador) using 29 datasets from Statistics Canada and CMHC (2015-2022).

\## Data Files

All 29 original datasets are available in the [`data/raw/`](data/raw/) folder:
- Vacancy rates for all 4 provinces
- Income data (market income and detailed income)
- Population estimates
- Average rents for all major Atlantic cities
- CMHC Rental Market Reports (2019-2025)

These files were downloaded from Statistics Canada and CMHC.

\## Key Results

\- \*\*Best Model:\*\* Linear Regression (R² = 0.993, MAE = 116 units)

\- \*\*Top Growth:\*\* New Brunswick (+245%), Nova Scotia (+202%)

\- \*\*Declining:\*\* Newfoundland (-50%)

\- \*\*Features Engineered:\*\* 19

\- \*\*Database Tables:\*\* 24 tables with 10,000+ rows



\## Visualizations in `outputs/`

\- `real\_housing\_visualizations.png` - Main dashboard

\- `feature\_importance.png` - Key drivers

\- `real\_predictions.png` - Model accuracy

\- `real\_housing\_trends.png` - Provincial trends

\## Setup

1\. Install Python 3.9+

2\. Install PostgreSQL

3\. Run: `pip install -r requirements.txt`

4\. Set password: `atlantic2026!`

5\. Run: `python src/load\_all\_datasets.py`

6\. Run: `python src/enhanced\_ml\_model\_final.py`

\## Source Code Documentation

For detailed explanations of each Python script, see:
[`src/README.md`](src/README.md)

\## Visualizations

All graphs are in the [`outputs/`](outputs/) folder with detailed explanations in [`outputs/README.md`](outputs/README.md)

Key visualizations include:
- `real_housing_visualizations.png` - Main dashboard (4 charts)
- `feature_importance.png` - What drives housing starts
- `real_predictions.png` - Model accuracy (99%!)




