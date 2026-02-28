import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the file and extract lines for ACTION 3
lines = []
with open('action_outputs.txt', 'r') as f:
    reading = False
    for line in f:
        line = line.strip()
        if line == '=== ACTION 3 ===':
            reading = True
            continue
        if line.startswith('=== ACTION 4 ==='):
            break
        if reading and line.startswith('|') and 'Route_Type' not in line and '---' not in line:
            lines.append(line)

# Parse the lines
data = []
for line in lines:
    parts = [p.strip() for p in line.split('|') if p.strip()]
    if len(parts) == 4:
        route_type, cong_level, avg_speed, pax = parts
        data.append({
            'Route_Type': route_type,
            'Congestion_Level': int(cong_level),
            'Average_Speed': float(avg_speed),
            'Total_Pax': float(pax.replace(',', ''))
        })

df = pd.DataFrame(data)

# Filter for the target route types
target_routes = ['City', 'Express', 'Feeder'] # order matters for stacking visually
df_filtered = df[df['Route_Type'].isin(target_routes)]

# Pivot the data for stacked bars
pivot_pax = df_filtered.pivot(index='Congestion_Level', columns='Route_Type', values='Total_Pax')[target_routes]

# Speed data (same for all route types at a given congestion level)
speed_data = df_filtered.groupby('Congestion_Level')['Average_Speed'].first()

plt.style.use('default')
fig, ax1 = plt.subplots(figsize=(12, 7.5), dpi=200)

# Colors matching the neon theme
route_colors = {
    'City': '#0077cc',     # Neon Cyan
    'Express': '#cc0055',  # Neon Pink
    'Feeder': '#22aa22'    # Neon Green
}

# Plot stacked bars on ax1 (Left Y-Axis)
x = pivot_pax.index
bottom = np.zeros(len(x))
width = 0.5

bars = []
for route in target_routes:
    b = ax1.bar(x, pivot_pax[route], width, bottom=bottom, label=route, 
                color=route_colors[route], edgecolor='#ffffff', linewidth=1.5, alpha=0.85)
    bars.append(b)
    bottom += pivot_pax[route]

# Adding "Total" Labels
for i, level in enumerate(x):
    total = bottom.values[i]
    ax1.text(level, total + (total * 0.02), f"~{int(total/1000)}K", 
             ha='center', va='bottom', fontsize=11, fontweight='bold', color='#111111')

ax1.set_xlabel('Congestion Level', fontsize=13, fontweight='bold', color='#222222', labelpad=12)
ax1.set_ylabel('Average Daily Total Pax', fontsize=13, fontweight='bold', color='#222222', labelpad=12)

# Format left Y-axis
def thousands_formatter(val, pos):
    return f'{int(val/1000)}K' if val >= 1000 else f'{int(val)}'
ax1.yaxis.set_major_formatter(plt.FuncFormatter(thousands_formatter))
ax1.tick_params(axis='y', colors='#bbbbbb', labelsize=11)
ax1.tick_params(axis='x', colors='#bbbbbb', labelsize=12)
ax1.set_xticks(x)

# Create ax2 (Right Y-Axis)
ax2 = ax1.twinx()

# Plot line on ax2
line_color = '#cc7700' # Bright Amber/Yellow
ax2.plot(x, speed_data, color=line_color, marker='o', markersize=10, 
         markeredgecolor='#ffffff', markeredgewidth=2, linewidth=3, label='Average Speed (km/h)')

# Glow effect for the line
ax2.plot(x, speed_data, color=line_color, linewidth=8, alpha=0.2)
ax2.plot(x, speed_data, color=line_color, linewidth=12, alpha=0.1)

ax2.set_ylabel('Average Speed (km/h)', fontsize=13, fontweight='bold', color=line_color, labelpad=12)
ax2.tick_params(axis='y', colors=line_color, labelsize=11)
ax2.set_ylim(0, 45) # Give it some ceiling above 40

# Add text callout to Congestion Level 5
callout_x = 5
callout_y = speed_data[5]

# "The Double Penalty: 50% drop in speed + ~20% stretch in Dwell Time due to passenger surge."
ax2.annotate('The Double Penalty:\n50% drop in speed + ~20% stretch in Dwell Time\ndue to passenger surge.', 
             xy=(callout_x, callout_y), xytext=(callout_x - 0.2, callout_y + 10),
             arrowprops=dict(facecolor='black', arrowstyle='->', lw=2, color='#222222'),
             fontsize=11, fontweight='bold', color='#111111',
             ha='right', va='bottom',
             bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#cc3300", lw=2, alpha=0.9))

# Titles
plt.figtext(0.5, 0.96, 'Task 3: Congestion Elasticity & The "Double Penalty" of Dwell Time', 
            fontsize=20, fontweight='bold', ha='center', color='#111111', family='sans-serif')
plt.figtext(0.5, 0.91, 'The "Catastrophic Loop" - Demand Peaks Exactly When System Capacity Halves', 
            fontsize=14, fontstyle='italic', ha='center', color='#bbbbbb', family='sans-serif')

# Create combined legend
# Need to gather handles and labels from both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

legend = ax1.legend(handles1 + handles2, labels1 + labels2, fontsize=11, loc='upper center', 
                   bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=True, 
                   facecolor='#f8f9fa', edgecolor='#bbbbbb', borderpad=1.2, labelcolor='black')
legend.get_frame().set_linewidth(1.5)

# Grid styling
ax1.grid(True, axis='y', linestyle='--', alpha=0.2, color='#cccccc')
ax1.set_axisbelow(True)

# Spine cleanup
for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_color('#999999')
    ax.spines['bottom'].set_linewidth(1.5)

ax1.spines['left'].set_color('#999999')
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['right'].set_visible(False)

ax2.spines['right'].set_color(line_color)
ax2.spines['right'].set_linewidth(1.5)
ax2.spines['left'].set_visible(False)

# Make space for legend and title
plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.22)

# Save the chart
output_file = 'Task3_Congestion_Double_Penalty.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
