import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

# ==========================================
# Subplot 1: Cannibalization
# ==========================================
ax1.set_title('Strategic Fleet Cannibalization\n(Weekday Optimization)', fontsize=16, fontweight='bold', color='#111111', pad=10)

# Left Circle: Intercity 109/110 (Grey/Underutilized)
circle_left = patches.Circle((2.5, 5), radius=1.8, facecolor='#f0f0f0', edgecolor='#cccccc', linewidth=2.5, alpha=0.9)
ax1.add_patch(circle_left)
ax1.text(2.5, 5.3, 'Intercity\n109 / 110', ha='center', va='center', fontsize=14, fontweight='bold', color='#bbbbbb')
ax1.text(2.5, 4.3, 'Underutilized', ha='center', va='center', fontsize=11, color='#cccccc', fontstyle='italic')

# Right Circle: City 101/103 (Red/Overloaded)
circle_right = patches.Circle((7.5, 5), radius=2.1, facecolor='#ffebe6', edgecolor='#cc0033', linewidth=3, alpha=0.9)
ax1.add_patch(circle_right)
ax1.text(7.5, 5.3, 'City\n101 / 103', ha='center', va='center', fontsize=16, fontweight='bold', color='#cc0033')
ax1.text(7.5, 4.2, 'Overload Risk', ha='center', va='center', fontsize=12, color='#881111', fontstyle='italic')

# Arrow connecting them -> "Cannibalization"
ax1.annotate('', xy=(5.4, 5), xytext=(4.3, 5),
             arrowprops=dict(facecolor='#0077cc', edgecolor='#0077cc', width=6, headwidth=18, headlength=18, alpha=0.9))
ax1.text(4.85, 5.4, '-15% Capacity\nShift', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#0077cc')


# ==========================================
# Subplot 2: Dynamic Weekend Roster
# ==========================================
ax2.set_title('Dynamic Weekend Roster\n(Leisure Realignment)', fontsize=16, fontweight='bold', color='#111111', pad=10)

# Left Circle: CBD & Industrial (Cyan/Corporate)
circle_left_2 = patches.Circle((2.5, 5), radius=1.9, facecolor='#e6f7ff', edgecolor='#0077cc', linewidth=2.5, alpha=0.9)
ax2.add_patch(circle_left_2)
ax2.text(2.5, 5.3, 'CBD &\nIndustrial', ha='center', va='center', fontsize=14, fontweight='bold', color='#0077cc')
ax2.text(2.5, 4.2, 'Weekend Drop', ha='center', va='center', fontsize=11, color='#005588', fontstyle='italic')

# Right Circle: Coastal Marina (Green/Leisure)
circle_right_2 = patches.Circle((7.5, 5), radius=2.1, facecolor='#e6ffe6', edgecolor='#22aa22', linewidth=3, alpha=0.9)
ax2.add_patch(circle_right_2)
ax2.text(7.5, 5.3, 'Coastal\nMarina', ha='center', va='center', fontsize=15, fontweight='bold', color='#22aa22')
ax2.text(7.5, 4.2, 'Weekend Surge', ha='center', va='center', fontsize=12, color='#116611', fontstyle='italic')

# Arrow connecting them -> "Weekend Shift"
ax2.annotate('', xy=(5.4, 5), xytext=(4.4, 5),
             arrowprops=dict(facecolor='#cc0055', edgecolor='#cc0055', width=6, headwidth=18, headlength=18, alpha=0.9))
ax2.text(4.9, 5.4, '-25% Dispatches\nInjected', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#cc0055')


# Add Impact Subtitles
ax1.text(5, 1, "Expected Impact: Compresses headways on City routes without requiring new CAPEX.", 
         ha='center', va='center', fontsize=10, fontstyle='italic', color='#444444')

ax2.text(5, 1, "Expected Impact: Eliminates dead mileage in CBDs and captures peak leisure revenue.", 
         ha='center', va='center', fontsize=10, fontstyle='italic', color='#444444')

# ==========================================
# Titles and Layout
# ==========================================
plt.figtext(0.5, 0.95, 'Task 5: Initial Fleet Allocation Strategy', 
            fontsize=22, fontweight='bold', ha='center', color='#111111', family='sans-serif')
plt.figtext(0.5, 0.88, 'Mandatory Shift to Dynamic Scheduling and Route Cannibalization', 
            fontsize=15, fontstyle='italic', ha='center', color='#bbbbbb', family='sans-serif')

plt.tight_layout()
plt.subplots_adjust(top=0.78)

# Save the chart
output_file = 'Task5_Fleet_Allocation_Strategy.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#ffffff')
print(f"Chart successfully saved as {output_file}")
