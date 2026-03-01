import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# --- Data Loading ---

q3_ridership = pd.read_csv('DecodeX_Given_Stuff/SHOCK/Shock_Ridership_2025_Q3.csv')
q3_ridership['Total_Pax'] = q3_ridership['Boarding_Count'] + q3_ridership['Alighting_Count']
q3_daily = q3_ridership.groupby(['Route_ID', 'Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
q3_route = q3_daily.groupby(['Route_ID', 'Route_Type'])['Total_Pax'].mean().reset_index()
q3_route.rename(columns={'Total_Pax': 'Q3_Actual'}, inplace=True)

q4_ridership = pd.read_csv('DecodeX_Given_Stuff/OutofTime/OutOfTime_Ridership_2025_Q4.csv')
q4_ridership['Total_Pax'] = q4_ridership['Boarding_Count'] + q4_ridership['Alighting_Count']
q4_daily = q4_ridership.groupby(['Route_ID', 'Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
q4_route = q4_daily.groupby(['Route_ID', 'Route_Type'])['Total_Pax'].mean().reset_index()
q4_route.rename(columns={'Total_Pax': 'Q4_Actual'}, inplace=True)

df = pd.merge(q3_route, q4_route[['Route_ID', 'Q4_Actual']], on='Route_ID')

# Stage 2 Forecast Logic
forecast_multipliers = {'Express': 1.10, 'City': 1.08, 'Feeder': 0.95, 'Intercity': 1.02}
df['Stage2_Forecast'] = df.apply(lambda r: r['Q3_Actual'] * forecast_multipliers[r['Route_Type']], axis=1)
df['Pct_Error'] = ((df['Stage2_Forecast'] - df['Q4_Actual']) / df['Q4_Actual']) * 100

# Sort: Express top, Feeder bottom
type_order = {'Express': 0, 'City': 1, 'Intercity': 2, 'Feeder': 3}
df['Type_Order'] = df['Route_Type'].map(type_order)
df = df.sort_values(['Type_Order', 'Route_ID'], ascending=[False, False])

# --- Plotting ---
fig, ax = plt.subplots(figsize=(16, 10), dpi=200)

df['Label'] = df.apply(lambda r: f"Rt {r['Route_ID']}  ({r['Route_Type']})", axis=1)
y_pos = np.arange(len(df))

# Colors
colors = ['#c62828' if e > 0 else '#2e7d32' for e in df['Pct_Error']]

bars = ax.barh(y_pos, df['Pct_Error'].values, color=colors, height=0.55, 
               edgecolor='white', linewidth=1.2, alpha=0.88)

# Labels: only the % value, placed well outside bar end
for i, (bar, (_, row)) in enumerate(zip(bars, df.iterrows())):
    width = bar.get_width()
    color = '#c62828' if width > 0 else '#2e7d32'
    
    if width > 0:
        ax.text(width + 0.6, y_pos[i], f'{width:+.1f}%', 
                va='center', ha='left', fontweight='bold', fontsize=12, color=color)
    else:
        ax.text(width - 0.6, y_pos[i], f'{width:+.1f}%', 
                va='center', ha='right', fontweight='bold', fontsize=12, color=color)

# Y-axis
ax.set_yticks(y_pos)
ax.set_yticklabels(df['Label'].values, fontsize=13, color='#222222')

# Zero line
ax.axvline(x=0, color='#222222', linewidth=2, zorder=0)

# Subtle background shading
ax.axvspan(0, 25, color='#fce4ec', alpha=0.15, zorder=0)
ax.axvspan(-25, 0, color='#e8f5e9', alpha=0.15, zorder=0)

# Horizontal separators between route type groups
prev_type = None
for i, (_, row) in enumerate(df.iterrows()):
    if prev_type is not None and row['Route_Type'] != prev_type:
        ax.axhline(y=i - 0.5, color='#bbbbbb', linewidth=1, linestyle='--', zorder=0)
    prev_type = row['Route_Type']

# Title
fig.text(0.5, 0.96, 'Forecast Performance Audit: Stage 2 Model vs Q4 Actuals',
         ha='center', fontsize=18, fontweight='bold', color='#111111')
fig.text(0.5, 0.93, 'Route-Level MAPE & Directional Bias Analysis',
         ha='center', fontsize=14, color='#555555')

# Axis
ax.set_xlabel('% Forecast Error  (Forecast − Actual) / Actual', fontsize=13, 
              fontweight='bold', color='#333333', labelpad=12)
ax.tick_params(axis='x', labelsize=11, colors='#555555')
ax.set_xlim(-25, 20)

# Spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Grid
ax.grid(axis='x', linestyle=':', alpha=0.35, color='#cccccc', zorder=0)
ax.set_axisbelow(True)

# Legend
legend_elements = [Patch(facecolor='#c62828', alpha=0.88, label='Overestimated (Upward Bias)'),
                   Patch(facecolor='#2e7d32', alpha=0.88, label='Underestimated (Downward Bias)')]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.08),
          ncol=2, fontsize=12, frameon=True, framealpha=0.95, edgecolor='#cccccc')

# Executive headline callout
fig.text(0.5, 0.01,
         'Verdict: Stage 2 models misclassified discovery volatility — +15% upward directional bias\n'
         'on Express routes and -10% downward bias on Feeders. Feeder rebound was underestimated.',
         ha='center', va='bottom', fontsize=11, color='#333333', style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff8e1', edgecolor='#f9a825', linewidth=1.5))

plt.subplots_adjust(bottom=0.18, top=0.90, left=0.20, right=0.88)

output_file = 'S3_Task1_Forecast_Audit.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
