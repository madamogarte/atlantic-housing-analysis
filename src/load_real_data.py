#load_real_data.py 
#This script loads the statcan_housing_starts CSV file into PostgreSQL database
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, types
import numpy as np
import urllib.parse

#password
raw_password = "atlantic2026!"
encoded_password = urllib.parse.quote_plus(raw_password)

#database connection with encoded password
engine = create_engine(f'postgresql://postgres:{encoded_password}@localhost:5432/postgres')

print("Connecting to database...")

#test connection first
try:
    with engine.connect() as conn:
        print("Database connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

#read the CSV file
try:
    df = pd.read_csv('data/raw/statcan_housing_starts.csv') 
    print(f"Loaded real data from CSV: {len(df)} rows")
    print(f"Columns found: {list(df.columns)}")
except FileNotFoundError:
    print("CSV file not found. Make sure statcan_housing_starts.csv is in data/raw/")
    exit()

#clean the data
print("\nCleaning data...")

# RENAME COLUMNS to match what your code expects
df = df.rename(columns={
    'REF_DATE': 'date',
    'GEO': 'city',
    'VALUE': 'housing_starts'
})

#convert date column properly
df['date'] = pd.to_datetime(df['date'])

# Add province mapping - FIXED: Using full province names, not abbreviations
province_map = {
    'Newfoundland and Labrador': 'Newfoundland and Labrador',
    'Prince Edward Island': 'Prince Edward Island', 
    'Nova Scotia': 'Nova Scotia',
    'New Brunswick': 'New Brunswick',
    'Atlantic provinces': 'Atlantic Provinces'
}
df['province'] = df['city'].map(province_map)

# Add placeholder columns (these will be filled by other datasets)
df['price'] = None
df['vacancy_rate'] = None
df['avg_rent'] = None
df['sales_volume'] = None

#remove any rows with missing critical data
df = df.dropna(subset=['housing_starts', 'city'])

print(f"After cleaning: {len(df)} rows")
print(f"Columns now: {list(df.columns)}")

# Drop unnecessary metadata columns
columns_to_keep = ['date', 'city', 'province', 'housing_starts', 'price', 
                   'vacancy_rate', 'avg_rent', 'sales_volume']
df = df[columns_to_keep]

#define SQL types for each column - FIXED: Increased province size
dtype_mapping = {
    'date': types.Date(),
    'city': types.VARCHAR(100),
    'province': types.VARCHAR(50),  # Changed from VARCHAR(2) to VARCHAR(50)
    'housing_starts': types.Integer(),
    'price': types.Numeric(10,2),
    'vacancy_rate': types.Numeric(5,2),
    'avg_rent': types.Numeric(10,2),
    'sales_volume': types.Integer()
}

#load into PostgreSQL
print("\nLoading into PostgreSQL...")

try:
    df.to_sql('atlantic_housing_real', 
              engine, 
              if_exists='replace', 
              index=False,
              dtype=dtype_mapping)
    print("Data loaded into PostgreSQL!")
    
except Exception as e:
    print(f"Error with to_sql: {e}")
    exit()

#verify the load
print("\nVerifying data load...")
try:
    with engine.connect() as conn:
        result = pd.read_sql("SELECT COUNT(*) FROM atlantic_housing_real", conn)
        print(f"Rows in database: {result.iloc[0,0]}")
        
        #show sample
        sample = pd.read_sql("""
            SELECT city, date, housing_starts, province
            FROM atlantic_housing_real 
            LIMIT 10
        """, conn)
        print("\nSample from database:")
        print(sample.to_string())
        
        #show summary by province
        summary = pd.read_sql("""
            SELECT 
                province,
                COUNT(*) as records,
                ROUND(AVG(housing_starts)) as avg_starts,
                ROUND(MIN(housing_starts)) as min_starts,
                ROUND(MAX(housing_starts)) as max_starts
            FROM atlantic_housing_real
            GROUP BY province
            ORDER BY avg_starts DESC
        """, conn)
        print("\nSummary by province:")
        print(summary.to_string(index=False))
        
except Exception as e:
    print(f"Could not verify: {e}")

print("\n Load process complete!")
