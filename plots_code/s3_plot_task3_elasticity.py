import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Data Loading ---

bus_routes = pd.read_csv('DecodeX_Given_Stuff/Bus_Routes.csv')

# H1 Ridership + Traffic
h1_rider = pd.read_csv('DecodeX_Given_Stuff/Train/Train_Ridership_2022_to_2025H1.csv')
h1_rider['Date'] = pd.to_datetime(h1_rider['Date'])
h1_rider['Total_Pax'] = h1_rider['Boarding_Count'] + h1_rider['Alighting_Count']
h1_rider = h1_rider[(h1_rider['Date'] >= '2025-01-01') & (h1_rider['Date'] <= '2025-06-30')]
h1_rider = pd.merge(h1_rider, bus_routes[['Route_ID', 'Route_Type']], on='Route_ID', how='left')

h1_traffic = pd.read_csv('DecodeX_Given_Stuff/Train/Train_Traffic_2022_to_2025H1.csv')
h1_traffic['Date'] = pd.to_datetime(h1_traffic['Date'])
h1_traffic = h1_traffic[(h1_traffic['Date'] >= '2025-01-01') & (h1_traffic['Date'] <= '2025-06-30')]

# Filter City + Express only
h1_ce = h1_rider[h1_rider['Route_Type'].isin(['City', 'Express'])]
h1_daily = h1_ce.groupby('Date')['Total_Pax'].sum().reset_index()
h1_merged = pd.merge(h1_daily, h1_traffic[['Date', 'Congestion_Level']], on='Date', how='left')
h1_elast = h1_merged.groupby('Congestion_Level')['Total_Pax'].mean().reset_index()
h1_elast.rename(columns={'Total_Pax': 'H1_Pax'}, inplace=True)

# Q4 Ridership + Traffic
q4_rider = pd.read_csv('DecodeX_Given_Stuff/OutofTime/OutOfTime_Ridership_2025_Q4.csv')
q4_rider['Total_Pax'] = q4_rider['Boarding_Count'] + q4_rider['Alighting_Count']
q4_rider['Date'] = pd.to_datetime(q4_rider['Date'])

q4_traffic = pd.read_csv('DecodeX_Given_Stuff/OutofTime/OutOfTime_Traffic_2025_Q4.csv')
q4_traffic['Date'] = pd.to_datetime(q4_traffic['Date'])

q4_ce = q4_rider[q4_rider['Route_Type'].isin(['City', 'Express'])]
q4_daily = q4_ce.groupby('Date')['Total_Pax'].sum().reset_index()
q4_merged = pd.merge(q4_daily, q4_traffic[['Date', 'Congestion_Level']], on='Date', how='left')
q4_elast = q4_merged.groupby('Congestion_Level')['Total_Pax'].mean().reset_index()
q4_elast.rename(columns={'Total_Pax': 'Q4_Pax'}, inplace=True)

# Merge
elast = pd.merge(h1_elast, q4_elast, on='Congestion_Level')

# Calculate slope (elasticity) for headline
h1_slope = (elast['H1_Pax'].iloc[-1] - elast['H1_Pax'].iloc[0]) / elast['H1_Pax'].iloc[0] * 100
q4_slope = (elast['Q4_Pax'].iloc[-1] - elast['Q4_Pax'].iloc[0]) / elast['Q4_Pax'].iloc[0] * 100

print(f"H1 elasticity slope (L1→L5): {h1_slope:+.1f}%")
print(f"Q4 elasticity slope (L1→L5): {q4_slope:+.1f}%")
print(f"Elasticity decay: {abs(h1_slope) - abs(q4_slope):.1f} pp reduction\n")

# --- Plotting ---
fig, ax = plt.subplots(figsize=(14, 8), dpi=200)

x = elast['Congestion_Level']

# H1 line (Pre-Metro) — steep slope
ax.plot(x, elast['H1_Pax'], color='#c62828', marker='o', linewidth=3, markersize=12,
        markeredgecolor='white', markeredgewidth=2, label='H1 2025 (Pre-Metro Phase 2)', zorder=5)
# Glow
ax.plot(x, elast['H1_Pax'], color='#c62828', linewidth=8, alpha=0.12)

# Q4 line (Post-Metro) — flat
ax.plot(x, elast['Q4_Pax'], color='#2e7d32', marker='D', linewidth=3, markersize=12,
        markeredgecolor='white', markeredgewidth=2, label='Q4 2025 (Post-Metro Phase 2)', zorder=5)
# Glow
ax.plot(x, elast['Q4_Pax'], color='#2e7d32', linewidth=8, alpha=0.12)

# Value labels
for _, row in elast.iterrows():
    cl = row['Congestion_Level']
    ax.text(cl, row['H1_Pax'] + 300, f"{int(row['H1_Pax']):,}", ha='center', va='bottom',
            fontsize=10, fontweight='bold', color='#c62828')
    ax.text(cl, row['Q4_Pax'] - 300, f"{int(row['Q4_Pax']):,}", ha='center', va='top',
            fontsize=10, fontweight='bold', color='#2e7d32')

# Shade the gap between curves to show substitution magnitude
ax.fill_between(x, elast['H1_Pax'], elast['Q4_Pax'], alpha=0.08, color='#ff9800',
                label='Metro Substitution Gap')

# Annotate the key divergence at Level 5
h1_l5 = elast.loc[elast['Congestion_Level'] == 5, 'H1_Pax'].values[0]
q4_l5 = elast.loc[elast['Congestion_Level'] == 5, 'Q4_Pax'].values[0]
gap_pct = (h1_l5 - q4_l5) / h1_l5 * 100

ax.annotate(f'Level 5 Gap: {int(h1_l5 - q4_l5):,} pax\n({gap_pct:.0f}% absorbed by Metro)',
            xy=(5, (h1_l5 + q4_l5) / 2), xytext=(3.3, (h1_l5 + q4_l5) / 2 + 800),
            fontsize=11, fontweight='bold', color='#e65100',
            arrowprops=dict(arrowstyle='->', color='#e65100', lw=2),
            bbox=dict(boxstyle='round,pad=0.4', fc='#fff3e0', ec='#e65100', lw=1.5))

# Title
fig.text(0.5, 0.97, 'Elasticity & Substitution Diagnosis: Congestion Response Decay',
         ha='center', fontsize=18, fontweight='bold', color='#111111')
fig.text(0.5, 0.935, 'City + Express Combined: Pre-Metro (H1) vs Post-Metro (Q4) Congestion Elasticity',
         ha='center', fontsize=13, color='#666666')

# Axis
ax.set_xlabel('Congestion Level', fontsize=14, fontweight='bold', color='#333333', labelpad=10)
ax.set_ylabel('Average Daily Passenger Volume\n(City + Express)', fontsize=13, 
              fontweight='bold', color='#333333', labelpad=10)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(['1\n(Free Flow)', '2\n(Light)', '3\n(Moderate)', '4\n(Heavy)', '5\n(Gridlock)'],
                    fontsize=11, color='#333333')

def thousands(x, pos):
    return f'{x/1000:g}K'
ax.yaxis.set_major_formatter(plt.FuncFormatter(thousands))
ax.tick_params(axis='y', labelsize=12, colors='#555555')

# Spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Grid
ax.grid(axis='y', linestyle=':', alpha=0.35, color='#cccccc', zorder=0)
ax.set_axisbelow(True)

# Legend
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=11,
          frameon=True, framealpha=0.95, edgecolor='#cccccc')

# Executive headline
fig.text(0.5, 0.01,
         'Verdict: Metro Phase 2 acts as a high-magnitude substitution sponge, absorbing\n'
         'traffic shocks and flattening the Level 5 congestion elasticity curve.',
         ha='center', va='bottom', fontsize=11, color='#333333', style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#e3f2fd', edgecolor='#42a5f5', linewidth=1.5))

plt.subplots_adjust(bottom=0.22, top=0.90, left=0.10, right=0.92)

output_file = 'S3_Task3_Elasticity_Decay.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
