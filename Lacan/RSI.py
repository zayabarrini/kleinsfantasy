import os

import matplotlib.pyplot as plt


def draw_rsi_schema():
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw circles
    circle_S = plt.Circle((0.5, 0.5), 0.4, color='blue', alpha=0.3)
    circle_R = plt.Circle((0.8, 0.5), 0.4, color='red', alpha=0.3)
    circle_I = plt.Circle((0.65, 0.8), 0.4, color='green', alpha=0.3)

    ax.add_artist(circle_S)
    ax.add_artist(circle_R)
    ax.add_artist(circle_I)

    # Labels
    ax.text(0.5, 0.5, 'S', fontsize=15, ha='center', color='blue')
    ax.text(0.8, 0.5, 'R', fontsize=15, ha='center', color='red')
    ax.text(0.65, 0.8, 'I', fontsize=15, ha='center', color='green')

    # Limits and aspect
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1.5)
    ax.set_aspect('equal')

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.set_title("RSI Venn Diagram", fontsize=20)

    # plt.show()# Create img folder if it doesn't exist
    os.makedirs('img', exist_ok=True)
    
    # Save the figure
    plt.savefig('img/RSI.png', dpi=300)  # Save as a PNG file with high resolution
    plt.close()  # Close the figure
    
    print("RSI image saved in the 'img' folder.")

draw_rsi_schema()

