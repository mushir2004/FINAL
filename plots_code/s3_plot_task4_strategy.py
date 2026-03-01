import matplotlib.pyplot as plt
import numpy as np

# --- Data: Fleet Allocation (% of total capacity) ---

categories = ['Q4 2025\nCurrent Allocation', '2026\nStabilized Design']

# Current Q4 allocation (based on Q4 ridership proportions)
# City: ~41%, Express: ~28%, Feeder: ~19%, Intercity: ~12%
current = {'City': 41, 'Express': 28, 'Feeder': 19, 'Intercity': 12}

# 2026 Proposed: Rationalize overlapping CBD City & Intercity to unlock 10% buffer
proposed = {'City': 35, 'Express': 30, 'Feeder': 13, 'Intercity': 12, 'Volatility Buffer': 10}

# Stack order (bottom to top)
stack_order = ['City', 'Express', 'Feeder', 'Intercity', 'Volatility Buffer']
colors = {
    'City': '#1565c0',
    'Express': '#c62828',
    'Feeder': '#2e7d32',
    'Intercity': '#e65100',
    'Volatility Buffer': '#f9a825'
}

# Build arrays
current_vals = [current.get(s, 0) for s in stack_order]
proposed_vals = [proposed.get(s, 0) for s in stack_order]

# --- Plotting ---
fig, ax = plt.subplots(figsize=(12, 9), dpi=200)

x = np.array([0, 1.2])
bar_width = 0.55

# Draw stacked bars
for data_vals, x_pos in [(current_vals, x[0]), (proposed_vals, x[1])]:
    bottom = 0
    for i, (segment, val) in enumerate(zip(stack_order, data_vals)):
        if val == 0:
            bottom += val
            continue
        
        bar = ax.bar(x_pos, val, bottom=bottom, width=bar_width, 
                     color=colors[segment], edgecolor='white', linewidth=2, alpha=0.90)
        
        # Label inside the block
        if val >= 8:
            label_y = bottom + val / 2
            ax.text(x_pos, label_y, f'{segment}\n{val}%', ha='center', va='center',
                    fontsize=12, fontweight='bold', color='white')
        elif val >= 5:
            label_y = bottom + val / 2
            ax.text(x_pos, label_y, f'{val}%', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white')
        
        bottom += val

# Special highlight for the Volatility Buffer block
# Add a glow/border effect
buf_bottom = sum(proposed_vals[:4])
buf_val = proposed_vals[4]
ax.bar(x[1], buf_val, bottom=buf_bottom, width=bar_width, 
       color='none', edgecolor='#f57f17', linewidth=3, linestyle='--', zorder=6)

# Arrow pointing to the buffer with callout
ax.annotate('NEW: Volatility Buffer\nfor Metro outages &\nfuture shocks',
            xy=(x[1] + bar_width/2, buf_bottom + buf_val/2),
            xytext=(x[1] + 0.55, buf_bottom + buf_val/2 + 5),
            fontsize=11, fontweight='bold', color='#f57f17',
            arrowprops=dict(arrowstyle='->', color='#f57f17', lw=2),
            bbox=dict(boxstyle='round,pad=0.4', fc='#fff8e1', ec='#f9a825', lw=1.5))

# Show what was rationalized with arrows between bars
# City shrank
ax.annotate('', xy=(x[1] - bar_width/2 - 0.02, 15), xytext=(x[0] + bar_width/2 + 0.02, 18),
            arrowprops=dict(arrowstyle='->', color='#1565c0', lw=1.5, alpha=0.5))
ax.text(0.6, 12, 'City -6%', ha='center', fontsize=9, color='#1565c0', alpha=0.6)

# Feeder shrank
ax.annotate('', xy=(x[1] - bar_width/2 - 0.02, 68), xytext=(x[0] + bar_width/2 + 0.02, 75),
            arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.5, alpha=0.5))
ax.text(0.6, 76, 'Feeder -6%', ha='center', fontsize=9, color='#2e7d32', alpha=0.6)

# Title
fig.text(0.5, 0.97, '2026 Forward Strategy: Fleet Capacity Reallocation',
         ha='center', fontsize=18, fontweight='bold', color='#111111')
fig.text(0.5, 0.935, 'Rationalizing overlapping corridors to establish a dedicated Volatility Buffer',
         ha='center', fontsize=13, color='#666666')

# Axis
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=14, fontweight='bold', color='#222222')
ax.set_ylabel('Fleet Capacity Allocation (%)', fontsize=13, fontweight='bold', 
              color='#333333', labelpad=10)
ax.set_ylim(0, 115)
ax.tick_params(axis='y', labelsize=12, colors='#555555')

# Spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Grid
ax.grid(axis='y', linestyle=':', alpha=0.3, color='#cccccc', zorder=0)
ax.set_axisbelow(True)
ax.set_xlim(-0.5, 2.2)

# Legend below
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[s], label=s) for s in stack_order]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.10),
          ncol=5, fontsize=11, frameon=True, framealpha=0.95, edgecolor='#cccccc')

# Executive headline
fig.text(0.5, 0.01,
         'Strategy: Rationalizing overlapping CBD corridors unlocks a quantified 10% efficiency\n'
         'gain, establishing a dedicated Volatility Buffer for future Metro infrastructure outages.',
         ha='center', va='bottom', fontsize=11, color='#333333', style='italic',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff8e1', edgecolor='#f9a825', linewidth=1.5))

plt.subplots_adjust(bottom=0.18, top=0.90, left=0.10, right=0.90)

output_file = 'S3_Task4_2026_Strategy.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
