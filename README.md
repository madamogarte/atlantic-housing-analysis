# Atlantic Canada Housing Market Analysis

[![Python](https://img.shields.io/badge/Python-3.9-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Accuracy](https://img.shields.io/badge/Accuracy-99.3%25-brightgreen)](https://github.com/madamogarte/atlantic-housing-analysis)

Housing starts analysis across Atlantic Canada using **29 datasets** from Statistics Canada and CMHC (2015-2022).

---

## Overview

This project analyzes housing starts across Nova Scotia, New Brunswick, Prince Edward Island, and Newfoundland and Labrador to understand regional disparities and predict future construction activity. The machine learning model achieves **99.3% accuracy** in forecasting housing starts.

---

## Key Results

| Province | Avg Housing Starts | Growth | Status |
|----------|-------------------|--------|--------|
| **Nova Scotia** | 5,517 | **+202%** | BOOMING |
| **New Brunswick** | 2,217 | **+245%** | EXPLOSIVE |
| **PEI** | 596 | **+198%** | BOOMING |
| **Newfoundland** | 742 | **-50%** | DECLINING |

**Best Model:** Linear Regression (R² = 0.993, MAE = 116 housing starts)

---

## Repository Structure

```
atlantic-housing-analysis/
│
├── src/                                # All Python source code
│   ├── enhanced_ml_model_final.py      # MAIN ML MODEL (99.3% accuracy)
│   ├── load_all_datasets.py            # Loads 29 datasets into PostgreSQL
│   ├── visualize_real_data.py          # Creates professional visualizations
│   ├── create_analysis_tables.py       # Creates summary tables
│   ├── genai_integration.py            # Generative AI component
│   ├── load_real_data.py               # Loads housing starts data
│   ├── inspect_tables.py               # Database inspector
│   └── test_password.py                # Database connection tester
│
├── outputs/                             # All visualizations
│   ├── real_housing_visualizations.png  # Main dashboard (4 charts)
│   ├── real_housing_trends.png          # Trend lines
│   ├── real_predictions.png             # Model accuracy (99%)
│   ├── feature_importance.png           # What drives housing starts
│   ├── predictions_vs_actual.png        # Earlier model comparison
│   └── predictions_2025.png             # Future forecasts
│
├── docs/                                # Documentation
│   ├── written_responses.md             # Answers to 3 capstone questions
│   ├── DATA_SOURCES.md                  # Complete dataset inventory
│   └── requirements.txt                 # Python package dependencies
│
├── data/                                # Data files
│   └── raw/                             # 29 original CSV/Excel files
│
├── README.md                            # This file
└── .gitignore                           # Files excluded from GitHub
```
---

## Visualizations

| Graph | Description |
|-------|-------------|
| `real_housing_visualizations.png` | 4-panel dashboard showing trends across provinces |
| `feature_importance.png` | Halifax dominates (95% of predictive power!) |
| `real_predictions.png` | Model accuracy - 99% predictions hug the perfect line |

**[See all visualizations with explanations](outputs/README.md)**

---
## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/madamogarte/atlantic-housing-analysis.git
   cd atlantic-housing-analysis
2. **Create and activate Conda environment**
   ```conda create -n atlantic-housing python=3.9 -y
   conda activate atlantic-housing
3. **Install Python dependencies**   
   ```
   pip install -r docs/requirements.txt
   
4. **Set up PostgreSQL database**
   ```
   - Download PostgreSQL from postgresql.org
   - Use default port: 5432
   - Set password to: atlantic2026!
     
5. **Load all 29 datasets**
    ```
    python src/load_all_datasets.py
    
6. **Run the machine learning model**
    ```
    python src/enhanced_ml_model_final.py

---
### Expected Results

After running the model, you should see:

- **Linear Regression**: \( R^2 = 0.993 \) (99.3% accuracy)
- **Mean Absolute Error**: 116 housing starts
- **Provincial Growth**:
  - **New Brunswick**: +245% 
  - **Nova Scotia**: +202% 
  - **Prince Edward Island**: +198% 
  - **Newfoundland and Labrador**: -50%
 ---
### Data Sources

All 29 datasets are from:
- **Statistics Canada**: - Housing starts, income, population estimates
- **CMHC**: - Rental market reports, vacancy rates
  
**[View Complete Data Sources Inventory](docs/DATA_SOURCES.md)**

The inventory includes:
- Table numbers for each Statistics Canada dataset
- Descriptions of what each file contains
- Download instructions and links
---

### Written Responses
**[View Answers to the three capstone questions](docs/written_responses.md)**

---

### Key Achievements
- 29 datasets integrated from Statistics Canada and CMHC
- 24 database tables created with 10,000+ rows
- 19 features engineered for machine learning
- 4 ML models trained and compared
- 99.3% accuracy in predicting housing starts
- 6 professional visualizations
- Generative AI insights generator

---

## Walkthrough Video

**[Watch the video on OneDrive](https://1drv.ms/v/c/30554cb0ac0697d4/IQDW-KtgdAADT5XdNtW-Y0sfAcmUfQDzdTfMEYCLwhlD6Lg)**

**Video Contents:**
- Introduction & Problem Definition
- Data Processing (29 datasets loaded)
- Machine Learning (99.3% accuracy!)
- Visualizations & Results
- Generative AI Insights
- Limitations & Conclusion
---

###  License
This project is licensed under the MIT License - see [LICENSE](https://github.com/madamogarte/atlantic-housing-analysis/blob/main/LICENSE) file for details

---

###  Author
madamogarte - [GitHub Profile](https://github.com/madamogarte)

Student ID: DA21080_AnnaLynOgarte_DA-Blue

---

###  Acknowledgments
- Statistics Canada for providing public data
- CMHC for rental market reports
- Skills for Hire Atlantic program

---

### Questions?
Contact me : ogarteams@gmail.com


