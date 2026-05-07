import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import numpy as np


SUB_COUNTIES = [
    'Westlands', 'Kasarani', 'Ruaraka', 'Embakasi North',
    'Embakasi West', 'Embakasi Central', 'Embakasi East', 'Embakasi South',
    'Makadara', 'Kamukunji', 'Starehe', 'Mathare',
    'Roysambu', 'Dagoretti North', 'Dagoretti South', 'Langata', 'Kibra'
]


ADJACENCY = {
    'Westlands':        ['Kasarani', 'Roysambu', 'Dagoretti North', 'Starehe'],
    'Kasarani':         ['Westlands', 'Roysambu', 'Ruaraka', 'Mathare'],
    'Ruaraka':          ['Kasarani', 'Mathare', 'Embakasi North'],
    'Embakasi North':   ['Ruaraka', 'Embakasi West', 'Embakasi Central', 'Mathare'],
    'Embakasi West':    ['Embakasi North', 'Embakasi Central', 'Makadara', 'Kamukunji'],
    'Embakasi Central': ['Embakasi North', 'Embakasi West', 'Embakasi East', 'Makadara'],
    'Embakasi East':    ['Embakasi Central', 'Embakasi South', 'Makadara'],
    'Embakasi South':   ['Embakasi East', 'Makadara', 'Langata'],
    'Makadara':         ['Embakasi West', 'Embakasi Central', 'Embakasi East',
                         'Embakasi South', 'Kamukunji', 'Starehe', 'Langata'],
    'Kamukunji':        ['Embakasi West', 'Makadara', 'Starehe'],
    'Starehe':          ['Westlands', 'Kamukunji', 'Makadara', 'Mathare',
                         'Dagoretti North', 'Kibra'],
    'Mathare':          ['Kasarani', 'Ruaraka', 'Embakasi North', 'Starehe', 'Kamukunji'],
    'Roysambu':         ['Westlands', 'Kasarani', 'Dagoretti North'],
    'Dagoretti North':  ['Westlands', 'Roysambu', 'Starehe', 'Dagoretti South'],
    'Dagoretti South':  ['Dagoretti North', 'Starehe', 'Kibra', 'Langata'],
    'Langata':          ['Dagoretti South', 'Kibra', 'Makadara', 'Embakasi South'],
    'Kibra':            ['Starehe', 'Dagoretti South', 'Langata'],
}



def get_legal_colours(region, assignment, num_colours):
    """Return colours not used by any assigned neighbour."""
    used = {assignment[nb] for nb in ADJACENCY[region] if nb in assignment}
    return [c for c in range(num_colours) if c not in used]


def mrv_select(unassigned, assignment, num_colours):
    """MRV heuristic: pick the variable with fewest legal values remaining."""
    return min(unassigned,
               key=lambda r: len(get_legal_colours(r, assignment, num_colours)))


def backtrack(assignment, regions, num_colours):
    if len(assignment) == len(regions):
        return assignment
    unassigned = [r for r in regions if r not in assignment]
    region = mrv_select(unassigned, assignment, num_colours)
    for colour in get_legal_colours(region, assignment, num_colours):
        assignment[region] = colour
        result = backtrack(assignment, regions, num_colours)
        if result is not None:
            return result
        del assignment[region]
    return None


def find_minimum_colours(regions):
    """Try increasing numbers of colours until a solution is found."""
    for k in range(1, len(regions) + 1):
        print(f"Trying with {k} colour(s)...", end=' ')
        solution = backtrack({}, regions, k)
        if solution is not None:
            print(f"✅ Solvable!")
            return k, solution
        print("❌ Not enough.")
    return None, None


print("=" * 55)
print("  CSP – Nairobi Sub-County Map Colouring")
print("  Goal: Minimum colours, no adjacent same colour")
print("=" * 55 + "\n")

min_colours, solution = find_minimum_colours(SUB_COUNTIES)

if solution:
    print(f"\n🎨 Minimum colours needed: {min_colours}")
    print("-" * 45)
    colour_names = ['Red', 'Blue', 'Green', 'Yellow',
                    'Orange', 'Purple', 'Cyan', 'Magenta']
    print("\nSolution:")
    for sc in SUB_COUNTIES:
        cname = colour_names[solution[sc]] if solution[sc] < len(colour_names) else str(solution[sc])
        print(f"  {sc:22s} → {cname}")

    # Verify
    violations = 0
    for sc, neighbours in ADJACENCY.items():
        for nb in neighbours:
            if solution[sc] == solution[nb]:
                print(f"  ❌ VIOLATION: {sc} & {nb}")
                violations += 1
    if violations == 0:
        print(f"\n  ✅ Verification passed – {min_colours} colours, no conflicts!")


n = len(SUB_COUNTIES)
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)


inner = ['Starehe', 'Makadara', 'Kamukunji', 'Embakasi Central']
outer = [s for s in SUB_COUNTIES if s not in inner]

pos = {}

for i, sc in enumerate(inner):
    a = i * 2 * np.pi / len(inner)
    pos[sc] = (0.9 * np.cos(a), 0.9 * np.sin(a))

for i, sc in enumerate(outer):
    a = i * 2 * np.pi / len(outer)
    pos[sc] = (2.5 * np.cos(a), 2.5 * np.sin(a))

PALETTE = ['#E05C5C', '#4A90D9', '#5CB85C', '#F5A623',
           '#9B59B6', '#1ABC9C', '#E67E22', '#2C3E50']

fig, ax = plt.subplots(figsize=(13, 11))
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-3.8, 3.8)
ax.set_ylim(-3.8, 3.8)
ax.set_title(f"Nairobi Sub-County Map Colouring\n"
             f"17 Sub-Counties | Minimum Colours Required: {min_colours}",
             fontsize=13, fontweight='bold', pad=15)


for sc, neighbours in ADJACENCY.items():
    x1, y1 = pos[sc]
    for nb in neighbours:
        x2, y2 = pos[nb]
        ax.plot([x1, x2], [y1, y2], color='#cccccc', linewidth=1, zorder=1)


radius = 0.38
for sc in SUB_COUNTIES:
    x, y = pos[sc]
    c_idx = solution[sc]
    circle = plt.Circle((x, y), radius,
                         color=PALETTE[c_idx], ec='white', linewidth=2.5, zorder=2)
    ax.add_patch(circle)
    
    label = sc.replace(' ', '\n') if len(sc) > 10 else sc
    ax.text(x, y, label, ha='center', va='center',
            fontsize=6.8, fontweight='bold', color='white', zorder=3)


legend_handles = [
    mpatches.Patch(color=PALETTE[i],
                   label=colour_names[i] if i < len(colour_names) else f"Color {i}")
    for i in range(min_colours)
]
ax.legend(handles=legend_handles, loc='lower right', fontsize=10,
          title=f'Colours Used ({min_colours})', title_fontsize=10,
          framealpha=0.9, bbox_to_anchor=(1.0, 0.0))

plt.tight_layout()
plt.savefig("nairobi_map_colouring.png", dpi=130, bbox_inches='tight')
plt.show()
print("\nMap saved as 'nairobi_map_colouring.png'")
