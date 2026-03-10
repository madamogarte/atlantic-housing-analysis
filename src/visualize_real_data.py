#visualize_real_data.py - Creates Professional Visualizations
#This script takes real housing data and creates publication quality graphs that show trends, patterns, and insights across Atlantic Canada. 
#Purpose : Creates beautiful, multi-panel visualizations from PostgreSQL data

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import urllib.parse
import matplotlib
matplotlib.use('TkAgg')  # Forces a different backend

#password
password = urllib.parse.quote_plus("atlantic2026!")
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/postgres')

print("-"*60)
print("CREATING VISUALIZATIONS WITH REAL DATA")
print("-"*60)

#load data from PostgreSQL
df = pd.read_sql("SELECT * FROM atlantic_housing_real ORDER BY date", engine)
print(f"Loaded {len(df)} rows from database")

#convert date to datetime
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.quarter

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 1. Housing Starts Over Time (Line Plot)
ax1 = plt.subplot(2, 2, 1)
for province in df['city'].unique():
    prov_data = df[df['city'] == province].sort_values('date')
    ax1.plot(prov_data['date'], prov_data['housing_starts'], 
             marker='o', markersize=4, linewidth=2, label=province)
ax1.set_title('Housing Starts in Atlantic Canada (2015-2022)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Housing Starts')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Total Housing Starts by Province (Bar Chart)
ax2 = plt.subplot(2, 2, 2)
total_starts = df.groupby('city')['housing_starts'].sum().sort_values()
colors = ['#ff7f0e' if x == 'Nova Scotia' else '#1f77b4' for x in total_starts.index]
bars = ax2.barh(range(len(total_starts)), total_starts.values, color=colors)
ax2.set_yticks(range(len(total_starts)))
ax2.set_yticklabels(total_starts.index)
ax2.set_title('Total Housing Starts (2015-2022)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number of Housing Starts')

#add value labels
for i, (bar, val) in enumerate(zip(bars, total_starts.values)):
    ax2.text(val + 500, bar.get_y() + bar.get_height()/2, f'{val:,.0f}', va='center')

# 3. Year-over-Year Growth (Heatmap)
ax3 = plt.subplot(2, 2, 3)
# Pivot data for heatmap
pivot_data = df.pivot_table(
    values='housing_starts',
    index='city',
    columns='year',
    aggfunc='sum'
)
sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax3, cbar_kws={'label': 'Housing Starts'})
ax3.set_title('Housing Starts by Year and Province', fontsize=14, fontweight='bold')

# 4. Quarterly Patterns
ax4 = plt.subplot(2, 2, 4)
quarterly = df.groupby(['city', 'quarter'])['housing_starts'].mean().reset_index()
for province in df['city'].unique():
    prov_data = quarterly[quarterly['city'] == province]
    ax4.plot(prov_data['quarter'], prov_data['housing_starts'], 
             marker='s', linewidth=2, label=province)
ax4.set_title('Average Housing Starts by Quarter', fontsize=14, fontweight='bold')
ax4.set_xlabel('Quarter')
ax4.set_ylabel('Average Housing Starts')
ax4.set_xticks([1, 2, 3, 4])
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/real_housing_visualizations.png', dpi=300, bbox_inches='tight')
print("\n Saved: outputs/real_housing_visualizations.png")

# Create a separate trend comparison
plt.figure(figsize=(14, 8))

# Calculate 4-quarter moving average
for province in df['city'].unique():
    prov_data = df[df['city'] == province].sort_values('date').copy()
    prov_data['ma_4q'] = prov_data['housing_starts'].rolling(4).mean()
    plt.plot(prov_data['date'], prov_data['ma_4q'], linewidth=3, label=f"{province} (4Q MA)")

plt.title('Housing Starts Trend (4-Quarter Moving Average)', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Housing Starts (4Q Moving Average)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('outputs/real_housing_trends.png', dpi=300, bbox_inches='tight')
print(" Saved: outputs/real_housing_trends.png")

print("\n Key Insights:")
print("-" * 40)
for province in df['city'].unique():
    prov_data = df[df['city'] == province].sort_values('date')
    start = prov_data['housing_starts'].iloc[0]
    end = prov_data['housing_starts'].iloc[-1]
    growth = ((end - start) / start) * 100
    total = prov_data['housing_starts'].sum()
    print(f"\n{province}:")
    print(f"  • Total starts (2015-2022): {total:,.0f}")
    print(f"  • Growth: {growth:.1f}%")
    print(f"  • 2015: {start:.0f} → 2022: {end:.0f}")

# Force the plots to show
plt.show()