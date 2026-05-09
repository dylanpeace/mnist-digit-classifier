import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
# STEP 1: Define Nairobi's 17 Sub-Counties & Adjacency

sub_counties = [
    'Westlands', 'Dagoretti North', 'Dagoretti South', 'Langata',
    'Kibra', 'Roysambu', 'Kasarani', 'Ruaraka', 'Embakasi North',
    'Embakasi West', 'Embakasi Central', 'Embakasi East', 'Embakasi South',
    'Makadara', 'Kamukunji', 'Starehe', 'Mathare'
]

# Adjacency based on geographic borders of Nairobi sub-counties
adjacency = {
    'Westlands':        ['Roysambu', 'Kasarani', 'Dagoretti North', 'Starehe'],
    'Dagoretti North':  ['Westlands', 'Dagoretti South', 'Kibra', 'Starehe'],
    'Dagoretti South':  ['Dagoretti North', 'Kibra', 'Langata'],
    'Langata':          ['Dagoretti South', 'Kibra', 'Embakasi West'],
    'Kibra':            ['Dagoretti North', 'Dagoretti South', 'Langata', 'Embakasi West', 'Starehe'],
    'Roysambu':         ['Westlands', 'Kasarani', 'Ruaraka', 'Starehe'],
    'Kasarani':         ['Westlands', 'Roysambu', 'Ruaraka', 'Embakasi North', 'Mathare'],
    'Ruaraka':          ['Roysambu', 'Kasarani', 'Embakasi North', 'Mathare', 'Starehe'],
    'Embakasi North':   ['Kasarani', 'Ruaraka', 'Embakasi West', 'Embakasi Central', 'Embakasi East'],
    'Embakasi West':    ['Langata', 'Kibra', 'Embakasi North', 'Embakasi Central', 'Embakasi South'],
    'Embakasi Central': ['Embakasi North', 'Embakasi West', 'Embakasi East', 'Embakasi South', 'Makadara'],
    'Embakasi East':    ['Embakasi North', 'Embakasi Central', 'Embakasi South'],
    'Embakasi South':   ['Embakasi West', 'Embakasi Central', 'Embakasi East', 'Makadara'],
    'Makadara':         ['Embakasi Central', 'Embakasi South', 'Kamukunji', 'Starehe'],
    'Kamukunji':        ['Makadara', 'Starehe', 'Mathare'],
    'Starehe':          ['Westlands', 'Dagoretti North', 'Kibra', 'Roysambu', 'Ruaraka',
                         'Makadara', 'Kamukunji', 'Mathare'],
    'Mathare':          ['Kasarani', 'Ruaraka', 'Kamukunji', 'Starehe'],
}

# STEP 2: CSP Solver – Try Minimum Colours First

def is_valid(node, colour, assignment):
    for neighbour in adjacency[node]:
        if neighbour in assignment and assignment[neighbour] == colour:
            return False
    return True

def backtrack(assignment, nodes, colours):
    if len(assignment) == len(nodes):
        return assignment
    unassigned = [n for n in nodes if n not in assignment]
    node = unassigned[0]
    for colour in colours:
        if is_valid(node, colour, assignment):
            assignment[node] = colour
            result = backtrack(assignment, nodes, colours)
            if result is not None:
                return result
            del assignment[node]
    return None

def solve_with_minimum_colours(nodes):
    """Try increasing numbers of colours until a solution is found."""
    colour_options = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple']
    for num_colours in range(1, len(colour_options) + 1):
        colours = colour_options[:num_colours]
        print(f"   Trying with {num_colours} colour(s): {colours} ...")
        result = backtrack({}, nodes, colours)
        if result is not None:
            print(f"   ✅ Solved with {num_colours} colours!\n")
            return result, colours
    return None, []
# STEP 3: Solve

print("=" * 55)
print("   Nairobi Sub-Counties Map Colouring – CSP Solver")
print("=" * 55)
print()
solution, colours_used = solve_with_minimum_colours(sub_counties)

if solution:
    print("Colour Assignment:")
    for sc, colour in solution.items():
        print(f"   {sc:20s} → {colour}")
    print()
    print(f"Minimum colours needed: {len(colours_used)}")
    print()
else:
    print("No solution found.")
    exit()
# STEP 4: Verify Constraints

print("Constraint Check:")
all_ok = True
for sc, neighbours in adjacency.items():
    for neighbour in neighbours:
        if solution[sc] == solution[neighbour]:
            print(f"   ❌ VIOLATION: {sc} and {neighbour} both → {solution[sc]}")
            all_ok = False
if all_ok:
    print("   ✅ All constraints satisfied – no adjacent sub-counties share a colour!\n")

# STEP 5: Visualise the Nairobi Map

# Colour palette
palette = {
    'Red':    '#E74C3C',
    'Blue':   '#2980B9',
    'Green':  '#27AE60',
    'Yellow': '#F1C40F',
    'Orange': '#E67E22',
    'Purple': '#8E44AD',
}

# Approximate (x, y) grid positions for each sub-county (schematic layout)
positions = {
    'Westlands':        (2, 7),
    'Roysambu':         (4, 8),
    'Kasarani':         (6, 8),
    'Mathare':          (5, 7),
    'Ruaraka':          (6, 7),
    'Dagoretti North':  (2, 6),
    'Starehe':          (4, 6),
    'Kamukunji':        (5, 6),
    'Embakasi North':   (7, 7),
    'Dagoretti South':  (2, 5),
    'Kibra':            (3, 5),
    'Makadara':         (5, 5),
    'Embakasi West':    (6, 5),
    'Embakasi Central': (7, 5),
    'Embakasi East':    (8, 5),
    'Langata':          (2, 4),
    'Embakasi South':   (7, 4),
}

fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor('#0f0f1a')
ax.set_facecolor('#0f0f1a')

box_w, box_h = 1.6, 0.85

# Draw adjacency lines first (behind boxes)
drawn_edges = set()
for sc, neighbours in adjacency.items():
    x1, y1 = positions[sc]
    for nb in neighbours:
        edge = tuple(sorted([sc, nb]))
        if edge not in drawn_edges:
            x2, y2 = positions[nb]
            ax.plot([x1, x2], [y1, y2], color='#444466', linewidth=1.2,
                    zorder=1, alpha=0.6)
            drawn_edges.add(edge)

# Draw sub-county boxes
for sc, (x, y) in positions.items():
    colour_name = solution[sc]
    c = palette[colour_name]

    rect = mpatches.FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.08",
        facecolor=c, edgecolor='white', linewidth=1.5,
        zorder=2, alpha=0.93
    )
    ax.add_patch(rect)

    # Sub-county name
    short = sc.replace('Embakasi ', 'Emb.\n').replace(' ', '\n') if len(sc) > 12 else sc
    ax.text(x, y + 0.12, short,
            ha='center', va='center', fontsize=7.5,
            fontweight='bold', color='white', zorder=3,
            path_effects=[pe.withStroke(linewidth=2, foreground='black')])

    # Colour label
    ax.text(x, y - 0.22, f'[{colour_name}]',
            ha='center', va='center', fontsize=6.5,
            color='white', alpha=0.85, zorder=3)

# Title
ax.text(0.5, 0.97,
        'Nairobi Sub-Counties – CSP Map Colouring',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=15, fontweight='bold', color='white')
ax.text(0.5, 0.93,
        f'Minimum colours needed: {len(colours_used)}  |  Sub-counties: {len(sub_counties)}',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=10, color='#aaaacc')

# Legend
legend_patches = [mpatches.Patch(color=palette[c], label=c) for c in colours_used]
ax.legend(handles=legend_patches, loc='lower center',
          bbox_to_anchor=(0.5, 0.01), ncol=len(colours_used),
          fontsize=10, facecolor='#1a1a2e',
          edgecolor='white', labelcolor='white', framealpha=0.9)

ax.set_xlim(0.5, 10)
ax.set_ylim(2.8, 9.5)
ax.axis('off')

plt.tight_layout()
plt.savefig('nairobi_map.png', dpi=130, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("Nairobi map saved to 'nairobi_map.png'")
