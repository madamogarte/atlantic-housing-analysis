#create_analysis_tables.py - Creates summary statistics and derived tables from housing data for Analysis
#This script takes raw housing data and creates summary tables in PostgreSQL that make analysis easier. 

# This file takes raw housing data and creates:
# - city_summary: Average prices by city
# - yoy_changes: Year-over-year growth rates
# - monthly_averages: Trends over time
# - market_segments: Groups cities by price ranges


import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse

#password
raw_password = "atlantic2026!"
encoded_password = urllib.parse.quote_plus(raw_password)

#database connection
engine = create_engine(f'postgresql://postgres:{encoded_password}@localhost:5432/postgres')

print("-"*50)
print("CREATING ANALYSIS TABLES")
print("-"*50)

#test connection 
try:
    with engine.connect() as conn:
        print("Connected to database")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

#check if source table exists
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'atlantic_housing_real'
        );
    """))
    exists = result.fetchone()[0]
    
    if not exists:
        print("Table 'atlantic_housing_real' doesn't exist!")
        print("Please run load_real_data.py first.")
        exit()
    else:
        print("Source table 'atlantic_housing_real' found")

#create analysis tables
with engine.connect() as conn:
    
    # 1. city summary table
    print("\nCreating city_summary table...")
    conn.execute(text("""
        DROP TABLE IF EXISTS city_summary;
        CREATE TABLE city_summary AS
        SELECT 
            city,
            province,
            MIN(date) as first_date,
            MAX(date) as last_date,
            COUNT(*) as record_count,
            ROUND(AVG(price)::numeric, 2) as avg_price,
            ROUND(MIN(price)::numeric, 2) as min_price,
            ROUND(MAX(price)::numeric, 2) as max_price,
            ROUND(AVG(vacancy_rate)::numeric, 2) as avg_vacancy,
            ROUND(AVG(avg_rent)::numeric, 2) as avg_rent
        FROM atlantic_housing_real
        GROUP BY city, province
        ORDER BY avg_price DESC;
    """))
    
    # 2. Year-over-year changes
    print("Creating yoy_changes table (year over year)...")
    conn.execute(text("""
        DROP TABLE IF EXISTS yoy_changes;
        CREATE TABLE yoy_changes AS
        SELECT 
            city,
            date,
            price,
            LAG(price, 12) OVER (PARTITION BY city ORDER BY date) as price_1y_ago,
            ROUND(
                ((price / LAG(price, 12) OVER (PARTITION BY city ORDER BY date) - 1) * 100)::numeric, 
                2
            ) as yoy_growth_percent
        FROM atlantic_housing_real
        ORDER BY city, date;
    """))
    
    # 3. Monthly averages
    print("Creating monthly_averages table...")
    conn.execute(text("""
        DROP TABLE IF EXISTS monthly_averages;
        CREATE TABLE monthly_averages AS
        SELECT 
            city,
            EXTRACT(YEAR FROM date) as year,
            EXTRACT(MONTH FROM date) as month,
            ROUND(AVG(price)::numeric, 2) as avg_price,
            ROUND(AVG(vacancy_rate)::numeric, 2) as avg_vacancy,
            ROUND(AVG(avg_rent)::numeric, 2) as avg_rent,
            SUM(housing_starts) as total_housing_starts
        FROM atlantic_housing_real
        GROUP BY city, year, month
        ORDER BY city, year, month;
    """))
    
    # 4. Market segments (by price range)
    print("Creating market_segments table...")
    conn.execute(text("""
        DROP TABLE IF EXISTS market_segments;
        CREATE TABLE market_segments AS
        SELECT 
            city,
            CASE 
                WHEN price < 250000 THEN 'Budget'
                WHEN price BETWEEN 250000 AND 400000 THEN 'Mid-range'
                WHEN price BETWEEN 400001 AND 600000 THEN 'Premium'
                ELSE 'Luxury'
            END as price_segment,
            COUNT(*) as property_count,
            ROUND(AVG(price)::numeric, 2) as avg_price_in_segment
        FROM atlantic_housing_real
        GROUP BY city, price_segment
        ORDER BY city, avg_price_in_segment;
    """))
    
    conn.commit()
    print("All analysis tables created!")

#show what we created
print("\nTables in your database:")
with engine.connect() as conn:
    tables = pd.read_sql("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """, conn)
    
    for table in tables['table_name']:
        count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0,0]
        print(f"  - {table}: {count} rows")

#show sample from city_summary
print("\nCity Summary Preview:")
with engine.connect() as conn:
    summary = pd.read_sql("SELECT * FROM city_summary LIMIT 10", conn)
    print(summary.to_string(index=False))

print("\nAnalysis tables ready for machine learning!")