"""EXP08 - Cell Coverage, Radius and Cell Splitting (ICT-4204).

Figure 1: Circular and hexagonal coverage area vs radius.
Figure 2: One large cell before splitting and seven small cells afterward.
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Parameters (same as exp8.m)
R = 1.0                 # Original cell radius (km)
r = 0.35 * R            # Small-cell radius (km)
n = 4                   # Path-loss exponent

# 2. Coverage area and power calculations
Ac0 = np.pi * R**2
Ac1 = np.pi * r**2
Ah0 = (3 * np.sqrt(3) / 2) * R**2
Ah1 = (3 * np.sqrt(3) / 2) * r**2
P = (r / R)**n

d = np.sqrt(3) * r     # Center-to-center spacing of small cells

print(f"Old radius R = {R:.2f} km, small radius r = {r:.2f} km")
print(f"Circle: old = {Ac0:.3f}, small = {Ac1:.3f} km^2")
print(f"Hexagon: old = {Ah0:.3f}, small = {Ah1:.3f} km^2")
print(f"Area ratio = {(r/R)**2:.4f} ({100*(r/R)**2:.2f}%)")
print(f"Power ratio = {P:.5f} ({10*np.log10(P):.2f} dB)")
print(f"Small-cell center spacing = {d:.3f} km")

# 3. Figure 1 - Coverage area versus cell radius
rv = np.linspace(0, 2 * R, 200)
Ac = np.pi * rv**2
Ah = (3 * np.sqrt(3) / 2) * rv**2

plt.figure(figsize=(9, 5))
plt.plot(rv, Ac, "b-", lw=2, label="Circular area")
plt.plot(rv, Ah, "m--", lw=2, label="Hexagonal area")
plt.plot(R, Ah0, "ko", markersize=7)
plt.plot(r, Ah1, "ks", markersize=7)
plt.text(R + 0.06, Ah0, "Original R")
plt.text(r + 0.06, Ah1, "Small r")
plt.xlabel("Cell radius (km)")
plt.ylabel("Coverage area (km²)")
plt.title("Cell Coverage Area vs Radius")
plt.legend()
plt.grid(True, alpha=0.35)
plt.tight_layout()

# 4. Figure 2 - Before and after cell splitting
# Pointy-top hexagonal vertices; final point closes each boundary.
t = np.deg2rad(np.arange(30, 391, 60))
xy = np.array([
    [0, 0], [d, 0], [d / 2, 1.5 * r], [-d / 2, 1.5 * r],
    [-d, 0], [-d / 2, -1.5 * r], [d / 2, -1.5 * r]
])

fig, ax = plt.subplots(1, 2, figsize=(11, 5), constrained_layout=True)

# Before: one large cell
ax[0].fill(R * np.cos(t), R * np.sin(t), color="#dee3ec", ec="black", lw=1.7)
ax[0].plot(0, 0, "k^", ms=9)  # Base station
ax[0].plot([0, R * np.cos(t[0])], [0, R * np.sin(t[0])], "b-", lw=2)
ax[0].text(0.45 * R, 0.33 * R, "R", color="blue", weight="bold")
ax[0].set_title("Before Splitting: One Large Cell")

# After: seven small hexagons (1 center + 6 neighbors)
for k, (x, y) in enumerate(xy, start=1):
    col = "#b8d6ff" if k == 1 else "#e8e8e8"
    ax[1].fill(x + r * np.cos(t), y + r * np.sin(t),
               color=col, ec="black", lw=1.2)
    ax[1].plot(x, y, "k^", ms=5)  # New base station
    ax[1].text(x, y - 0.45 * r, f"C{k}", ha="center", fontsize=8)

# Show radius r of small cell C2
x, y = xy[1]
ax[1].plot([x, x + r * np.cos(t[0])], [y, y + r * np.sin(t[0])], "b-", lw=2)
ax[1].text(x + 0.4 * r, y + 0.37 * r, "r", color="blue", weight="bold")

# Reference outline of original cell (not an exact partition)
ax[1].plot(R * np.cos(t), R * np.sin(t), "k--", lw=1.5,
           label="Old cell boundary")
ax[1].legend(loc="lower center", bbox_to_anchor=(0.5, -0.19), fontsize=9)
ax[1].set_title("After Splitting: Seven Small Cells (Schematic)")

for a in ax:
    a.set_aspect("equal", adjustable="box")
    a.set_xlim(-1.3 * R, 1.3 * R)
    a.set_ylim(-1.3 * R, 1.3 * R)
    a.set_xlabel("Distance (km)")
    a.set_ylabel("Distance (km)")
    a.grid(True, alpha=0.25)
    a.set_axisbelow(True)

plt.show()
