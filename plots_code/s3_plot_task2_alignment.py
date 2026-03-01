import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Data Loading ---

bus_routes = pd.read_csv('DecodeX_Given_Stuff/Bus_Routes.csv')

# H1 Ridership
h1 = pd.read_csv('DecodeX_Given_Stuff/Train/Train_Ridership_2022_to_2025H1.csv')
h1['Date'] = pd.to_datetime(h1['Date'])
h1['Total_Pax'] = h1['Boarding_Count'] + h1['Alighting_Count']
h1_2025 = h1[(h1['Date'] >= '2025-01-01') & (h1['Date'] <= '2025-06-30')].copy()
h1_2025 = pd.merge(h1_2025, bus_routes[['Route_ID', 'Route_Type']], on='Route_ID', how='left')
h1_daily = h1_2025.groupby(['Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
h1_summary = h1_daily.groupby('Route_Type')['Total_Pax'].mean().reset_index()
h1_summary.rename(columns={'Total_Pax': 'H1'}, inplace=True)

# Q3 Ridership
q3 = pd.read_csv('DecodeX_Given_Stuff/SHOCK/Shock_Ridership_2025_Q3.csv')
q3['Total_Pax'] = q3['Boarding_Count'] + q3['Alighting_Count']
q3_daily = q3.groupby(['Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
q3_summary = q3_daily.groupby('Route_Type')['Total_Pax'].mean().reset_index()
q3_summary.rename(columns={'Total_Pax': 'Q3'}, inplace=True)

# Q4 Ridership
q4 = pd.read_csv('DecodeX_Given_Stuff/OutofTime/OutOfTime_Ridership_2025_Q4.csv')
q4['Total_Pax'] = q4['Boarding_Count'] + q4['Alighting_Count']
q4_daily = q4.groupby(['Route_Type', 'Date'])['Total_Pax'].sum().reset_index()
q4_summary = q4_daily.groupby('Route_Type')['Total_Pax'].mean().reset_index()
q4_summary.rename(columns={'Total_Pax': 'Q4'}, inplace=True)

# Merge all periods
df = pd.merge(h1_summary, q3_summary, on='Route_Type')
df = pd.merge(df, q4_summary, on='Route_Type')

# --- Plotting: Slopegraph ---
fig, ax = plt.subplots(figsize=(14, 9), dpi=200)

x_points = [0, 1, 2]
x_labels = ['H1 2025\n(Jan–Jun)\nBaseline', 'Q3 2025\n(Jul–Sep)\nShock', 'Q4 2025\n(Oct–Dec)\nEquilibrium']

# Style per Route Type
styles = {
    'Express':   {'color': '#c62828', 'marker': 'D', 'lw': 3.5},
    'Feeder':    {'color': '#2e7d32', 'marker': 's', 'lw': 3.5},
    'City':      {'color': '#1565c0', 'marker': 'o', 'lw': 2, 'alpha': 0.4},
    'Intercity': {'color': '#e65100', 'marker': '^', 'lw': 2, 'alpha': 0.4},
}

for _, row in df.iterrows():
    rt = row['Route_Type']
    s = styles[rt]
    values = [row['H1'], row['Q3'], row['Q4']]
    alpha = s.get('alpha', 1.0)
    
    # Glow effect for primary lines
    if rt in ['Express', 'Feeder']:
        ax.plot(x_points, values, color=s['color'], linewidth=8, alpha=0.12)
        ax.plot(x_points, values, color=s['color'], linewidth=5, alpha=0.25)
    
    # Main line
    ax.plot(x_points, values, color=s['color'], marker=s['marker'], linewidth=s['lw'],
            markersize=12, markeredgecolor='white', markeredgewidth=2, label=rt,
            alpha=alpha, zorder=5 if rt in ['Express', 'Feeder'] else 3)
    
    # Value labels at each point
    for xi, val in zip(x_points, values):
        y_offset = 250 if rt in ['Express', 'City'] else -350
        if rt in ['Express', 'Feeder']:
            ax.text(xi, val + y_offset, f'{int(val):,}', ha='center', va='center',
                    fontsize=11, fontweight='bold', color=s['color'])

# Shock event marker
ax.axvline(x=1, color='#ffab00', linewidth=2, linestyle='--', alpha=0.6, zorder=0)
ax.text(1, ax.get_ylim()[1] * 0.98, 'Metro Phase 2\nShock', ha='center', va='top',
        fontsize=10, fontweight='bold', color='#f57f17', alpha=0.7,
        bbox=dict(boxstyle='round,pad=0.3', fc='#fff8e1', ec='#ffab00', lw=1, alpha=0.8))

# Annotate the key story on the lines
# Express: overshoot then correction
mid_express_q3 = df.loc[df['Route_Type'] == 'Express', 'Q3'].values[0]
mid_express_q4 = df.loc[df['Route_Type'] == 'Express', 'Q4'].values[0]
ax.annotate('Express cools\n(-1.1%)', xy=(2, mid_express_q4), xytext=(2.25, mid_express_q4 + 400),
            fontsize=10, color='#c62828', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#c62828', lw=1.5))

# Feeder: undershoot then rebound
mid_feeder_q3 = df.loc[df['Route_Type'] == 'Feeder', 'Q3'].values[0]
mid_feeder_q4 = df.loc[df['Route_Type'] == 'Feeder', 'Q4'].values[0]
ax.annotate('Feeder rebounds\n(+9.2%)', xy=(2, mid_feeder_q4), xytext=(2.25, mid_feeder_q4 - 500),
            fontsize=10, color='#2e7d32', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.5))

# Title
fig.text(0.5, 0.97, 'Strategic Alignment Evaluation: Network Trajectory Through the Shock',
         ha='center', fontsize=18, fontweight='bold', color='#111111')
fig.text(0.5, 0.935, 'H1 Baseline → Q3 Shock → Q4 Redistributed Equilibrium',
         ha='center', fontsize=13, color='#666666')

# Axis
ax.set_xticks(x_points)
ax.set_xticklabels(x_labels, fontsize=13, fontweight='bold', color='#333333')
ax.set_ylabel('Average Daily Passenger Volume', fontsize=13, fontweight='bold', 
              color='#333333', labelpad=10)

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
ax.set_xlim(-0.3, 2.7)

# Legend
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=4, fontsize=12,
          frameon=True, framealpha=0.95, edgecolor='#cccccc')

# Executive headline
fig.text(0.5, 0.01,
         'Verdict: Q4 stabilization proves Stage 2 Feeder fleet cannibalization was excessive;\n'
         'the network found a redistributed equilibrium, not permanent shock intensity.',
         ha='center', va='bottom', fontsize=11, color='#333333', style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#e8f5e9', edgecolor='#66bb6a', linewidth=1.5))

plt.subplots_adjust(bottom=0.20, top=0.90, left=0.10, right=0.88)

output_file = 'S3_Task2_Strategic_Alignment.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
