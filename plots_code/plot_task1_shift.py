import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Data Loading and Prep ---

# Load Q3 Ridership
q3_ridership = pd.read_csv('DecodeX_Given_Stuff/SHOCK/Shock_Ridership_2025_Q3.csv')
q3_ridership['Date'] = pd.to_datetime(q3_ridership['Date'])
q3_ridership['Total_Pax'] = q3_ridership['Boarding_Count'] + q3_ridership['Alighting_Count']

# Load H1 Ridership
h1_ridership = pd.read_csv('DecodeX_Given_Stuff/Train/Train_Ridership_2022_to_2025H1.csv')
h1_ridership['Date'] = pd.to_datetime(h1_ridership['Date'])
h1_ridership['Total_Pax'] = h1_ridership['Boarding_Count'] + h1_ridership['Alighting_Count']

# Filter H1 to only include 2025 H1
h1_2025 = h1_ridership[(h1_ridership['Date'] >= '2025-01-01') & (h1_ridership['Date'] <= '2025-06-30')].copy()

# Load Route Types
bus_routes = pd.read_csv('DecodeX_Given_Stuff/Bus_Routes.csv')
h1_2025_with_type = pd.merge(h1_2025, bus_routes[['Route_ID', 'Route_Type']], on='Route_ID', how='left')

# Calculate Q3 Average Daily Total_Pax by Route_Type
q3_daily = q3_ridership.groupby(['Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
q3_summary = q3_daily.groupby('Route_Type')['Total_Pax'].mean().reset_index().rename(columns={'Total_Pax': 'Q3_Avg_Daily_Pax'})

# Calculate H1 Average Daily Total_Pax by Route_Type
h1_daily = h1_2025_with_type.groupby(['Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
h1_summary = h1_daily.groupby('Route_Type')['Total_Pax'].mean().reset_index().rename(columns={'Total_Pax': 'H1_Avg_Daily_Pax'})

# Merge and calculate % change
merged = pd.merge(h1_summary, q3_summary, on='Route_Type')
merged['Percent_Change'] = ((merged['Q3_Avg_Daily_Pax'] - merged['H1_Avg_Daily_Pax']) / merged['H1_Avg_Daily_Pax']) * 100

# Order by absolute shift magnitude (biggest shift first)
merged = merged.sort_values(by='Percent_Change', ascending=False)

# --- Plotting: Grouped Horizontal Bar Chart ---
plt.style.use('default')
fig, ax = plt.subplots(figsize=(14, 8), dpi=200)

route_types = merged['Route_Type'].tolist()
y_pos = np.arange(len(route_types))
bar_height = 0.35

# H1 bars (BEFORE) — neutral gray
bars_before = ax.barh(y_pos + bar_height/2, merged['H1_Avg_Daily_Pax'], 
                       height=bar_height, color='#b0bec5', edgecolor='white', 
                       linewidth=1, label='BEFORE: H1 2025 (Jan–Jun)', alpha=0.85)

# Q3 bars (AFTER) — colored by direction of change
after_colors = []
for pc in merged['Percent_Change']:
    if pc > 5:
        after_colors.append('#2e7d32')   # Strong green for big gains
    elif pc > 0:
        after_colors.append('#66bb6a')   # Light green for small gains
    elif pc > -10:
        after_colors.append('#ef5350')   # Light red for small losses
    else:
        after_colors.append('#c62828')   # Strong red for big losses

bars_after = ax.barh(y_pos - bar_height/2, merged['Q3_Avg_Daily_Pax'], 
                      height=bar_height, color=after_colors, edgecolor='white', 
                      linewidth=1, label='AFTER: Q3 2025 (Jul–Sep)', alpha=0.90)

# Add % change annotations — placed far right with enough gap
for i, (_, row) in enumerate(merged.iterrows()):
    pct = row['Percent_Change']
    max_val = max(row['H1_Avg_Daily_Pax'], row['Q3_Avg_Daily_Pax'])
    
    color = '#2e7d32' if pct > 0 else '#c62828'
    arrow = '▲' if pct > 0 else '▼'
    
    ax.text(max_val + 350, y_pos[i], f'{arrow} {pct:+.1f}%', 
            va='center', ha='left', fontweight='bold', fontsize=14, color=color)

# Add value labels just outside the end of each bar
for bars, label_color in [(bars_before, '#555555'), (bars_after, '#333333')]:
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 80, bar.get_y() + bar.get_height()/2, 
                f'{int(width):,}', va='center', ha='left', 
                fontsize=10, color=label_color, fontweight='bold')

# Y-axis labels
ax.set_yticks(y_pos)
ax.set_yticklabels(route_types, fontsize=15, fontweight='bold', color='#222222')

# Title (single block, no separate subtitle to avoid overlap)
ax.set_title('Metro Phase 2 Structural Break: Before vs After Volume Comparison\n'
             'Shock Event: Metro Phase 2 Launch — July 1, 2025', 
             fontsize=17, fontweight='bold', pad=18, color='#111111',
             linespacing=1.6)

# X-axis
ax.set_xlabel('Average Daily Passenger Volume', fontsize=13, fontweight='bold', 
              color='#333333', labelpad=12)

# Format x-axis
def thousands(x, pos):
    return f'{x/1000:g}K'
ax.xaxis.set_major_formatter(plt.FuncFormatter(thousands))
ax.tick_params(axis='x', labelsize=12, colors='#555555')

# Legend — placed below the chart to avoid overlap
legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, 
                   fontsize=12, frameon=True, framealpha=0.95, edgecolor='#cccccc',
                   handlelength=2.5, handleheight=1.5)
legend.get_frame().set_linewidth(1.5)

# Spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Grid
ax.grid(axis='x', linestyle=':', alpha=0.35, color='#cccccc', zorder=0)
ax.set_axisbelow(True)

# Expand x-limit to fit % labels and value labels
ax.set_xlim(0, merged[['H1_Avg_Daily_Pax', 'Q3_Avg_Daily_Pax']].max().max() * 1.35)

plt.subplots_adjust(bottom=0.20, top=0.88)

# Save the chart
plt.savefig('Task1_Shift_Classification_BarChart.png', dpi=300, bbox_inches='tight', facecolor='#ffffff')
print("Chart successfully saved as Task1_Shift_Classification_BarChart.png")
