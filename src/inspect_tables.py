#inspect_tables.py - Database Inspector & Inventory Tool
#This is a utility script that shows everything in PostgreSQL database at a glance. 

import pandas as pd
from sqlalchemy import create_engine, inspect
import urllib.parse

password = urllib.parse.quote_plus("atlantic2026!")
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/postgres')

inspector = inspect(engine)

#check vacancy tables
vacancy_tables = ['vacancy_vacancy_rates_cmanovas', 
                  'vacancy_vacancy_rates_cmanewb',
                  'vacancy_vacancy_rates_cmapei',
                  'vacancy_vacancy_rates_cmanewfoundland']

for table in vacancy_tables:
    print(f"\n Columns in {table}:")
    columns = inspector.get_columns(table)
    for col in columns:
        print(f"  - {col['name']}")
    
    #show first row
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", engine)
    print(f"  Sample data: {df.to_dict('records')[0] if len(df) > 0 else 'No data'}")