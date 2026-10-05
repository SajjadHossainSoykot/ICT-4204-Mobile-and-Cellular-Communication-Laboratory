"""
Experiment 08: Analysis of Cell Coverage, Cell Radius, and Cell Splitting
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

# Configurable parameters
ORIGINAL_RADIUS_KM = 2.0
SPLIT_FACTOR = 2.0          # R2 = R1 / m
PATH_LOSS_EXPONENT = 4.0    # course R^-4 mobile-radio model


def circular_area(radius_km):
    """A = pi R^2 (km^2)."""
    return np.pi * radius_km**2


def hexagonal_area(radius_km):
    """A = (3 sqrt(3) / 2) R^2 for center-to-vertex radius R (km^2)."""
    return (3 * np.sqrt(3) / 2) * radius_km**2


def main():
    split_radius_km = ORIGINAL_RADIUS_KM / SPLIT_FACTOR

    # Pt2 / Pt1 = (R2 / R1)^n for an unchanged receiver threshold
    power_ratio = (split_radius_km / ORIGINAL_RADIUS_KM) ** PATH_LOSS_EXPONENT
    power_change_db = 10 * np.log10(power_ratio)  # power_ratio > 0, so log10 is defined

    results = pd.DataFrame({
        "Quantity": [
            "Original radius (km)",
            "Split radius (km)",
            "Original circular area (km²)",
            "Split circular area (km²)",
            "Original hexagonal area (km²)",
            "Split hexagonal area (km²)",
            "Pt_new / Pt_old",
            "Power change (dB)",
        ],
        "Value": [
            ORIGINAL_RADIUS_KM,
            split_radius_km,
            circular_area(ORIGINAL_RADIUS_KM),
            circular_area(split_radius_km),
            hexagonal_area(ORIGINAL_RADIUS_KM),
            hexagonal_area(split_radius_km),
            power_ratio,
            power_change_db,
        ],
    })
    print(results.to_string(index=False))

    # Cell radius versus coverage area
    radii_km = np.linspace(0.1, 5.0, 250)
    plt.figure(figsize=(9, 5))
    plt.plot(radii_km, circular_area(radii_km), label="Circular approximation")
    plt.plot(radii_km, hexagonal_area(radii_km), label="Hexagonal cell")
    plt.xlabel("Cell radius (km)")
    plt.ylabel("Coverage area (km²)")
    plt.title("Cell Radius vs Coverage Area")
    plt.legend()
    plt.grid(True)

    # Conceptual cell size before and after splitting
    plt.figure(figsize=(9, 5))
    ax = plt.gca()
    ax.add_patch(RegularPolygon((0, 0), numVertices=6, radius=ORIGINAL_RADIUS_KM,
                                orientation=np.pi / 6, fill=False, linewidth=2))
    ax.add_patch(RegularPolygon((5, 0), numVertices=6, radius=split_radius_km,
                                orientation=np.pi / 6, fill=False, linewidth=2))
    plt.text(0, -2.5, f"Original cell\nR = {ORIGINAL_RADIUS_KM:.1f} km", ha="center")
    plt.text(5, -2.5, f"Split cell\nR = {split_radius_km:.1f} km", ha="center")
    plt.xlim(-3, 7)
    plt.ylim(-3, 3)
    ax.set_aspect("equal", adjustable="box")
    plt.axis("off")
    plt.title("Conceptual Cell Radius Before and After Splitting")

    plt.show()


if __name__ == "__main__":
    main()
