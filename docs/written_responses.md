# WRITTEN RESPONSES - ATLANTIC CANADA HOUSING ANALYSIS
---
## QUESTION 1: PROBLEM DEFINITION
**Describe the problem you chose to work on and why it is worth solving.**

### Problem Definition
This project analyzes housing starts across Atlantic Canada (Nova Scotia, New Brunswick, Prince Edward Island and Newfoundland and Labrador) to understand regional disparities and predict future construction activity. The core question is: *Why are some Atlantic provinces experiencing housing booms while others face decline and can we predict these patterns?*

### Context
Atlantic Canada has experienced unprecedented demographic shifts since 2020. Interprovincial migration from Ontario and British Columbia has created significant housing pressure in some provinces, while others face population decline and economic challenges:

- **Nova Scotia:** Halifax saw 202% growth in housing starts, yet prices remain unaffordable for many first time homebuyers
- **New Brunswick:** Moncton and Saint John experienced 245% growth, the fastest in Atlantic Canada
- **Prince Edward Island:** Charlottetown grew 198%, driven by remote workers and tourism
- **Newfoundland and Labrador:** Housing starts declined 50%, indicating population loss and economic challenges

Current decision making relies on anecdotal evidence and lagging indicators. Without predictive analytics, millions in housing investments may be misallocated and vulnerable communities may not receive the support they need.

### Who Benefits

| Stakeholder | How They Benefit |
|-------------|------------------|
| **Policymakers** | Target affordable housing funding to provinces with highest demand |
| **Developers** | Identify growth markets for new construction projects |
| **Homebuyers** | Understand which regions offer affordable options |
| **Economists** | Track regional economic indicators for policy planning |
| **Urban Planners** | Make data driven decisions about infrastructure investment |

### Useful Outcome
A predictive model that:

- Achieves **>95% accuracy** in forecasting housing starts 12 months ahead
- Identifies the top factors driving construction in each province
- Quantifies regional disparities to guide evidence based decision making

**Result Achieved:** Linear Regression model with **99.3% accuracy** (R²=0.993), identifying that New Brunswick grew 245% while Newfoundland declined 50%. The model reveals that location (specifically Halifax) accounts for 95% of predictive power, confirming that Atlantic Canada is not one unified market but rather distinct regional economies.

---

## QUESTION 2: APPROACH & TOOL SELECTION
**Explain how you decided to approach the problem and which tools or techniques you selected.**

### High Level Approach
This project was approached as a time series regression problem with the following strategy:

1. **Data Acquisition:** Downloaded 29 datasets from Statistics Canada and CMHC covering 2015-2022
2. **Data Processing:** Cleaned inconsistent formats, handled missing values and integrated into PostgreSQL
3. **Feature Engineering:** Created 19 features including lag variables and rolling averages
4. **Model Development:** Trained and compared 4 regression models
5. **Insight Generation:** Used Generative AI to translate technical results into plain language recommendations

### Specific Tools and Techniques

| Tool | Purpose | Why Appropriate |
|------|---------|------------------|
| **PostgreSQL** | Database management | Handles 29 integrated tables with complex joins; reliable for structured data |
| **Pandas/NumPy** | Data cleaning and manipulation | Efficient for handling missing values and transforming date formats |
| **Scikit-learn** | ML model implementation | Provides consistent API for Linear Regression, Ridge and Random Forest |
| **XGBoost** | Gradient boosting comparison | Industry standard for tabular data; benchmark against simpler models |
| **Matplotlib/Seaborn** | Visualization | Publication quality graphs for provincial comparisons |
| **OpenAI API** | Generative AI | Translates technical metrics into stakeholder friendly insights |

### The 29 Datasets
The project integrates data from multiple Statistics Canada tables:

| Category | Count | Examples |
|----------|-------|----------|
| Housing Starts | 1 | `statcan_housing_starts.csv` (Table 34-10-0139-01) |
| Vacancy Rates | 4 | Vacancy rates for NS, NB, PEI, NL |
| Income Data | 8 | Market income and detailed income data for all provinces |
| Population Data | 2+ | Population estimates and components of change |
| Average Rents | 5 | City level rent data for Halifax, Moncton, Saint John, St. John's, Charlottetown |
| RMR Reports | 7 | CMHC Rental Market Reports 2019-2025 |
| **TOTAL** | **29** | **Complete Atlantic Canada housing dataset** |

### Why These Choices Were Appropriate

- **PostgreSQL** was chosen over SQLite because it handles concurrent connections and complex joins across 29 tables without performance degradation
- **Linear Regression** was selected as the primary model because initial EDA showed strong linear relationships in lag features; it also offers interpretability for stakeholders
- **Random Forest and XGBoost** were included as benchmarks to validate that simpler models weren't missing complex patterns
- **Generative AI** bridges the gap between technical R² scores and practical recommendations for non technical users

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| SQLite | Limited concurrent access; slower with 29 integrated tables |
| Tableau only | Would provide visualization but miss predictive capability |
| TensorFlow/Deep Learning | Overkill for structured tabular data; simpler models achieved 99.3% accuracy |
| ARIMA/Time Series models | Cannot incorporate external features (income, vacancy rates) that proved valuable |

### Tradeoffs Acknowledged

- **Complexity vs Interpretability:** Random Forest had slightly lower accuracy (97.5%) than Linear Regression (99.3%) but was harder to explain to stakeholders
- **Data Volume vs Granularity:** Provincial data was complete but city level data had gaps; chose provincial for reliability
- **Recency vs History:** 2015-2022 data captures pre and post pandemic trends but excludes 2023-2024

---

## QUESTION 3: REFLECTION
**Write a reflection on what you learned by completing this project.**

### What Worked Better Than Expected

**Data integration** was surprisingly smooth. PostgreSQL handled joining 29 tables without performance issues and the final master table with 128 rows and 19 features loaded in seconds. I expected database bottlenecks but the schema design proved efficient.

**Model performance** exceeded expectations. Linear Regression achieved **99.3% accuracy** (R²=0.993) far above my 95% target. The MAE of 116 housing starts means predictions are off by only 116 units on average, which is precise enough for policy decisions.

**Generative AI integration** worked better than anticipated. Initially planned as a "nice to have," the AI insights actually revealed patterns I'd missed particularly the contrast between booming mainland provinces and declining Newfoundland.

**Feature importance** revealed something fascinating: Halifax alone accounts for 95% of predictive power. This confirmed that Atlantic Canada isn't one unified market, it's Halifax plus everyone else. The model taught me something about the region I didn't fully appreciate before.

### What Worked Worse Than Expected

**Data cleaning** consumed **80% of project time** far more than anticipated. The raw CSV files had:

- Inconsistent date formats (some had full dates, others just years)
- Column names with spaces requiring careful quoting in SQL
- Missing values that broke initial pipeline runs

**Rental data** proved problematic. The `TO_DATE()` function failed on columns containing only year numbers, requiring conditional logic to check data types before processing. Several rent tables showed "No data" despite existing files, indicating column naming mismatches.

**Population tables** were unavailable. Despite multiple attempts, population estimates tables weren't found in the database, limiting demographic features in the model.

### Challenges and Limitations

| Challenge | Impact | Solution |
|-----------|--------|----------|
| Date format inconsistencies | Broke initial data loading | Added conditional logic to detect and handle both string dates and year numbers |
| Missing population data | Couldn't include demographic features | Model still achieved 99.3% accuracy without them |
| Rental data formatting issues | Some rent tables didn't load | Focused on income data which loaded successfully |
| Data latency | Latest data only goes to 2022 | Acknowledged in limitations; future work can update |

### What I Would Change Next Time

1. **Build validation checks earlier.** I spent weeks debugging only to discover date format issues. Next time, I'd write a data validation script first to check column types, missing values and date formats before any analysis.

2. **Include interest rate and mortgage data.** Current model captures supply side factors (vacancy rates, housing starts) but misses financing costs that influence buyer demand.

3. **Create an interactive dashboard.** Stakeholders would benefit from a Streamlit app where they could explore predictions by province and scenario.

4. **Automate data refresh.** Manual downloads limit the model to 2022 data; an API pipeline would enable real time updates.

5. **Add city level granularity.** Provincial aggregates mask intra provincial variation (e.g., Halifax vs rural Nova Scotia).

### What This Project Taught Me

**Data preparation is the real work.** The course emphasized algorithms, but this project revealed that 80% of data science is cleaning, transforming and integrating data. Models are only as good as the data feeding them.

**Simple tools often outperform complex ones.** Linear Regression beat Random Forest and XGBoost on this structured data. I learned to start simple and add complexity only when justified, not because "more advanced" means "better."

**Domain context matters as much as technical metrics.** The model's 99.3% accuracy is impressive, but the real value is the insight it generated: New Brunswick grew 245% while Newfoundland declined 50%. Numbers without context are meaningless.

**Stakeholder communication is half the job.** Generative AI helped translate R² scores into plain language, but I also learned to frame results around the original problem: helping policymakers target housing investments where they're needed most.

**Real world data is messy.** The Statistics Canada data I downloaded looked clean, but it had inconsistent formats, missing values and column naming issues. Working with real data taught me patience and problem solving skills no textbook could provide.

---

*This project taught me that real world data science is 20% modeling and 80% everything else ... data wrangling, stakeholder communication and problem framing. The technical skills matter, but judgment about which problems to solve and how to frame solutions matters more.*
