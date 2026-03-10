\# Atlantic Canada Housing Market Analysis



\## Overview

This project analyzes housing starts across Atlantic Canada (Nova Scotia, New Brunswick, Prince Edward Island, Newfoundland and Labrador) using 29 datasets from Statistics Canada and CMHC (2015-2022).



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

