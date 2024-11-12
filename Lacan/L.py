import os

import matplotlib.pyplot as plt


def draw_l_schema():
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot points
    ax.plot(0, 1, 'ko')  # S (Es)
    ax.plot(1, 0, 'ko')  # A (Otro)
    ax.plot(-1, 0, 'ko')  # a (yo)
    ax.plot(0, -1, 'ko')  # a' (otro)

    # Labels
    ax.text(0, 1.1, 'S (Es)', fontsize=12, ha='center')
    ax.text(1.1, 0, 'A (Otro)', fontsize=12, ha='center')
    ax.text(-1.1, 0, 'a (yo)', fontsize=12, ha='center')
    ax.text(0, -1.1, "a' (otro)", fontsize=12, ha='center')

    # Lines
    ax.plot([0, 1], [1, 0], 'k--')
    ax.plot([0, -1], [1, 0], 'k--')
    ax.plot([1, -1], [0, 0], 'k-')
    ax.plot([0, 0], [1, -1], 'k-')

    # Annotations
    ax.text(0.5, 0.5, 'relación imaginaria', fontsize=10, ha='center')
    ax.text(0, 0.5, 'inconsciente', fontsize=10, ha='center', rotation=90)

    # Limits and aspect
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.set_title("L Schema (Communication structure)", fontsize=15)

    # plt.show()

    # Create img folder if it doesn't exist
    os.makedirs('img', exist_ok=True)
    
    # Save the figure
    plt.savefig('img/L.png', dpi=300)  # Save as a PNG file with high resolution
    plt.close()  # Close the figure
    
    print("L Schema image saved in the 'img' folder.")

draw_l_schema()

