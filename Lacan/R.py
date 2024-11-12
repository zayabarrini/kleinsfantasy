import os

import matplotlib.pyplot as plt
import numpy as np


def draw_r_schema():
    fig, ax = plt.subplots(figsize=(6, 6))

    # Lines
    ax.plot([0, 1], [1, 0], 'k-')
    ax.plot([0, 1], [0, 1], 'k--')
    ax.plot([0, 0], [0, 1], 'k--')
    ax.plot([0, 1], [0, 0], 'k--')
    ax.plot([0, 1], [1, 1], 'k--')
    ax.plot([1, 1], [0, 1], 'k--')

    # Labels
    ax.text(0, 1, 'Φ', fontsize=15, ha='center')
    ax.text(1, 1, 'I', fontsize=15, ha='center')
    ax.text(1, 0, 'A', fontsize=15, ha='center')
    ax.text(0, 0, 'a\'', fontsize=15, ha='center')
    ax.text(0.5, 1.05, 'i', fontsize=12, ha='center')
    ax.text(0.5, -0.05, 'm', fontsize=12, ha='center')
    ax.text(-0.05, 0.5, 'm', fontsize=12, va='center', rotation=90)
    ax.text(1.05, 0.5, 'I', fontsize=12, va='center', rotation=90)

    # Limits and aspect
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_aspect('equal')

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.set_title("R Schema (Structure of reality in neurosis)", fontsize=15)

    # plt.show()
    
    # Create img folder if it doesn't exist
    os.makedirs('img', exist_ok=True)
    
    # Save the figure
    plt.savefig('img/R.png', dpi=300)  # Save as a PNG file with high resolution
    plt.close()  # Close the figure
    
    print("R Schema image saved in the 'img' folder.")
draw_r_schema()

