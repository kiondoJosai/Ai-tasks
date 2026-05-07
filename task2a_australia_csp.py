import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict




REGIONS = ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS']


ADJACENCY = {
    'WA':  ['NT', 'SA'],
    'NT':  ['WA', 'SA', 'QLD'],
    'SA':  ['WA', 'NT', 'QLD', 'NSW', 'VIC'],
    'QLD': ['NT', 'SA', 'NSW'],
    'NSW': ['QLD', 'SA', 'VIC'],
    'VIC': ['SA', 'NSW'],
    'TAS': []  
}

COLOURS = ['Blue', 'Red', 'Green']



def is_consistent(region, colour, assignment):
    """Return True if assigning `colour` to `region` violates no constraints."""
    for neighbour in ADJACENCY[region]:
        if neighbour in assignment and assignment[neighbour] == colour:
            return False
    return True


def backtrack(assignment, regions):
    """Recursive backtracking search."""
    
    if len(assignment) == len(regions):
        return assignment

   
    unassigned = [r for r in regions if r not in assignment]
    region = unassigned[0]

    for colour in COLOURS:
        if is_consistent(region, colour, assignment):
            assignment[region] = colour
            print(f"  Trying  {region} = {colour}")
            result = backtrack(assignment, regions)
            if result is not None:
                return result
            print(f"  Backtrack from {region} = {colour}")
            del assignment[region]

    return None  



print("=" * 50)
print("  CSP – Australia Map Colouring")
print("  Colours: Blue, Red, Green")
print("=" * 50)
print("\nSearch trace:")
solution = backtrack({}, REGIONS)

if solution:
    print("\n✅ Solution found!")
    print("-" * 30)
    for region, colour in solution.items():
        print(f"  {region:5s} → {colour}")
    print("-" * 30)

    
    violations = 0
    for region, neighbours in ADJACENCY.items():
        for nb in neighbours:
            if solution[region] == solution[nb]:
                print(f"  ❌ VIOLATION: {region} and {nb} both = {solution[region]}")
                violations += 1
    if violations == 0:
        print("  ✅ Verification passed: no adjacent regions share a colour!")
else:
    print("❌ No solution found.")


COLOUR_MAP = {'Blue': '#4A90D9', 'Red': '#E05C5C', 'Green': '#5CB85C'}


REGION_BOXES = {
    'WA':  (0.0,  0.2, 1.8, 2.4),
    'NT':  (1.9,  1.2, 1.4, 1.4),
    'SA':  (1.9,  0.2, 1.4, 0.9),
    'QLD': (3.4,  1.2, 1.5, 1.4),
    'NSW': (3.4,  0.5, 1.5, 0.6),
    'VIC': (3.4,  0.2, 1.5, 0.2),
    'TAS': (3.9, -0.5, 0.8, 0.5),
}

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(-0.2, 5.5)
ax.set_ylim(-0.8, 2.9)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Australia Map Colouring – CSP Solution\n"
             "Rule: No two adjacent regions share the same colour",
             fontsize=13, fontweight='bold', pad=15)

for region, (x, y, w, h) in REGION_BOXES.items():
    colour = solution[region]
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.05",
        facecolor=COLOUR_MAP[colour],
        edgecolor='white', linewidth=2.5
    )
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, f"{region}\n({colour})",
            ha='center', va='center', fontsize=9.5,
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='none', edgecolor='none'))


legend_patches = [mpatches.Patch(color=COLOUR_MAP[c], label=c) for c in COLOURS]
ax.legend(handles=legend_patches, loc='lower left', fontsize=10,
          title='Colours Used', title_fontsize=10, framealpha=0.9)

plt.tight_layout()
plt.savefig("australia_map_colouring.png", dpi=130, bbox_inches='tight')
plt.show()
print("\nMap saved as 'australia_map_colouring.png'")
