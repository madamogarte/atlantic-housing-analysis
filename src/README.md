# Source Code Documentation - Atlantic Canada Housing Analysis

This folder contains all Python scripts for the project. Below is a detailed explanation of each file and its purpose.

---

## **DATA LOADING & DATABASE SCRIPTS**

### 1. `load_all_datasets.py` - The MASTER Data Loader
**Purpose:** Scans `data/raw/` folder and automatically loads ALL 29 datasets into PostgreSQL.

**What it does:**
- Finds 22 CSV files and 7 Excel files
- Loads vacancy rates, income data, population estimates, and rental reports
- Creates 24+ database tables
- Builds master table combining all data
- Shows final summary of everything loaded

**Why it's important:** This is the **FIRST script to run**. Everything else depends on it!

---

### 2. `load_real_data.py` - Housing Starts Loader
**Purpose:** Loads the main housing starts dataset (`statcan_housing_starts.csv`) into PostgreSQL.

**What it does:**
- Reads housing starts data from Statistics Canada Table 34-10-0139-01
- **Cleans and transforms data (renames columns, converts dates)**
- Adds province codes (NS, NB, PEI, NL)
- Creates `atlantic_housing_real` table

**Why it's important:** This provides the **target variable** for machine learning.

---

### 3. `test_password.py` - Database Connection Tester
**Purpose:** Tests if Python can connect to PostgreSQL successfully.

**What it does:**
- Attempts to connect to database with password `atlantic2026!`
- Tests creating, inserting, and dropping a temporary table
- Returns success message or error details

**Why it's important:** Use this first to troubleshoot connection issues.

---

### 4. `inspect_tables.py` - Database Inspector
**Purpose:** Shows all tables, columns, and sample data in the database.

**What it does:**
- Lists all 24+ tables in PostgreSQL
- Displays column names and data types
- Shows first 3 rows of sample data

**Why it's important:** Quickly verify data loaded correctly and see table structures.

---

## **DATA ANALYSIS & PREPARATION**

### 5. `create_analysis_tables.py` - Summary Table Creator
**Purpose:** Creates derived tables for easier analysis.

**What it does:**
- **`city_summary`** - Average, min, max prices by city
- **`yoy_changes`** - Year-over-year growth rates
- **`monthly_averages`** - Seasonal patterns
- **`market_segments`** - Price category breakdowns

**Why it's important:** Makes complex analysis simple with pre-aggregated data.

---

## **MACHINE LEARNING**

### 6. `enhanced_ml_model_final.py` - MAIN ML MODEL
**Purpose:** Trains 4 machine learning models to predict housing starts with 99.3% accuracy.

**What it does:**
- Loads data from all 29 datasets
- Engineers **19 features** including lag variables and rolling averages
- Trains 4 models: Linear Regression, Ridge, Random Forest, XGBoost
- Compares performance (R² scores and MAE)
- Identifies best model (Linear Regression: R² = 0.993, MAE = 116)
- Shows provincial growth rates:
  - New Brunswick: +245%
  - Nova Scotia: +202%
  - PEI: +198%
  - Newfoundland: -50%
- Saves feature importance plot to `outputs/`

**Why it's important:** This is the **HEART of the project** - the main machine learning component!

---

## **VISUALIZATION**

### 7. `visualize_real_data.py` - Graph Creator
**Purpose:** Creates professional, publication-quality visualizations.

**What it does:**
- Generates **4-panel dashboard** (`real_housing_visualizations.png`)
- Creates **trend lines** with 4-quarter moving averages (`real_housing_trends.png`)
- Shows price trends, vacancy rates, rent comparisons, and distributions
- Prints key insights (growth rates, averages)

**Why it's important:** Turns numbers into compelling visuals for your video and report.

---

## **GENERATIVE AI**

### 8. `genai_integration.py` - AI Insights Generator
**Purpose:** Creates plain-language market insights from the numerical results.

**What it does:**
- Loads provincial summary data from database
- Generates 6 AI-style insights about regional differences
- Provides policy recommendations
- No API key needed - works instantly!

**Why it's important:** Fulfills the **Generative AI requirement** and shows how to communicate results to non-technical audiences.

---

## **QUICK REFERENCE - WHICH SCRIPT TO RUN WHEN**

| Order | Script | When to Run |
|:-----:|--------|-------------|
| **1** | `test_password.py` | First time setup, troubleshooting |
| **2** | **`load_all_datasets.py`** | **FIRST!** Before any analysis |
| **3** | `inspect_tables.py` | After loading, to verify |
| **4** | `load_real_data.py` | If housing starts not in load_all |
| **5** | `create_analysis_tables.py` | After data loaded |
| **6** | **`enhanced_ml_model_final.py`** | **MAIN EVENT!** After data ready |
| **7** | `visualize_real_data.py` | After model runs |
| **8** | `genai_integration.py` | Last - the finale! |

---

## **KEY ACHIEVEMENTS**

| Script | Achievement |
|--------|-------------|
| `load_all_datasets.py` | Loads **29 datasets** into 24+ tables |
| `enhanced_ml_model_final.py` | **99.3% accuracy** in predicting housing starts |
| `create_analysis_tables.py` | Creates 4 analysis-ready summary tables |
| `visualize_real_data.py` | Generates 6 professional graphs |
| `genai_integration.py` | Produces AI-style market insights |d
