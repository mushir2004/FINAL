import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- Data: Current vs Proposed Fleet Allocation ---
# Current allocation (H1 baseline, simplified as % of total fleet)
current_labels = ['City\n(Rt 101-103)', 'Express\n(Rt 104-105, 112)', 'Feeder\n(Rt 106-108)', 'Intercity\n(Rt 109-110)', 'Express Buffer\n(Rt 111)']
current_values = [30, 20, 25, 15, 10]
current_colors = ['#0077cc', '#cc0055', '#22aa22', '#cc7700', '#cc0055']

# Proposed allocation (Post-Reallocation)
proposed_labels = ['City\n(Rt 101-103)', 'Express\n(Rt 104-105, 112)', 'Feeder\n(Rt 106-108)', 'Intercity\n(Rt 109-110)', 'Express Buffer\n(Rt 111)']
proposed_values = [30, 35, 10, 10, 15]
proposed_colors = ['#0077cc', '#cc0055', '#22aa22', '#cc7700', '#cc0055']

# --- Plotting ---
fig, axes = plt.subplots(1, 2, figsize=(18, 9), dpi=200)

# Helper to draw donut
def draw_donut(ax, values, labels, colors, title, highlight_idx=None):
    wedges, texts, autotexts = ax.pie(
        values, labels=None, autopct='%1.0f%%', startangle=90,
        colors=colors, pctdistance=0.78,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2.5),
        textprops={'fontsize': 13, 'fontweight': 'bold', 'color': '#333333'}
    )
    
    # Highlight specific wedges with thicker edge
    if highlight_idx:
        for i in highlight_idx:
            wedges[i].set_edgecolor('#ff3333')
            wedges[i].set_linewidth(3.5)
    
    # Add labels outside with lines
    for i, (wedge, label) in enumerate(zip(wedges, labels)):
        ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        
        horizontalalignment = 'left' if x >= 0 else 'right'
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        
        ax.annotate(label, xy=(x * 0.78, y * 0.78), xytext=(x * 1.35, y * 1.25),
                    horizontalalignment=horizontalalignment, fontsize=10, color='#333333',
                    arrowprops=dict(arrowstyle='-', color='#999999', lw=1),
                    bbox=dict(boxstyle='round,pad=0.3', fc='#f8f9fa', ec='#dddddd', lw=1))
    
    ax.set_title(title, fontsize=16, fontweight='bold', color='#111111', pad=20)
    
    return wedges

# Left Donut: Current Allocation
draw_donut(axes[0], current_values, current_labels, current_colors, 
           'Current Fleet Allocation\n(H1 2025 Baseline)', highlight_idx=[2, 3])

# Center text for left donut
axes[0].text(0, 0, 'BEFORE\nReallocation', ha='center', va='center', 
             fontsize=13, fontweight='bold', color='#555555')

# Right Donut: Proposed Allocation
draw_donut(axes[1], proposed_values, proposed_labels, proposed_colors,
           'Proposed Fleet Allocation\n(Q4 2025 Recalibrated)', highlight_idx=[1, 4])

# Center text for right donut
axes[1].text(0, 0, 'AFTER\nReallocation', ha='center', va='center', 
             fontsize=13, fontweight='bold', color='#555555')

# --- Draw the massive flow arrow between the two donuts ---
# Use figure-level coordinates
arrow = fig.add_axes([0.42, 0.38, 0.16, 0.24])  # [left, bottom, width, height]
arrow.set_xlim(0, 1)
arrow.set_ylim(0, 1)
arrow.axis('off')

# Big curved arrow from left to right
arrow.annotate('', xy=(0.95, 0.65), xytext=(0.05, 0.65),
               arrowprops=dict(arrowstyle='->', color='#cc0055', lw=4, 
                               connectionstyle='arc3,rad=0.0'))

# Label on the arrow
arrow.text(0.5, 0.82, '35% Fleet\nRedeployed', ha='center', va='center', 
           fontsize=13, fontweight='bold', color='#cc0055')

# Red arrow below (what's being taken)
arrow.annotate('', xy=(0.95, 0.35), xytext=(0.05, 0.35),
               arrowprops=dict(arrowstyle='->', color='#cc3333', lw=3, 
                               connectionstyle='arc3,rad=0.0', linestyle='dashed'))

arrow.text(0.5, 0.18, 'Feeder -35%\nIntercity -33%', ha='center', va='center', 
           fontsize=11, fontweight='bold', color='#cc3333')

# --- Main Title ---
fig.suptitle('Task 4: Fleet Reallocation Strategy — Feeder Cannibalization to Express Fortification', 
             fontsize=20, fontweight='bold', color='#111111', y=0.98)

# --- Strategy Callout Box at bottom ---
callout_text = ('Strategy: Cease surface competition with Metro Phase 2; '
                'fortify Express transit bridges.\n'
                'Headway Revision: Feeder 10→20 min  |  Express 15→8 min (Peak)')

fig.text(0.5, 0.02, callout_text, ha='center', va='bottom', fontsize=13, 
         fontweight='bold', color='#111111',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#fff3cd', edgecolor='#cc7700', 
                   linewidth=2, alpha=0.95))

plt.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.12, wspace=0.4)

# Save the chart
output_file = 'Task4_Fleet_Reallocation.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
