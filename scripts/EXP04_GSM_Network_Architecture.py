"""
Experiment 04: Study and Simulation of GSM Network Architecture
Course: Mobile and Cellular Communication Laboratory
Course Code: ICT-4204
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Node positions (x, y) for the simplified architecture diagram
NODES = {
    "MS": (0.5, 2.0),
    "BTS": (2.5, 2.0),
    "BSC": (4.5, 2.0),
    "MSC": (6.5, 2.0),
    "PSTN": (9.0, 2.0),
    "HLR": (7.5, 3.5),
    "VLR": (6.0, 3.5),
    "AUC": (9.0, 3.5),
    "EIR": (7.5, 0.5),
}

# Logical links (start, end, interface label)
EDGES = [
    ("MS", "BTS", "Um"),
    ("BTS", "BSC", "Abis"),
    ("BSC", "MSC", "A"),
    ("MSC", "PSTN", ""),
    ("MSC", "HLR", ""),
    ("MSC", "VLR", ""),
    ("HLR", "AUC", ""),  # the AUC is associated with the HLR
    ("MSC", "EIR", ""),
]

# Simplified mobile-originated call setup (source, destination, action)
CALL_SETUP_STEPS = [
    ("MS", "BTS", "Random access / service request"),
    ("BTS", "BSC", "Forward access request"),
    ("BSC", "MSC", "Call setup request"),
    ("MSC", "VLR/HLR/AUC", "Subscriber and security checks"),
    ("MSC", "BSC", "Authorize traffic-channel setup"),
    ("BSC", "BTS", "Activate radio traffic channel"),
    ("BTS", "MS", "Assign traffic channel"),
    ("MSC", "PSTN / Destination", "Establish outgoing connection"),
    ("Network", "MS", "Call connected"),
]


def draw_architecture(nodes, edges):
    """Draw boxes for GSM entities and bidirectional arrows for links."""
    plt.figure(figsize=(12, 6))

    for name, (x, y) in nodes.items():
        box = Rectangle((x - 0.45, y - 0.28), 0.9, 0.56, fill=False)
        plt.gca().add_patch(box)
        plt.text(x, y, name, ha="center", va="center", fontsize=11)

    for start, end, label in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        plt.annotate(
            "",
            xy=(x2 - 0.45 if x2 > x1 else x2 + 0.45, y2),
            xytext=(x1 + 0.45 if x2 > x1 else x1 - 0.45, y1),
            arrowprops=dict(arrowstyle="<->"),  # GSM links are bidirectional
        )
        if label:
            plt.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.18, label, ha="center")

    plt.xlim(-0.5, 10.2)
    plt.ylim(-0.2, 4.3)
    plt.axis("off")
    plt.title("Simplified GSM Network Architecture")


def main():
    # 1. Call setup sequence
    print("Simplified mobile-originated call setup:")
    for step_number, (source, destination, action) in enumerate(CALL_SETUP_STEPS, start=1):
        print(f"{step_number:02d}. {source:10s} -> {destination:20s}: {action}")

    # 2. Architecture diagram
    draw_architecture(NODES, EDGES)
    plt.show()


if __name__ == "__main__":
    main()
