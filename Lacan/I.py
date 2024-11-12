import os

import matplotlib.pyplot as plt
import numpy as np


def draw_i_schema():
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot points
    ax.plot(0, 0, 'ko')  # a
    ax.plot(1, 0, 'ko')  # A
    ax.plot(0.5, 0.5, 'ko')  # $ (Es)

    # Labels
    ax.text(0, -0.1, 'a', fontsize=15, ha='center')
    ax.text(1, -0.1, 'A', fontsize=15, ha='center')
    ax.text(0.5, 0.6, 'S', fontsize=15, ha='center')
    
    # Lines
    ax.plot([0, 1], [0, 0], 'k-')
    ax.plot([0, 0.5], [0, 0.5], 'k--')
    ax.plot([1, 0.5], [0, 0.5], 'k--')

    # Annotations
    ax.text(0.25, 0.25, 'relación imaginaria', fontsize=10, ha='center', rotation=45)
    ax.text(0.75, 0.25, 'inconsciente', fontsize=10, ha='center', rotation=-45)

    # Limits and aspect
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1)
    ax.set_aspect('equal')

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.set_title("I Schema (Loss of reality in psychosis)", fontsize=15)

    # plt.show()

    # Create img folder if it doesn't exist
    os.makedirs('img', exist_ok=True)

    # Save the figure
    plt.savefig('img/I.png', dpi=300)  # Save as a PNG file with high resolution
    plt.close()  # Close the figure
    
    print("I scheme image saved in the 'img' folder.")
    
draw_i_schema()


