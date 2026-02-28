import pandas as pd
import matplotlib.pyplot as plt

# Read the file and extract lines for ACTION 4
lines = []
with open('action_outputs.txt', 'r') as f:
    reading = False
    for line in f:
        line = line.strip()
        if line == '=== ACTION 4 ===':
            reading = True
            continue
        # stop reading if we hit another action block or end
        if reading and line.startswith('==='):
            break
        if reading and line.startswith('|') and 'Route_ID' not in line and '---' not in line:
            lines.append(line)

# Parse the lines
routes_df = pd.read_csv('Bus_Routes.csv')
route_type_map = dict(zip(routes_df['Route_ID'].astype(str), routes_df['Route_Type']))

data = []
for line in lines:
    parts = [p.strip() for p in line.split('|') if p.strip()]
    if len(parts) == 2:
        route_id, pax = parts
        rtype = route_type_map.get(route_id, 'Unknown')
        data.append({
            'Route_ID': f"Route {route_id} ({rtype})",
            'Route_Num': route_id,
            'Total_Pax': float(pax.replace(',', ''))
        })

df = pd.DataFrame(data)

# Sort by Total_Pax descending
df = df.sort_values(by='Total_Pax', ascending=True) # Ascending for horizontal bar chart so highest is top

plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 8), dpi=200)

# Colors matching the neon theme
overload_color = '#cc0033' # Neon Red
underutilized_color = '#22aa22' # Neon Green
neutral_color = '#0077cc' # Neon Cyan

colors = []
for index, row in df.iterrows():
    if row['Route_Num'] in ['101', '103']:
        colors.append(overload_color)
    elif row['Route_Num'] in ['109', '110']:
        colors.append(underutilized_color)
    else:
        colors.append(neutral_color)

# Plot horizontal bars
bars = ax.barh(df['Route_ID'], df['Total_Pax'], color=colors, edgecolor='#ffffff', linewidth=1.5, alpha=0.9)

# Add glow effect
ax.barh(df['Route_ID'], df['Total_Pax'], color=colors, edgecolor='none', linewidth=0, alpha=0.15, height=0.9)
ax.barh(df['Route_ID'], df['Total_Pax'], color=colors, edgecolor='none', linewidth=0, alpha=0.05, height=1.1)

# Annotations (values at the end of bars)
for bar, color, (idx, row) in zip(bars, colors, df.iterrows()):
    width = bar.get_width()
    # Adding label inside or outside the bar
    if row['Route_Num'] in ['101', '103']:
        label_text = f"{int(width):,} (Overload Risk)"
    elif row['Route_Num'] in ['109', '110']:
        label_text = f"{int(width):,} (Underutilized)"
    else:
        label_text = f"{int(width):,}"

    ax.text(width + 50, bar.get_y() + bar.get_height()/2, label_text, 
            ha='left', va='center', fontsize=11, fontweight='bold', color=color)

# Titles
plt.figtext(0.5, 0.95, 'Task 4: H2 2025 Baseline Forecast & Structural Imbalance', 
            fontsize=20, fontweight='bold', ha='center', color='#111111', family='sans-serif')
plt.figtext(0.5, 0.90, 'Imminent Overload Risk on City Corridors vs. Idle Capacity on Intercity Routes', 
            fontsize=13, fontstyle='italic', ha='center', color='#bbbbbb', family='sans-serif')

ax.set_xlabel('Average Daily Passengers in 2025', fontsize=13, fontweight='bold', color='#222222', labelpad=12)
ax.set_ylabel('Corridor / Route ID', fontsize=13, fontweight='bold', color='#222222', labelpad=12)

# Format X-axis
def thousands_formatter(val, pos):
    return f'{int(val/1000)}K' if val >= 1000 else f'{int(val)}'
ax.xaxis.set_major_formatter(plt.FuncFormatter(thousands_formatter))
ax.tick_params(axis='x', colors='#bbbbbb', labelsize=11)
ax.tick_params(axis='y', colors='#bbbbbb', labelsize=12)

# Grid styling
ax.grid(True, axis='x', linestyle='--', alpha=0.2, color='#cccccc')
ax.set_axisbelow(True)

# Spine cleanup
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color('#999999')
    ax.spines[spine].set_linewidth(1.5)

# Expand x-limit slightly to fit the labels
ax.set_xlim(0, df['Total_Pax'].max() * 1.35)

plt.tight_layout()
plt.subplots_adjust(top=0.84)

# Save the chart
output_file = 'Task4_Structural_Imbalance.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
