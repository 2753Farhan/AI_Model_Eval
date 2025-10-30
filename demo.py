import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Define milestones and tasks with durations
milestones = {
    'Milestone 1: Foundation': [
        ('Environment Setup & Data Acquisition', 1),
        ('Static Analysis Tools Configuration', 2),
        ('Human Baseline Metrics Calculation', 1)
    ],
    'Milestone 2: Code Generation': [
        ('Design Prompt Strategies', 2),
        ('Configure Free LLM APIs', 1),
        ('Automated Code Generation', 2)
    ],
    'Milestone 3: Functional Testing': [
        ('Implement Secure Sandbox', 2),
        ('Automated Test Execution', 1),
        ('Calculate Pass@k Metrics', 1)
    ],
    'Milestone 4: Quality Analysis': [
        ('Batch Static Analysis', 2),
        ('Data Aggregation & Normalization', 1),
        ('Statistical Comparison', 1)
    ],
    'Milestone 5: Synthesis & Reporting': [
        ('Implement TOPSIS Algorithm', 2),
        ('Final Rankings & Dashboard Deployment', 2),
        ('Final Documentation & Submission', 1)
    ]
}

# Colors for different milestones
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

# Calculate positions and dates
start_date = datetime(2024, 9, 1)
current_week = 0
y_pos = 0

# Plot each task
for i, (milestone, tasks) in enumerate(milestones.items()):
    # Add milestone label
    ax.text(-0.5, y_pos + len(tasks)/2 - 0.5, milestone, 
            ha='right', va='center', fontweight='bold', fontsize=10)
    
    for j, (task, duration) in enumerate(tasks):
        # Calculate start and end weeks
        start_week = current_week
        end_week = current_week + duration
        
        # Create rectangle for task
        rect = patches.Rectangle(
            (start_week, y_pos), duration, 0.8,
            linewidth=1, edgecolor='black', facecolor=colors[i], alpha=0.7
        )
        ax.add_patch(rect)
        
        # Add task text
        ax.text(start_week + duration/2, y_pos + 0.4, task, 
                ha='center', va='center', fontsize=9, weight='bold')
        
        # Add week labels
        ax.text(start_week, y_pos - 0.1, f'W{start_week+1}', 
                ha='left', va='top', fontsize=8)
        if j == len(tasks) - 1:  # Last task in milestone
            ax.text(end_week, y_pos - 0.1, f'W{end_week+1}', 
                    ha='right', va='top', fontsize=8)
        
        y_pos += 1
        current_week = end_week
    
    y_pos += 0.5  # Space between milestones

# Configure plot appearance
ax.set_xlim(-2, 16)
ax.set_ylim(0, y_pos)
ax.set_xlabel('Weeks', fontweight='bold', fontsize=12)
ax.set_ylabel('Tasks', fontweight='bold', fontsize=12)
ax.set_title('CodeQualBench Project Timeline (15 Weeks)', 
             fontweight='bold', fontsize=14, pad=20)

# Add week grid
for week in range(0, 16):
    ax.axvline(x=week, color='gray', linestyle='--', alpha=0.3, linewidth=0.5)

# Customize ticks
ax.set_xticks(range(0, 16))
ax.set_xticklabels([f'W{i+1}' for i in range(16)])
ax.set_yticks([])

# Add legend
legend_elements = [
    patches.Patch(color=colors[i], label=list(milestones.keys())[i])
    for i in range(len(milestones))
]
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, -0.1))

plt.tight_layout()
plt.grid(True, axis='x', alpha=0.3)
plt.show()

# Print summary
print("Project Timeline Summary:")
print("=" * 50)
current_week = 0
for milestone, tasks in milestones.items():
    print(f"\n{milestone}:")
    for task, duration in tasks:
        print(f"  Weeks {current_week+1}-{current_week+duration}: {task}")
        current_week += duration