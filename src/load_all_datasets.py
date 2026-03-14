#load_all_datasets.py - The MASTER Data Loader (ALL 29 Datasets!)
#The comprehensive data loading script in the project. It scans your data/raw/ folder and loads ALL 29 datasets into PostgreSQL automatically.
#Purpose - Automatically finds and loads ALL 29 datasets into PostgreSQL

#imports and setup
import pandas as pd
from sqlalchemy import create_engine, types
import urllib.parse
from pathlib import Path
import glob

#set password
password = urllib.parse.quote_plus("atlantic2026!")
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/postgres')

print("-"*60)
print("LOADING ALL ATLANTIC CANADA DATASETS")
print("-"*60)

#get all CSV files
csv_files = list(Path("data/raw").glob("*.csv"))
xlsx_files = list(Path("data/raw").glob("*.xlsx"))
#counts CSV and Excel files
print(f"\nFound {len(csv_files)} CSV files and {len(xlsx_files)} Excel files")

# =====================================
# 1. LOAD RENTAL MARKET REPORTS (Excel 2019-2025)
# =====================================
print("\nLoading Rental Market Reports...")
rental_data = []

for file in xlsx_files:
    if "rmr-canada" in file.name:
        print(f"  Reading {file.name}...")
        try:
            # Try different sheets
            df = pd.read_excel(file, sheet_name=0)  # First sheet
            df['source_file'] = file.name
            rental_data.append(df)
        except Exception as e:
            print(f"    Error: {e}")

if rental_data:
    all_rentals = pd.concat(rental_data, ignore_index=True)
    all_rentals.to_sql('cmhc_rental_reports', engine, if_exists='replace', index=False)
    print(f"  Loaded {len(all_rentals)} rows to 'cmhc_rental_reports'")

# =====================================
# 2. LOAD VACANCY RATES
# =====================================
print("\n Loading Vacancy Rates...")
vacancy_files = [f for f in csv_files if "Vacancy" in f.name]

for file in vacancy_files:
    print(f"  Reading {file.name}...")
    df = pd.read_csv(file)
    table_name = f"vacancy_{file.stem.replace(' ', '_').lower()}"
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"    Loaded to '{table_name}'")

# =====================================
# 3. LOAD POPULATION DATA (FIXED VERSION)
# =====================================
print("\n Loading Population Data...")
pop_files = [f for f in csv_files if "Population" in f.name]

for file in pop_files:
    print(f"  Reading {file.name}...")
    try:
        df = pd.read_csv(file)
        
        #create short, meaningful table names
        if "estimatesby" in file.name.lower():
            table_name = "population_detailed"
        elif "estimates census" in file.name.lower():
            table_name = "population_estimates"
        elif "components" in file.name.lower():
            table_name = "population_components"
        else:
            #generic short name
            table_name = f"pop_{len(pop_files)}"
        
        print(f"    Saving as '{table_name}'...")
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"    Loaded {len(df)} rows to '{table_name}'")
        
        #show first few columns to understand the data
        print(f"    Columns: {list(df.columns)[:5]}...")
        
    except Exception as e:
        print(f"    Error with {file.name}: {e}")
# =====================================
# 4. LOAD INCOME DATA
# =====================================
print("\n Loading Income Data...")
income_files = [f for f in csv_files if "Income" in f.name or "Market income" in f.name]

for file in income_files:
    print(f"  Reading {file.name}...")
    df = pd.read_csv(file)
    table_name = f"income_{file.stem.replace(' ', '_').lower()}"
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"    Loaded to '{table_name}'")

# =====================================
# 5. LOAD AVERAGE RENTS BY CITY
# =====================================
print("\nLoading Average Rents by City...")
rent_files = [f for f in csv_files if "AverageRent" in f.name]

for file in rent_files:
    print(f"  Reading {file.name}...")
    df = pd.read_csv(file)
    table_name = f"rents_{file.stem.replace(' ', '_').lower()}"
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"    Loaded to '{table_name}'")

# =====================================
# 6. CREATE MASTER TABLE (FIXED WITH text())
# =====================================
print("\nCreating Master Table with all data...")

from sqlalchemy import text, inspect

#check what tables we have
inspector = inspect(engine)
all_tables = inspector.get_table_names()
print(f"Available tables: {len(all_tables)}")

with engine.connect() as conn:
    #drop existing master table if it exists (using text())
    conn.execute(text("DROP TABLE IF EXISTS atlantic_master"))
    conn.commit()
    print("Dropped existing master table")
    
    #create base master table with housing starts (using text())
    conn.execute(text("""
        CREATE TABLE atlantic_master AS
        SELECT 
            h.date,
            h.city as province,
            h.housing_starts
        FROM atlantic_housing_real h
        WHERE h.city != 'Atlantic provinces'
        ORDER BY h.date, h.city
    """))
    conn.commit()
    print("Created base master table")

#check the result
result = pd.read_sql("SELECT * FROM atlantic_master LIMIT 10", engine)
print("\nMaster table preview:")
print(result.to_string())

#count rows
count = pd.read_sql("SELECT COUNT(*) FROM atlantic_master", engine).iloc[0,0]
print(f"\n Master table created with {count} rows")

# =====================================
# 7. FINAL SUMMARY
# =====================================
print("\n" + "-"*60)
print("FINAL DATABASE SUMMARY")
print("-"*60)

from sqlalchemy import inspect
inspector = inspect(engine)

for table_name in sorted(inspector.get_table_names()):
    try:
        count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", engine).iloc[0,0]
        print(f"  - {table_name}: {count:>6} rows")
    except Exception as e:
        print(f"  - {table_name}: ? rows (error: {e})")

print("-"*60)

#show summary
print("\nTables in database:")
from sqlalchemy import inspect
inspector = inspect(engine)
for table_name in inspector.get_table_names():
    count = pd.read_sql(f"SELECT COUNT(*) FROM {table_name}", engine).iloc[0,0]
    print(f"  - {table_name}: {count} rows")

# THE 29 DATASETS THIS FILE LOADS
# RMR Excel Files	7	rmr-canada-2019-en.xlsx through rmr-canada-2025-en.xlsx
# Vacancy Rates	    4	Vacancy rates CMANovaS.csv, CMANewB.csv, CMAPEI.csv, CMANewFoundLand.csv
# Population Data	2+	Population estimates census metropolitan area.csv, Population estimatesby...
# Income Data	    8	IncomeDataNovaScotia.csv, IncomeDataNewBrunswick.csv, Market income CMANovaScotia.csv, etc.
# Average Rents	    5	AverageRentsHalifaxNovaScotia.csv, AverageRentsMonctonNewBrunswick.csv, etc.
# Housing Starts	1	statcan_housing_starts.csv (loaded elsewhere)
# Components	    2	Components of population change...
