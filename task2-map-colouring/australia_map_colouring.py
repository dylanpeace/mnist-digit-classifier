# ============================================================
# Task 2(a) – Constraint Satisfaction Problem (CSP)
# Map Colouring – Australia (5 Regions, 3 Colours)
# Foundations of Artificial Intelligence
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ─────────────────────────────────────────────
# STEP 1: Define the Regions and Adjacency
# ─────────────────────────────────────────────

# Five main regions of Australia (simplified)
regions = [
    'WA',   # Western Australia
    'NT',   # Northern Territory
    'SA',   # South Australia
    'QLD',  # Queensland
    'NSW',  # New South Wales
]

# Adjacency list – which regions share a border
adjacency = {
    'WA':  ['NT', 'SA'],
    'NT':  ['WA', 'SA', 'QLD'],
    'SA':  ['WA', 'NT', 'QLD', 'NSW'],
    'QLD': ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'QLD'],
}

colours = ['Blue', 'Red', 'Green']

# ─────────────────────────────────────────────
# STEP 2: CSP Solver using Backtracking
# ─────────────────────────────────────────────

def is_valid(region, colour, assignment):
    """Check if assigning this colour to this region violates any constraint."""
    for neighbour in adjacency[region]:
        if neighbour in assignment and assignment[neighbour] == colour:
            return False  # Neighbour has the same colour – constraint violated!
    return True

def backtrack(assignment):
    """Recursively try to assign colours to all regions."""
    # Base case: all regions are assigned
    if len(assignment) == len(regions):
        return assignment

    # Pick the next unassigned region
    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]

    # Try each colour
    for colour in colours:
        if is_valid(region, colour, assignment):
            assignment[region] = colour          # Assign colour
            result = backtrack(assignment)       # Recurse
            if result is not None:
                return result
            del assignment[region]               # Backtrack

    return None  # No valid colour found – trigger backtrack

# ─────────────────────────────────────────────
# STEP 3: Solve the CSP
# ─────────────────────────────────────────────

print("=" * 50)
print("   Australia Map Colouring – CSP Solver")
print("=" * 50)

solution = backtrack({})

if solution:
    print("\n✅ Solution Found!\n")
    for region, colour in solution.items():
        print(f"   {region:5s}  →  {colour}")
    print()
else:
    print("\n❌ No solution found.")

# ─────────────────────────────────────────────
# STEP 4: Verify No Adjacent Regions Share a Colour
# ─────────────────────────────────────────────

print("Constraint Check (no adjacent regions share a colour):")
all_ok = True
for region, neighbours in adjacency.items():
    for neighbour in neighbours:
        if solution[region] == solution[neighbour]:
            print(f"   ❌ VIOLATION: {region} and {neighbour} both have {solution[region]}")
            all_ok = False
if all_ok:
    print("   ✅ All constraints satisfied!\n")

# ─────────────────────────────────────────────
# STEP 5: Visualise the Coloured Map
# ─────────────────────────────────────────────

colour_map = {
    'Blue':  '#4A90D9',
    'Red':   '#E74C3C',
    'Green': '#2ECC71',
}

# Approximate polygon coordinates for each region (schematic, not exact geo)
region_shapes = {
    'WA':  {'x': 0.05, 'y': 0.15, 'w': 0.28, 'h': 0.70},
    'NT':  {'x': 0.35, 'y': 0.40, 'w': 0.22, 'h': 0.45},
    'SA':  {'x': 0.35, 'y': 0.10, 'w': 0.22, 'h': 0.30},
    'QLD': {'x': 0.59, 'y': 0.40, 'w': 0.22, 'h': 0.45},
    'NSW': {'x': 0.59, 'y': 0.10, 'w': 0.22, 'h': 0.30},
}

region_labels = {
    'WA':  'Western\nAustralia',
    'NT':  'Northern\nTerritory',
    'SA':  'South\nAustralia',
    'QLD': 'Queensland',
    'NSW': 'New South\nWales',
}

fig, ax = plt.subplots(1, 1, figsize=(12, 7))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Draw ocean background
ocean = FancyBboxPatch((0.02, 0.02), 0.96, 0.90,
                        boxstyle="round,pad=0.01",
                        facecolor='#1B4F72', edgecolor='#2980B9', linewidth=2)
ax.add_patch(ocean)

# Draw each region
for region, shape in region_shapes.items():
    c = colour_map[solution[region]]
    rect = FancyBboxPatch(
        (shape['x'], shape['y']), shape['w'], shape['h'],
        boxstyle="round,pad=0.01",
        facecolor=c, edgecolor='white', linewidth=2, alpha=0.92
    )
    ax.add_patch(rect)

    # Label
    cx = shape['x'] + shape['w'] / 2
    cy = shape['y'] + shape['h'] / 2
    ax.text(cx, cy + 0.04, region_labels[region],
            ha='center', va='center', fontsize=10,
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.3))
    ax.text(cx, cy - 0.07, f"[{solution[region]}]",
            ha='center', va='center', fontsize=9,
            color='white', alpha=0.85)

# Title
ax.text(0.5, 0.97, 'Australia Map Colouring – CSP Solution',
        ha='center', va='top', fontsize=14, fontweight='bold',
        color='white', transform=ax.transAxes)

# Legend
legend_patches = [mpatches.Patch(color=colour_map[c], label=c) for c in colours]
ax.legend(handles=legend_patches, loc='lower center',
          bbox_to_anchor=(0.5, 0.0), ncol=3,
          fontsize=10, facecolor='#1a1a2e',
          edgecolor='white', labelcolor='white')

plt.tight_layout()
plt.savefig('australia_map.png', dpi=120, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("Map saved to 'australia_map.png'")
