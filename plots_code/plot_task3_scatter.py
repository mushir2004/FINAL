import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import collections

# --- Data Loading and Prep ---

# 1. Load Route Information (for Average_Travel_Time and Route_Type)
bus_routes = pd.read_csv('DecodeX_Given_Stuff/Bus_Routes.csv')

# 2. Load Q3 Ridership Actuals
q3_ridership = pd.read_csv('DecodeX_Given_Stuff/SHOCK/Shock_Ridership_2025_Q3.csv')
q3_ridership['Total_Pax'] = q3_ridership['Boarding_Count'] + q3_ridership['Alighting_Count']

# Aggregate to find Q3 average daily pax per route
q3_daily = q3_ridership.groupby(['Route_ID', 'Date'])['Total_Pax'].sum().reset_index()
q3_route_summary = q3_daily.groupby('Route_ID')['Total_Pax'].mean().reset_index()
q3_route_summary.rename(columns={'Total_Pax': 'Q3_Avg_Daily_Pax'}, inplace=True)

# 3. Load H1/Stage 1 Forecasts from action_outputs.txt (Action 4)
lines = []
with open('action_outputs.txt', 'r') as f:
    reading = False
    for line in f:
        line = line.strip()
        if line == '=== ACTION 4 ===':
            reading = True
            continue
        if reading and line.startswith('|') and 'Route_ID' not in line and '---' not in line:
            lines.append(line)

h1_data = []
for line in lines:
    parts = [p.strip() for p in line.split('|') if p.strip()]
    if len(parts) == 2:
        route_id, pax = parts
        h1_data.append({
            'Route_ID': int(route_id),
            'H1_Avg_Daily_Pax': float(pax.replace(',', ''))
        })
h1_df = pd.DataFrame(h1_data)

# Merge everything together
network_df = pd.merge(bus_routes, q3_route_summary, on='Route_ID', how='left')
network_df = pd.merge(network_df, h1_df, on='Route_ID', how='left')

# --- Plotting ---
plt.style.use('default')
fig, ax = plt.subplots(figsize=(12, 8), dpi=200)

# Define Quadrant Thresholds (based on visual distribution)
# Let's say: 
# High Pax > 2750
# Slow Travel Time > 45 mins
pax_threshold = 2750
time_threshold = 45

# Colors by Route Type for Q3 actuals
type_colors = {
    'City': '#0077cc',     # Cyan
    'Express': '#cc0055',  # Pink
    'Feeder': '#22aa22',   # Green
    'Intercity': '#cc7700' # Amber
}

# Plot the matrix quadrants
ax.axhline(y=pax_threshold, color='#555555', linestyle='--', linewidth=1.5, zorder=0)
ax.axvline(x=time_threshold, color='#555555', linestyle='--', linewidth=1.5, zorder=0)

# Quadrant labels
quadrant_font = {'fontsize': 12, 'fontweight': 'bold', 'color': '#dddddd', 'alpha': 0.10}
# Top-Right (Danger)
ax.text(time_threshold + 1, network_df['Q3_Avg_Daily_Pax'].max() - 100, 
        'SYSTEM\nOVERLOAD\n(High Volume + Slow Speed)', 
        ha='left', va='top', **quadrant_font)
# Top-Left (High Efficiency)
ax.text(time_threshold - 1, network_df['Q3_Avg_Daily_Pax'].max() - 100, 
        'HIGH EFFICIENCY\n(High Volume + Fast Speed)', 
        ha='right', va='top', **quadrant_font)
# Bottom-Left (Underutilized)
ax.text(time_threshold - 1, network_df['Q3_Avg_Daily_Pax'].min() + 100, 
        'STRANDED CAPITAL\n(Underutilized)', 
        ha='right', va='bottom', **quadrant_font)

# Plot Points and Movement Vectors (H1 to Q3)
for idx, row in network_df.iterrows():
    rt_type = row['Route_Type']
    color = type_colors.get(rt_type, '#999999')
    
    # Q3 Actual Position (Bigger, brighter)
    ax.scatter(row['Avg_Travel_Time_Min'], row['Q3_Avg_Daily_Pax'], 
               color=color, s=250, edgecolor='#ffffff', linewidth=1.5, zorder=4, label=rt_type)
    
    # H1 Target Position (Smaller, faded)
    ax.scatter(row['Avg_Travel_Time_Min'], row['H1_Avg_Daily_Pax'], 
               color=color, alpha=0.3, s=100, edgecolor='none', zorder=2)
    
    # Arrow showing movement
    ax.annotate('', xy=(row['Avg_Travel_Time_Min'], row['Q3_Avg_Daily_Pax']), 
                xytext=(row['Avg_Travel_Time_Min'], row['H1_Avg_Daily_Pax']),
                arrowprops=dict(arrowstyle="->", color=color, alpha=0.5, lw=1.5), zorder=3)
    
    # Labels
    # Use adaptive offsets to avoid overlap based on volume
    x_offset = 0.3
    
    if row['Route_ID'] == 104:
        y_offset = 50
        # Highlight Express overload
        ax.text(row['Avg_Travel_Time_Min'] + x_offset, row['Q3_Avg_Daily_Pax'] + y_offset, 
                f"Rt {row['Route_ID']}\n(+28%)", fontsize=11, fontweight='bold', color=color, zorder=5)
    elif row['Route_ID'] == 105:
        y_offset = -80
        # Highlight Express overload (push label down below origin point)
        ax.text(row['Avg_Travel_Time_Min'] + x_offset, row['Q3_Avg_Daily_Pax'] + y_offset, 
                f"Rt {row['Route_ID']}\n(+28%)", fontsize=11, fontweight='bold', color=color, zorder=5)
    elif row['Route_ID'] in [106, 107]:
        # Highlight Feeder collapse, push labels further down
        y_offset = -120
        ax.text(row['Avg_Travel_Time_Min'] + x_offset, row['Q3_Avg_Daily_Pax'] + y_offset, 
                f"Rt {row['Route_ID']}\n(-25%)", fontsize=11, fontweight='bold', color=color, zorder=5)
    else:
        # Standard label
        y_offset = 30 if row['Q3_Avg_Daily_Pax'] < 2500 else -60
        ax.text(row['Avg_Travel_Time_Min'] + x_offset, row['Q3_Avg_Daily_Pax'] + y_offset, 
                f"Rt {row['Route_ID']}", fontsize=10, color='#666666', zorder=5)

# Deduplicate legend
handles, labels = ax.get_legend_handles_labels()
by_label = collections.OrderedDict(zip(labels, handles))
# Create legend manually for style
legend = ax.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=11, 
                   framealpha=0.9, edgecolor='#cccccc', title="Route Type", title_fontsize=12)
legend.get_title().set_fontweight('bold')

# Titles
ax.set_title('Task 3: Operational Risk Reassessment Matrix (H1 Target → Q3 Actual)', 
             fontsize=18, fontweight='bold', pad=20, color='#111111')
plt.figtext(0.5, 0.90, 'Express Routes Pushed to Breaking Point; Feeders Sink into Underutilization', 
            fontsize=13, fontstyle='italic', ha='center', color='#555555')

ax.set_xlabel('Average Scheduled Travel Time (Minutes)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Average Daily Passenger Volume', fontsize=12, fontweight='bold', labelpad=10)

def thousands(x, pos):
    return f'{x/1000:g}K'
ax.yaxis.set_major_formatter(plt.FuncFormatter(thousands))

# Style touches
ax.set_facecolor('#fafafa')
ax.grid(True, linestyle=':', alpha=0.6, color='#cccccc', zorder=1)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#999999')
ax.spines['bottom'].set_color('#999999')

plt.tight_layout()

# Save the chart
output_file = 'Task3_Risk_Matrix.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
