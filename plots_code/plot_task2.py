import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parse data for ACTION 2
lines = []
with open('action_outputs.txt', 'r') as f:
    reading = False
    for line in f:
        line = line.strip()
        if line == '=== ACTION 2 ===':
            reading = True
            continue
        if line.startswith('=== ACTION 3 ==='):
            break
        if reading and line.startswith('|') and 'DayOfWeek' not in line and '---' not in line:
            lines.append(line)

data = []
for line in lines:
    parts = [p.strip() for p in line.split('|') if p.strip()]
    if len(parts) == 3:
        zone, day, pax = parts
        pax = float(pax.replace(',', ''))
        data.append({'Zone': zone, 'DayOfWeek': day, 'Pax': pax})

df = pd.DataFrame(data)

# Filter for the target zones
target_zones = ['CBD_Downtown', 'Core_Deira', 'Coastal_Marina']
df_filtered = df[df['Zone'].isin(target_zones)].copy()

# Classify Days
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
df_filtered['Type'] = df_filtered['DayOfWeek'].apply(lambda x: 'Weekday (Mon-Fri)' if x in weekdays else 'Weekend (Sat-Sun)')

# Group to get average daily pax per day type
grouped = df_filtered.groupby(['Zone', 'Type'])['Pax'].mean().reset_index()

# Pivot for easier plotting
pivot_df = grouped.pivot(index='Zone', columns='Type', values='Pax').reindex(target_zones)

plt.style.use('default')
fig, ax = plt.subplots(figsize=(12, 7), dpi=200)

x = np.arange(len(target_zones))
width = 0.35

# Color Palettes
weekday_color = '#0077cc' # Neon Cyan
weekend_color = '#cc0055' # Neon Pink

# Create Clustered Bars
bars1 = ax.bar(x - width/2, pivot_df['Weekday (Mon-Fri)'], width, label='Weekday (Mon-Fri)', 
               color=weekday_color, edgecolor='#ffffff', linewidth=1.5)
bars2 = ax.bar(x + width/2, pivot_df['Weekend (Sat-Sun)'], width, label='Weekend (Sat-Sun)', 
               color=weekend_color, edgecolor='#ffffff', linewidth=1.5)

# Add glow effects by plotting slightly wider, highly transparent bars underneath
# (Optional, but adds to the neon vibe)

# Add percentage drop/rise labels above the weekend bars
for i in range(len(target_zones)):
    weekday_val = pivot_df['Weekday (Mon-Fri)'].iloc[i]
    weekend_val = pivot_df['Weekend (Sat-Sun)'].iloc[i]
    
    pct_change = ((weekend_val - weekday_val) / weekday_val) * 100
    
    # Conditional formatting for drop vs rise
    if pct_change < 0:
        icon = '▼'
        color = '#cc3300' # Reddish-orange for drop
    else:
        icon = '▲'
        color = '#22aa22' # Neon green for rise
        
    label_text = f'{icon} {pct_change:+.1f}%'
    
    # Annotate on the chart
    ax.text(x[i] + width/2, weekend_val + (pivot_df.max().max() * 0.02), label_text, 
            ha='center', va='bottom', fontsize=14, fontweight='bold', color=color)

    # Put raw values horizontal at the top of the bars (just below percentage)
    ax.text(x[i] - width/2, weekday_val - (pivot_df.max().max() * 0.03), f'{int(weekday_val):,}', 
            ha='center', va='top', fontsize=11, color='white', fontweight='bold')
    ax.text(x[i] + width/2, weekend_val - (pivot_df.max().max() * 0.03), f'{int(weekend_val):,}', 
            ha='center', va='top', fontsize=11, color='white', fontweight='bold')


# Titles and descriptions
plt.figtext(0.5, 0.96, 'Task 2: Day-Type Volatility (Weekday vs. Weekend)', 
            fontsize=22, fontweight='bold', ha='center', color='#111111', family='sans-serif')
plt.figtext(0.5, 0.91, 'Complete Demand Inversion Between Corporate and Tourism Zones on Weekends', 
            fontsize=15, fontstyle='italic', ha='center', color='#bbbbbb', family='sans-serif')

# Axes configurations
ax.set_xlabel('Corridors / Zones', fontsize=13, fontweight='bold', color='#222222', labelpad=12)
ax.set_ylabel('Average Daily Passengers', fontsize=13, fontweight='bold', color='#222222', labelpad=12)

# Set x-ticks
ax.set_xticks(x)
ax.set_xticklabels([z.replace('_', '\n') for z in target_zones], fontsize=13, fontweight='bold', color='#bbbbbb')

# Format y-axis labels
def thousands_formatter(val, pos):
    return f'{int(val/1000)}K' if val >= 1000 else f'{int(val)}'
ax.yaxis.set_major_formatter(plt.FuncFormatter(thousands_formatter))
ax.tick_params(axis='y', colors='#bbbbbb', labelsize=11)

# Grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.3, color='#cccccc')
ax.set_axisbelow(True)

# Spine cleanup
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color('#999999')
    ax.spines[spine].set_linewidth(1.5)

# Expand y-limit slightly to fit the % labels
ax.set_ylim(0, pivot_df.max().max() * 1.15)

# Legend positioning
legend = ax.legend(fontsize=12, loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=True, 
                   facecolor='#f8f9fa', edgecolor='#bbbbbb', borderpad=1.2, labelcolor='black')
legend.get_frame().set_linewidth(1.5)

plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.35)

# Save chart
output_file = 'Task2_DayType_Divergence.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
