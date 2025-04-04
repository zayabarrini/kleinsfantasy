import os

import matplotlib.pyplot as plt
import numpy as np


# Function to generate Klein Bottle coordinates
def klein_bottle(u, v):
    x = (2/15) * (3 * np.cos(u) + np.cos(3 * u)) * (2 + np.sin(v))
    y = (2/15) * (3 * np.sin(u) - np.sin(3 * u)) * (2 + np.sin(v))
    z = (1/5) * (np.sin(v) + 2 * np.sin(u))
    return x, y, z

# Create u and v values
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, 2 * np.pi, 50)
u, v = np.meshgrid(u, v)

# Get the Klein Bottle coordinates
x, y, z = klein_bottle(u, v)

# Plotting
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')  # Updated line
ax.plot_surface(x, y, z, color='cyan', edgecolor='k', alpha=0.7)

# Set labels and title
ax.set_title("Klein Bottle")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

# Create img folder if it doesn't exist
os.makedirs('img', exist_ok=True)

# Save the figure
plt.savefig('img/k2.png', dpi=300)  # Save as a PNG file with high resolution
plt.close()  # Close the figure

print("Klein Bottle image saved in the 'img' folder.")

