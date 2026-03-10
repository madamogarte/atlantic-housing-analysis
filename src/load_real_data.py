#load_real_data.py
#This script loads the primary housing starts CSV file into PostgreSQL database

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
    df = pd.read_csv('data/raw/cmhc_atlantic_housing.csv')
    print(f"Loaded real data from CSV: {len(df)} rows")
except FileNotFoundError:
    print("CSV file not found. Run download_cmhc_data.py first!")
    exit()

#clean the data
print("\n Cleaning data...")

#convert date column properly
df['date'] = pd.to_datetime(df['date'])

#remove any rows with missing critical data
df = df.dropna(subset=['price', 'city'])

#remove outliers (prices that are too extreme)
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['price'] >= Q1 - 3*IQR) & (df['price'] <= Q3 + 3*IQR)]

print(f" After cleaning: {len(df)} rows")

#define SQL types for each column
dtype_mapping = {
    'date': types.Date(),
    'price': types.Numeric(10,2),
    'vacancy_rate': types.Numeric(5,2),
    'avg_rent': types.Numeric(10,2),
    'housing_starts': types.Integer(),
    'sales_volume': types.Integer(),
    'city': types.VARCHAR(50),
    'province': types.VARCHAR(2)
}

#load into PostgreSQL
print("\n Loading into PostgreSQL...")

try:
    df.to_sql('atlantic_housing_real', 
              engine, 
              if_exists='replace', 
              index=False,
              dtype=dtype_mapping)
    print(" Data loaded into PostgreSQL!")
    
except Exception as e:
    print(f" Error with to_sql: {e}")
    
    #alternative method if the first one fails
    print("\n Trying alternative method...")
    
    #create connection and load manually
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password=raw_password  # Use raw password for psycopg2
    )
    cur = conn.cursor()
    
    #create table manually
    cur.execute("""
        DROP TABLE IF EXISTS atlantic_housing_real;
        CREATE TABLE atlantic_housing_real (
            date DATE,
            city VARCHAR(50),
            province VARCHAR(2),
            price DECIMAL(10,2),
            vacancy_rate DECIMAL(5,2),
            avg_rent DECIMAL(10,2),
            housing_starts INTEGER,
            sales_volume INTEGER
        );
    """)
    
    #insert data row by row
    for idx, row in df.iterrows():
        cur.execute("""
            INSERT INTO atlantic_housing_real 
            (date, city, province, price, vacancy_rate, avg_rent, housing_starts, sales_volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['date'].date(), 
            row['city'], 
            row['province'], 
            float(row['price']),
            float(row['vacancy_rate']),
            float(row['avg_rent']),
            int(row['housing_starts']),
            int(row['sales_volume'])
        ))
        
        #show progress every 100 rows
        if (idx + 1) % 100 == 0:
            print(f"  Inserted {idx + 1} rows...")
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Alternative method successful! Inserted {len(df)} rows.")

#verify the load
print("\nVerifying data load...")
try:
    with engine.connect() as conn:
        result = pd.read_sql("SELECT COUNT(*) FROM atlantic_housing_real", conn)
        print(f"Rows in database: {result.iloc[0,0]}")
        
        #show sample
        sample = pd.read_sql("""
            SELECT city, date, price, vacancy_rate 
            FROM atlantic_housing_real 
            LIMIT 10
        """, conn)
        print("\n Sample from database:")
        print(sample.to_string())
        
        #show summary by city
        summary = pd.read_sql("""
            SELECT 
                city,
                COUNT(*) as records,
                ROUND(AVG(price)) as avg_price,
                ROUND(MIN(price)) as min_price,
                ROUND(MAX(price)) as max_price
            FROM atlantic_housing_real
            GROUP BY city
            ORDER BY avg_price DESC
        """, conn)
        print("\n Summary by city:")
        print(summary.to_string(index=False))
        
except Exception as e:
    print(f" Could not verify: {e}")