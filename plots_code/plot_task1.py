import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Read the file and extract lines for ACTION 1
lines = []
with open('action_outputs.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line == '=== ACTION 2 ===':
            break
        if line.startswith('|') and 'Year-Month' not in line and '---' not in line:
            lines.append(line)

# Parse the lines
data = []
for line in lines:
    parts = [p.strip() for p in line.split('|') if p.strip()]
    if len(parts) == 3:
        year_month, zone, total_pax = parts
        data.append({
            'Year-Month': year_month,
            'Zone': zone,
            'Total_Pax': int(total_pax)
        })

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Year-Month'], format='%Y-%m')

# Filter for the top 3 zones
target_zones = ['CBD_Downtown', 'Res_AlQusais', 'Coastal_Marina']
df_filtered = df[df['Zone'].isin(target_zones)]

plt.style.use('default')
fig, ax = plt.subplots(figsize=(14, 8), dpi=200)

# Vibrant neon color palette for dark theme
colors = {'CBD_Downtown': '#0077cc',  # Neon Cyan
          'Res_AlQusais': '#cc0055',  # Neon Pink
          'Coastal_Marina': '#22aa22'} # Neon Green
markers = {'CBD_Downtown': 'o', 'Res_AlQusais': 's', 'Coastal_Marina': 'D'}

for zone in target_zones:
    zone_data = df_filtered[df_filtered['Zone'] == zone].sort_values('Date')
    
    # Glowing effect multi-layered plotting
    ax.plot(zone_data['Date'], zone_data['Total_Pax'], color=colors[zone], linewidth=8, alpha=0.1)
    ax.plot(zone_data['Date'], zone_data['Total_Pax'], color=colors[zone], linewidth=4, alpha=0.3)
    
    # Main crisp line
    ax.plot(zone_data['Date'], zone_data['Total_Pax'], label=zone.replace('_', ' '), 
            color=colors[zone], marker=markers[zone], linewidth=2, markersize=8,
            markeredgecolor='#ffffff', markeredgewidth=1)
    
    # Add linear trendline
    x_num = mdates.date2num(zone_data['Date'])
    z = np.polyfit(x_num, zone_data['Total_Pax'], 1)
    p = np.poly1d(z)
    ax.plot(zone_data['Date'], p(x_num), color=colors[zone], linestyle=':', alpha=0.8, linewidth=1.5)

# Highlight Summer Moderation (June, July, August)
years = df_filtered['Date'].dt.year.unique()
for year in years:
    # 06-01 to 08-31
    start_shade = pd.to_datetime(f'{year}-06-01')
    end_shade = pd.to_datetime(f'{year}-08-31')
    
    label = 'Summer Moderation (Jun-Aug)' if year == years[0] else ""
    # Dark red/orange shade for contrast
    ax.axvspan(start_shade, end_shade, color='#cc3300', alpha=0.25, label=label)

# Add Forecast Horizon line
last_date = df_filtered['Date'].max()
ax.axvline(x=last_date, color='#bbbbbb', linestyle='--', linewidth=2, zorder=0)
ax.text(last_date + pd.Timedelta(days=15), ax.get_ylim()[1] * 0.95, 'H2 2025\nForecast\nHorizon', 
        color='#999999', fontsize=12, fontweight='bold', va='top', ha='left')

# Add Hero Metric
hero_text = "Core Growth: +41%\n(Jan '22 vs Jan '25)"
props = dict(boxstyle='round,pad=0.5', facecolor='#ffffff', alpha=0.9, edgecolor='#cc0055', linewidth=2)
ax.text(0.02, 0.96, hero_text, transform=ax.transAxes, fontsize=14, fontweight='bold',
        verticalalignment='top', bbox=props, color='#111111')

ax.set_xlim(df_filtered['Date'].min() - pd.Timedelta(days=15), df_filtered['Date'].max() + pd.Timedelta(days=200))

# Title and subtitle formatting
plt.figtext(0.5, 0.95, 'Long-Term Growth Decomposition Across Corridors', 
            fontsize=22, fontweight='bold', ha='center', color='#111111', family='sans-serif')
plt.figtext(0.5, 0.90, 'Aggressive Secular Growth Masked by Extreme Summer Moderation', 
            fontsize=15, fontstyle='italic', ha='center', color='#bbbbbb', family='sans-serif')

ax.set_xlabel('Timeline (Jan 2022 - Jun 2025)', fontsize=13, fontweight='bold', color='#222222', labelpad=12)
ax.set_ylabel('Total Monthly Passengers', fontsize=13, fontweight='bold', color='#222222', labelpad=12)

# Axis ticks formatting
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.tick_params(axis='x', colors='#bbbbbb', labelsize=11, rotation=45)
ax.tick_params(axis='y', colors='#bbbbbb', labelsize=11)

# Grid styling
ax.grid(True, linestyle='--', alpha=0.3, color='#cccccc')
ax.set_axisbelow(True)

# Spine styling
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color('#999999')
    ax.spines[spine].set_linewidth(1.5)

# Format y-axis to show "K" for thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}K'
ax.yaxis.set_major_formatter(plt.FuncFormatter(thousands_formatter))

# Legend styling
legend = ax.legend(fontsize=12, loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=4, frameon=True, 
                   facecolor='#f8f9fa', edgecolor='#bbbbbb', borderpad=1.2, labelcolor='black')
legend.get_frame().set_linewidth(1.5)

plt.tight_layout()
plt.subplots_adjust(top=0.82, bottom=0.35)

# Save the chart
plt.savefig('Task1_Growth_Decomposition_Modern.png', dpi=300, bbox_inches='tight', facecolor='#ffffff')
print("Chart successfully saved as Task1_Growth_Decomposition_Modern.png")
